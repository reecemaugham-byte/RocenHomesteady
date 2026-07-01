import streamlit as st
import hashlib
import os
from datetime import datetime
from supabase import create_client, Client

# --- SUPABASE CONNECTION ---
def get_supabase():
    url = os.environ.get("SUPABASE_URL", "")
    key = os.environ.get("SUPABASE_KEY", "")
    if not url or not key:
        # Fallback to st.secrets for local dev
        try:
            url = st.secrets["SUPABASE_URL"]
            key = st.secrets["SUPABASE_KEY"]
        except:
            st.error("Supabase not configured. Set environment variables or secrets.")
            st.stop()
    return create_client(url, key)

# --- PASSWORD HASHING ---
def hash_password(password: str) -> str:
    salt = "rocen_homesteady_salt_2024"
    return hashlib.sha256(f"{password}{salt}".encode()).hexdigest()

# --- AUTH FUNCTIONS ---
def sign_up(email: str, username: str, password: str) -> tuple:
    supabase = get_supabase()
    try:
        # Check if email exists
        existing_email = supabase.table("users").select("email").eq("email", email).execute()
        if existing_email.data:
            return False, "That email is already registered."

        # Check if username exists
        existing_user = supabase.table("users").select("username").eq("username", username).execute()
        if existing_user.data:
            return False, "That username is already taken."

        # Insert new user
        hashed_pw = hash_password(password)
        result = supabase.table("users").insert({
            "email": email,
            "username": username,
            "hashed_password": hashed_pw,
            "is_active": True
        }).execute()

        return True, "Account created! You can now log in."
    except Exception as e:
        return False, f"Something went wrong: {str(e)}"

def log_in(email: str, password: str) -> tuple:
    supabase = get_supabase()
    try:
        hashed_pw = hash_password(password)
        result = supabase.table("users").select("*").eq("email", email).eq("hashed_password", hashed_pw).execute()

        if result.data:
            user = result.data[0]
            # Update last login
            try:
                supabase.table("users").update({
                    "last_login": datetime.utcnow().isoformat()
                }).eq("id", user["id"]).execute()
            except:
                pass  # Don't fail login if last_login update fails
            return True, user
        else:
            return False, "Invalid email or password."
    except Exception as e:
        return False, f"Something went wrong: {str(e)}"

# --- LOGIN / SIGNUP UI ---
def render_auth():
    """Show login/signup screen. Returns user dict if logged in, or None."""
    if "user" not in st.session_state:
        st.session_state.user = None

    # If already logged in, return user
    if st.session_state.user is not None:
        return st.session_state.user

    # Show login/signup form
    st.markdown("---")
    st.markdown("## 🌿 Welcome to Rocen Homesteady")
    st.markdown("*Please log in or create an account to continue.*")
    st.markdown("---")

    tab_login, tab_signup = st.tabs(["🔑 Log In", "📝 Create Account"])

    with tab_login:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("🔑 Log In", use_container_width=True)

            if submit:
                if not email or not password:
                    st.warning("Please fill in both fields.")
                else:
                    success, result = log_in(email, password)
                    if success:
                        st.session_state.user = result
                        st.success("Welcome back!")
                        st.rerun()
                    else:
                        st.error(result)

    with tab_signup:
        with st.form("signup_form"):
            new_email = st.text_input("Email", key="signup_email")
            new_username = st.text_input("Username", key="signup_username")
            new_password = st.text_input("Password", type="password", key="signup_password")
            new_password2 = st.text_input("Confirm Password", type="password", key="signup_password2")
            submit = st.form_submit_button("📝 Create Account", use_container_width=True)

            if submit:
                if not new_email or not new_username or not new_password:
                    st.warning("Please fill in all fields.")
                elif len(new_password) < 6:
                    st.warning("Password must be at least 6 characters.")
                elif new_password != new_password2:
                    st.warning("Passwords don't match.")
                else:
                    success, msg = sign_up(new_email, new_username, new_password)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)

    # Block the rest of the app
    st.stop()
    return None

def render_logout_sidebar():
    """Show logout button in sidebar. Call this after render_auth succeeds."""
    if st.session_state.get("user"):
        with st.sidebar:
            st.markdown("---")
            st.markdown(f"👤 **{st.session_state.user['username']}**")
            st.caption(f"📧 {st.session_state.user['email']}")
            if st.button("🚪 Log Out"):
                st.session_state.user = None
                st.rerun()
