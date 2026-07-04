import streamlit as st
import hashlib
from datetime import datetime
from utils import get_db_connection, load_game, apply_save_data

# --- PASSWORD HASHING ---
def hash_password(password: str) -> str:
    salt = "rocen_homesteady_salt_2024"
    return hashlib.sha256(f"{password}{salt}".encode()).hexdigest()

# --- DATABASE INIT FOR AUTH ---
def init_auth_db():
    """Create the users table if it doesn't exist."""
    conn = get_db_connection()
    if conn:
        try:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS users
                         (username TEXT PRIMARY KEY, 
                          hashed_password TEXT, 
                          is_active BOOLEAN DEFAULT TRUE,
                          created_at TEXT,
                          last_login TEXT)''')
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Auth DB Init Error: {e}")

# --- AUTH FUNCTIONS ---
def sign_up(username: str, password: str) -> tuple:
    init_auth_db() # ensure table exists
    conn = get_db_connection()
    if not conn:
        return False, "Database connection failed."
    try:
        c = conn.cursor()
        # Check if user exists
        c.execute("SELECT username FROM users WHERE username=%s", (username,))
        if c.fetchone():
            conn.close()
            return False, "That username is already taken. Try a different one!"

        # Insert new user
        hashed_pw = hash_password(password)
        created_at = datetime.utcnow().isoformat()
        c.execute("""INSERT INTO users (username, hashed_password, is_active, created_at) 
                     VALUES (%s, %s, %s, %s)""", 
                  (username, hashed_pw, True, created_at))
        conn.commit()
        conn.close()
        return True, "Account created! You can now log in."
    except Exception as e:
        return False, f"Something went wrong: {str(e)}"

def log_in(username: str, password: str) -> tuple:
    init_auth_db() # ensure table exists
    conn = get_db_connection()
    if not conn:
        return False, "Database connection failed."
    try:
        hashed_pw = hash_password(password)
        c = conn.cursor()
        c.execute("SELECT username FROM users WHERE username=%s AND hashed_password=%s", (username, hashed_pw))
        result = c.fetchone()

        if result:
            # Update last login time
            try:
                last_login = datetime.utcnow().isoformat()
                c.execute("UPDATE users SET last_login=%s WHERE username=%s", (last_login, username))
                conn.commit()
            except:
                pass
            conn.close()
            
            # Return a user dictionary
            user_data = {"username": username}
            return True, user_data
        else:
            conn.close()
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
                    success, msg = sign_up(new_username, password=new_password)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)

    # Block the rest of the app if not logged in
    st.stop()
    return None

def render_logout_sidebar():
    """Show logout button in sidebar. Call this after render_auth succeeds."""
    if st.session_state.get("user"):
        with st.sidebar:
            st.markdown("---")
            st.markdown(f"👤 **{st.session_state.user['username']}**")
            if st.button("🚪 Log Out"):
                # Clear all session state for a clean logout
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
