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
def sign_up(username: str, password: str) -> tuple:
    supabase = get_supabase()
    try:
        existing_user = supabase.table("users").select("username").eq("username", username).execute()
        if existing_user.data:
            return False, "That username is already taken. Try a different one!"

        hashed_pw = hash_password(password)
        result = supabase.table("users").insert({
            "username": username,
            "hashed_password": hashed_pw,
            "is_active": True
        }).execute()

        return True, "Account created! You can now log in."
    except Exception as e:
        return False, f"Something went wrong: {str(e)}"

def log_in(username: str, password: str) -> tuple:
    supabase = get_supabase()
    try:
        hashed_pw = hash_password(password)
        result = supabase.table("users").select("*").eq("username", username).eq("hashed_password", hashed_pw).execute()

        if result.data:
            user = result.data[0]
            try:
                supabase.table("users").update({
                    "last_login": datetime.utcnow().isoformat()
                }).eq("id", user["id"]).execute()
            except:
                pass
            return True, user
        else:
            return False, "Invalid username or password."
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
    st.markdown("*Log in or create an account to save your progress.*")
    st.markdown("---")

    tab_login, tab_signup = st.tabs(["🔑 Log In", "📝 Create Account"])

    with tab_login:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("🔑 Log In", use_container_width=True)

            if submit:
                if not username or not password:
                    st.warning("Please fill in both fields.")
                else:
                    success, result = log_in(username, password)
                    if success:
                        st.session_state.user = result
                        # Auto-load saved progress on login
                        from utils import load_game, apply_save_data
                        saved_data = load_game(username)
                        if saved_data:
                            apply_save_data(saved_data)
                            st.session_state['game_loaded'] = True
                        st.success(f"Welcome back, {result['username']}!")
                        st.rerun()
                    else:
                        st.error(result)

    with tab_signup:
        with st.form("signup_form"):
            new_username = st.text_input("Choose a Username", key="signup_username")
            new_password = st.text_input("Choose a Password", type="password", key="signup_password")
            new_password2 = st.text_input("Confirm Password", type="password", key="signup_password2")
            submit = st.form_submit_button("📝 Create Account", use_container_width=True)

            if submit:
                if not new_username or not new_password:
                    st.warning("Please fill in all fields.")
                elif len(new_username) < 3:
                    st.warning("Username must be at least 3 characters.")
                elif len(new_password) < 4:
                    st.warning("Password must be at least 4 characters.")
                elif new_password != new_password2:
                    st.warning("Passwords don't match.")
                else:
                    success, msg = sign_up(new_username, new_password)
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
            if st.button("🚪 Log Out"):
                st.session_state.user = None
                st.rerun()
