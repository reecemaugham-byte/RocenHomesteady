"""
Database connection pool for Rocen Homesteady.
Uses asyncpg for non-blocking PostgreSQL access.
Shared pool across auth and progress modules.
"""

import os
import asyncpg

# Global connection pool — set by init_pool(), used by auth.py and progress.py
pool: asyncpg.Pool = None


async def init_pool() -> bool:
    """Create the connection pool. Call once at app startup."""
    global pool
    uri = os.environ.get("DATABASE_URL")
    if not uri:
        print("WARNING: DATABASE_URL not set — auth and progress features disabled")
        return False

    # asyncpg uses postgresql:// (not postgres://)
    if uri.startswith("postgres://"):
        uri = "postgresql://" + uri[len("postgres://"):]

    # Strip sslmode from query string — asyncpg handles SSL via parameter
    ssl_required = "sslmode=require" in uri
    uri = uri.replace("?sslmode=require", "").replace("&sslmode=require", "")

    try:
        pool = await asyncpg.create_pool(
            uri,
            ssl="require" if ssl_required else None,
            min_size=2,
            max_size=10,
        )
        print("Database pool connected")
        return True
    except Exception as e:
        print(f"DB Pool Error: {e}")
        return False


async def close_pool():
    """Close the connection pool. Call at app shutdown."""
    global pool
    if pool:
        await pool.close()
        pool = None
        print("Database pool closed")


async def create_tables():
    """Create or migrate database tables. Called after pool is ready."""
    global pool
    if not pool:
        return False

    async with pool.acquire() as conn:
        # Users table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                hashed_password TEXT,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TEXT,
                last_login TEXT
            )
        """)

        # Saves table — use JSONB for the data column
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS saves (
                username TEXT PRIMARY KEY,
                data JSONB,
                last_saved TEXT
            )
        """)

        # Migration: if data column was TEXT, convert to JSONB
        try:
            row = await conn.fetchrow("""
                SELECT data_type FROM information_schema.columns
                WHERE table_name = 'saves' AND column_name = 'data'
            """)
            if row and row["data_type"] == "text":
                await conn.execute("""
                    ALTER TABLE saves ALTER COLUMN data TYPE JSONB
                    USING CASE WHEN data IS NULL THEN NULL ELSE data::jsonb END
                """)
                print("Migrated saves.data from TEXT to JSONB")
        except Exception as e:
            print(f"Migration check (non-critical): {e}")

    print("Database tables ready")
    return True
