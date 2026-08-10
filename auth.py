"""
Authentication module for Rocen Homesteady.
Handles user registration, login, JWT tokens, and password management.
Supports migration from legacy SHA256+salt (Streamlit) to bcrypt.
Uses asyncpg for non-blocking database access via shared pool.
"""

import os
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple

from jose import JWTError, jwt
from passlib.context import CryptContext

import db


# ==========================================
# CONFIGURATION
# ==========================================

SECRET_KEY = os.environ.get(
    "SECRET_KEY", "rocen_homesteady_dev_secret_change_in_production"
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7
LEGACY_SALT = "rocen_homesteady_salt_2024"


# ==========================================
# PASSWORD HASHING
# ==========================================

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a stored hash.
    Supports bcrypt (new) and legacy SHA256+salt (Streamlit).
    """
    # Try bcrypt first
    if hashed_password.startswith(("$2b$", "$2a$", "$2y$")):
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception:
            return False

    # Fall back to legacy SHA256+salt (Streamlit compatibility)
    legacy = hashlib.sha256(
        f"{plain_password}{LEGACY_SALT}".encode()
    ).hexdigest()
    return hashed_password == legacy


def is_legacy_hash(hashed_password: str) -> bool:
    """Check if a hash is a legacy SHA256 hash (not bcrypt)."""
    return not hashed_password.startswith(("$2b$", "$2a$", "$2y$"))


# ==========================================
# JWT TOKENS
# ==========================================

def create_access_token(username: str) -> str:
    """Create a JWT access token for a user."""
    expire = datetime.now(timezone.utc) + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    payload = {"sub": username, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str) -> Optional[dict]:
    """Verify a JWT access token. Returns payload dict or None."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


# ==========================================
# USER OPERATIONS
# ==========================================

async def get_user(username: str) -> Optional[dict]:
    """Get a user from the database by username."""
    if not db.pool:
        return None
    try:
        async with db.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT username, hashed_password, is_active, created_at, last_login "
                "FROM users WHERE username=$1",
                username,
            )
            if row:
                return dict(row)
            return None
    except Exception as e:
        print(f"Get User Error: {e}")
        return None


async def sign_up(username: str, password: str) -> Tuple[bool, str]:
    """Register a new user. Returns (success, message)."""
    if not username or not password:
        return False, "Please fill in all fields."
    if len(username) < 3:
        return False, "Username must be at least 3 characters."
    if len(password) < 4:
        return False, "Password must be at least 4 characters."
    if " " in username:
        return False, "Username cannot contain spaces."

    if not db.pool:
        return False, "Database unavailable. Please try again later."

    try:
        async with db.pool.acquire() as conn:
            # Check if user exists
            existing = await conn.fetchval(
                "SELECT username FROM users WHERE username=$1",
                username,
            )
            if existing:
                return False, "That username is already taken. Try a different one!"

            # Insert new user with bcrypt hash
            hashed_pw = hash_password(password)
            created_at = datetime.now(timezone.utc).isoformat()
            await conn.execute(
                "INSERT INTO users (username, hashed_password, is_active, created_at) "
                "VALUES ($1, $2, $3, $4)",
                username, hashed_pw, True, created_at,
            )

        return True, "Account created! You can now log in."
    except Exception as e:
        print(f"Sign Up Error: {e}")
        return False, "Something went wrong. Please try again."


async def log_in(username: str, password: str) -> Tuple[bool, dict]:
    """
    Authenticate a user and return a JWT token.
    Migrates legacy SHA256 passwords to bcrypt on successful login.
    Returns (success, {token, username} or {error}).
    """
    if not username or not password:
        return False, {"error": "Please fill in all fields."}

    if not db.pool:
        return False, {"error": "Database unavailable. Please try again later."}

    try:
        async with db.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT username, hashed_password, is_active FROM users WHERE username=$1",
                username,
            )

            if not row:
                return False, {"error": "Invalid username or password."}

            db_username = row["username"]
            db_hash = row["hashed_password"]
            db_active = row["is_active"]

            if not db_active:
                return False, {"error": "Account is disabled. Contact support."}

            # Verify password (supports bcrypt and legacy SHA256)
            if not verify_password(password, db_hash):
                return False, {"error": "Invalid username or password."}

            # Migrate legacy SHA256 hash to bcrypt
            if is_legacy_hash(db_hash):
                new_hash = hash_password(password)
                await conn.execute(
                    "UPDATE users SET hashed_password=$1 WHERE username=$2",
                    new_hash, username,
                )

            # Update last login
            last_login = datetime.now(timezone.utc).isoformat()
            await conn.execute(
                "UPDATE users SET last_login=$1 WHERE username=$2",
                last_login, username,
            )

        # Create JWT token
        token = create_access_token(username)
        return True, {"token": token, "username": username}

    except Exception as e:
        print(f"Login Error: {e}")
        return False, {"error": "Something went wrong. Please try again."}


# ==========================================
# FASTAPI DEPENDENCY
# ==========================================

async def get_current_user(request) -> Optional[dict]:
    """
    FastAPI dependency. Returns user dict if JWT cookie is valid, else None.
    Does NOT hit the database — just decodes the token.
    """
    token = request.cookies.get("access_token")
    if not token:
        return None

    payload = verify_access_token(token)
    if not payload:
        return None

    username = payload.get("sub")
    if not username:
        return None

    return {"username": username}
