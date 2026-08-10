"""
Game progress persistence for Rocen Homesteady.
Saves and loads game state to/from PostgreSQL using asyncpg.
Supports guest progress merge for seamless login experience.
"""

import json
from datetime import datetime, timezone
from typing import Optional

import db


# ==========================================
# SAVE / LOAD
# ==========================================

async def save_progress(username: str, data: dict) -> bool:
    """Save all game progress for a user. Upserts the entire blob."""
    if not db.pool:
        return False
    try:
        async with db.pool.acquire() as conn:
            last_saved = datetime.now(timezone.utc).isoformat()
            await conn.execute(
                """INSERT INTO saves (username, data, last_saved)
                   VALUES ($1, $2::jsonb, $3)
                   ON CONFLICT (username)
                   DO UPDATE SET data = EXCLUDED.data, last_saved = EXCLUDED.last_saved""",
                username, json.dumps(data), last_saved,
            )
        return True
    except Exception as e:
        print(f"Save Progress Error: {e}")
        return False


async def load_progress(username: str) -> Optional[dict]:
    """Load all game progress for a user. Returns None if no save exists."""
    if not db.pool:
        return None
    try:
        async with db.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT data FROM saves WHERE username=$1",
                username,
            )
            if row and row["data"]:
                # JSONB comes back as a dict automatically
                return dict(row["data"]) if isinstance(row["data"], dict) else row["data"]
            return None
    except Exception as e:
        print(f"Load Progress Error: {e}")
        return None


async def delete_progress(username: str) -> bool:
    """Delete all saved progress for a user."""
    if not db.pool:
        return False
    try:
        async with db.pool.acquire() as conn:
            await conn.execute(
                "DELETE FROM saves WHERE username=$1",
                username,
            )
        return True
    except Exception as e:
        print(f"Delete Progress Error: {e}")
        return False


# ==========================================
# GUEST PROGRESS MERGE
# ==========================================

def merge_progress(guest_data: dict, server_data: dict) -> dict:
    """
    Merge guest progress into server progress.
    For each field, keeps the "best" value:
    - Numbers: takes the max
    - Lists: takes the union (deduped)
    - Strings: keeps the longer one
    - Dicts: recurses
    - If only one side has a key, keeps it
    """
    merged = {}
    all_keys = set(list(guest_data.keys()) + list(server_data.keys()))

    for key in all_keys:
        guest_val = guest_data.get(key)
        server_val = server_data.get(key)

        if guest_val is None:
            merged[key] = server_val
            continue
        if server_val is None:
            merged[key] = guest_val
            continue

        merged[key] = _merge_values(guest_val, server_val)

    return merged


def _merge_values(guest_val, server_val):
    """Recursively merge two values, keeping the 'best' of each."""
    # Type mismatch — keep the server value as canonical
    if type(guest_val) != type(server_val):
        # Special case: int vs float are comparable
        if isinstance(guest_val, (int, float)) and isinstance(server_val, (int, float)):
            return max(guest_val, server_val)
        return server_val

    # Numbers: take the max
    if isinstance(guest_val, (int, float)):
        return max(guest_val, server_val)

    # Strings: keep the longer one
    if isinstance(guest_val, str):
        return guest_val if len(guest_val) >= len(server_val) else server_val

    # Booleans: True wins
    if isinstance(guest_val, bool):
        return guest_val or server_val

    # Lists: union, preserving order
    if isinstance(guest_val, list):
        seen = set()
        result = []
        for item in guest_val + server_val:
            key = json.dumps(item, sort_keys=True) if isinstance(item, (dict, list)) else str(item)
            if key not in seen:
                seen.add(key)
                result.append(item)
        return result

    # Dicts: recurse
    if isinstance(guest_val, dict):
        return merge_progress(guest_val, server_val)

    # Default: keep server
    return server_val


async def merge_and_save(username: str, guest_data: dict) -> Optional[dict]:
    """
    Load server data, merge with guest data, save result.
    Uses a transaction with row lock to prevent race conditions.
    Returns the merged data, or None on failure.
    """
    if not db.pool:
        return None
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                # Lock the row to prevent concurrent merges
                row = await conn.fetchrow(
                    "SELECT data FROM saves WHERE username=$1 FOR UPDATE",
                    username,
                )
                server_data = dict(row["data"]) if (row and row["data"]) else {}

                merged = merge_progress(guest_data, server_data)
                last_saved = datetime.now(timezone.utc).isoformat()

                await conn.execute(
                    """INSERT INTO saves (username, data, last_saved)
                       VALUES ($1, $2::jsonb, $3)
                       ON CONFLICT (username)
                       DO UPDATE SET data = EXCLUDED.data, last_saved = EXCLUDED.last_saved""",
                    username, json.dumps(merged), last_saved,
                )

        return merged
    except Exception as e:
        print(f"Merge Progress Error: {e}")
        return None
