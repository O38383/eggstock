"""
oauth_db.py - Hybrid SQLite & Supabase storage engine for Discord OAuth2 authorized members.
Tracks connected users, access/refresh tokens, and join status.
Supports dual-write and fallback caching: SQLite local cache + Supabase cloud PostgreSQL.
"""

import sqlite3
import os
import time
import json
import logging
import threading
import urllib.request
import urllib.parse
import urllib.error

log = logging.getLogger("eggstock.oauth_db")

DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DB_PATH = os.path.join(DB_DIR, "oauth_members.db")

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://mtymdgujtauyqupjdcsr.supabase.co").rstrip("/")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", os.environ.get("SUPABASE_KEY", "")).strip()


def _is_supabase_enabled() -> bool:
    """Check if Supabase credentials are configured."""
    return bool(SUPABASE_URL and SUPABASE_KEY)


def _supabase_request(endpoint: str, method: str = "GET", data: dict | list | None = None, prefer: str | None = None) -> tuple[int, any]:
    """Execute an HTTP request against the Supabase PostgREST API."""
    if not _is_supabase_enabled():
        return 0, None
    url = f"{SUPABASE_URL}/rest/v1/{endpoint}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
    }
    if prefer:
        headers["Prefer"] = prefer

    body = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=5.0) as resp:
            status = resp.status
            content = resp.read().decode("utf-8")
            if content:
                try:
                    return status, json.loads(content)
                except Exception:
                    return status, content
            return status, None
    except urllib.error.HTTPError as he:
        err_msg = he.read().decode("utf-8", errors="ignore")
        log.warning(f"[oauth_db] Supabase HTTP {he.code} on {method} {endpoint}: {err_msg}")
        return he.code, None
    except Exception as exc:
        log.warning(f"[oauth_db] Supabase request error on {method} {endpoint}: {exc}")
        return 0, None


def _bg_task(fn, *args):
    """Run a sync function in a background daemon thread so HTTP calls never block."""
    t = threading.Thread(target=fn, args=args, daemon=True)
    t.start()


def _sync_user_to_supabase(user_record: dict):
    """Upsert OAuth user into Supabase."""
    try:
        payload = {
            "user_id": str(user_record.get("user_id")),
            "username": user_record.get("username", "Unknown"),
            "discriminator": user_record.get("discriminator", "0"),
            "avatar": user_record.get("avatar") or "",
            "access_token": user_record.get("access_token", ""),
            "refresh_token": user_record.get("refresh_token", ""),
            "expires_at": int(user_record.get("expires_at", 0)),
            "scope": user_record.get("scope", "identify guilds.join"),
            "joined_guild": bool(user_record.get("joined_guild")),
            "last_seen_at": user_record.get("last_seen_at") or time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "ip_hash": user_record.get("ip_hash", "")
        }
        status, _ = _supabase_request(
            "oauth_users?on_conflict=user_id",
            method="POST",
            data=payload,
            prefer="resolution=merge-duplicates,return=minimal"
        )
        if status in (200, 201, 204):
            log.info(f"[oauth_db] Synced user {payload['user_id']} ({payload['username']}) to Supabase")
        else:
            log.warning(f"[oauth_db] Failed to sync user {payload['user_id']} to Supabase: status {status}")
    except Exception as exc:
        log.error(f"[oauth_db] Error in _sync_user_to_supabase: {exc}")


def _sync_session_to_supabase(session_record: dict):
    """Upsert user session into Supabase."""
    try:
        payload = {
            "session_token": session_record.get("session_token"),
            "user_id": str(session_record.get("user_id")),
            "username": session_record.get("username", "Member"),
            "raw_username": session_record.get("raw_username", ""),
            "avatar_url": session_record.get("avatar_url", ""),
            "joined_guild": bool(session_record.get("joined_guild")),
            "created_at": float(session_record.get("created_at", time.time())),
            "expires_at": float(session_record.get("expires_at", 0))
        }
        status, _ = _supabase_request(
            "user_sessions?on_conflict=session_token",
            method="POST",
            data=payload,
            prefer="resolution=merge-duplicates,return=minimal"
        )
        if status in (200, 201, 204):
            log.info(f"[oauth_db] Synced session for user {payload['user_id']} to Supabase")
        else:
            log.warning(f"[oauth_db] Failed to sync session to Supabase: status {status}")
    except Exception as exc:
        log.error(f"[oauth_db] Error in _sync_session_to_supabase: {exc}")


def _delete_session_from_supabase(session_token: str):
    """Delete session from Supabase."""
    try:
        encoded = urllib.parse.quote(session_token)
        _supabase_request(f"user_sessions?session_token=eq.{encoded}", method="DELETE")
    except Exception as exc:
        log.error(f"[oauth_db] Error in _delete_session_from_supabase: {exc}")


def _cache_session_to_sqlite(session_token: str, user_info: dict, expires_at: float):
    """Helper to write a retrieved Supabase session back into local SQLite cache."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO user_sessions (
                    session_token, user_id, username, raw_username, avatar_url, joined_guild, created_at, expires_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session_token,
                str(user_info.get("user_id")),
                user_info.get("username", "Member"),
                user_info.get("raw_username", ""),
                user_info.get("avatar_url", ""),
                1 if user_info.get("joined_guild") else 0,
                user_info.get("created_at", time.time()),
                expires_at
            ))
            conn.commit()
    except Exception as exc:
        log.error(f"[oauth_db] Error caching session to SQLite: {exc}")


def _fetch_session_from_supabase(session_token: str) -> dict | None:
    """Fetch unexpired session from Supabase when not present in local SQLite cache."""
    if not _is_supabase_enabled():
        return None
    try:
        now = time.time()
        encoded = urllib.parse.quote(session_token)
        status, data = _supabase_request(
            f"user_sessions?session_token=eq.{encoded}&expires_at=gt.{now}&select=*"
        )
        if status == 200 and isinstance(data, list) and len(data) > 0:
            row = data[0]
            session_info = {
                "user_id": row["user_id"],
                "username": row["username"],
                "raw_username": row.get("raw_username", ""),
                "avatar_url": row.get("avatar_url", ""),
                "joined_guild": bool(row.get("joined_guild")),
                "created_at": float(row.get("created_at", now)),
            }
            # Cache locally into SQLite for fast subsequent lookups
            _cache_session_to_sqlite(session_token, session_info, float(row.get("expires_at", now + 86400)))
            return session_info
    except Exception as exc:
        log.error(f"[oauth_db] Error fetching session from Supabase: {exc}")
    return None


def migrate_sqlite_to_supabase():
    """Migrate any existing SQLite records to Supabase."""
    if not _is_supabase_enabled():
        return
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM oauth_users")
            users = [dict(r) for r in cursor.fetchall()]
            cursor.execute("SELECT * FROM user_sessions WHERE expires_at > ?", (time.time(),))
            sessions = [dict(r) for r in cursor.fetchall()]

        for u in users:
            _sync_user_to_supabase(u)
        for s in sessions:
            _sync_session_to_supabase(s)

        if users or sessions:
            log.info(f"[oauth_db] Migrated {len(users)} users and {len(sessions)} sessions from SQLite to Supabase")
    except Exception as exc:
        log.error(f"[oauth_db] Migration error: {exc}")


def init_db():
    """Initialize the SQLite database schema if not present and trigger cloud sync."""
    os.makedirs(DB_DIR, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS oauth_users (
                user_id TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                discriminator TEXT DEFAULT '0',
                avatar TEXT,
                access_token TEXT NOT NULL,
                refresh_token TEXT NOT NULL,
                expires_at INTEGER NOT NULL,
                scope TEXT DEFAULT 'identify guilds.join',
                joined_guild INTEGER DEFAULT 0,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ip_hash TEXT
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_oauth_joined ON oauth_users(joined_guild)
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS user_sessions (
                session_token TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                username TEXT NOT NULL,
                raw_username TEXT,
                avatar_url TEXT,
                joined_guild INTEGER DEFAULT 1,
                created_at REAL NOT NULL,
                expires_at REAL NOT NULL
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_sessions_token ON user_sessions(session_token)
        """)
        conn.commit()
    log.info(f"[oauth_db] Database initialized at {DB_PATH}")

    # If Supabase is enabled, perform background migration of any un-synced data
    if _is_supabase_enabled():
        log.info("[oauth_db] Supabase integration active. Starting background sync...")
        _bg_task(migrate_sqlite_to_supabase)


def save_oauth_user(user_data: dict, token_data: dict, joined_guild: bool = True, ip_hash: str = "") -> bool:
    """Save or update an authorized OAuth user (writes to SQLite and background syncs to Supabase)."""
    try:
        user_id = str(user_data.get("id"))
        username = user_data.get("username", "Unknown")
        discriminator = user_data.get("discriminator", "0")
        avatar = user_data.get("avatar") or ""
        access_token = token_data.get("access_token", "")
        refresh_token = token_data.get("refresh_token", "")
        expires_in = int(token_data.get("expires_in", 604800))
        expires_at = int(time.time()) + expires_in
        scope = token_data.get("scope", "identify guilds.join")
        now_iso = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        now_iso_z = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        # 1. Update SQLite locally first
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("""
                INSERT INTO oauth_users (
                    user_id, username, discriminator, avatar,
                    access_token, refresh_token, expires_at, scope,
                    joined_guild, last_seen_at, ip_hash
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    username=excluded.username,
                    discriminator=excluded.discriminator,
                    avatar=excluded.avatar,
                    access_token=excluded.access_token,
                    refresh_token=excluded.refresh_token,
                    expires_at=excluded.expires_at,
                    joined_guild=MAX(oauth_users.joined_guild, excluded.joined_guild),
                    last_seen_at=excluded.last_seen_at,
                    ip_hash=excluded.ip_hash
            """, (
                user_id, username, discriminator, avatar,
                access_token, refresh_token, expires_at, scope,
                1 if joined_guild else 0, now_iso, ip_hash
            ))
            conn.commit()

        # 2. Asynchronously sync to Supabase
        if _is_supabase_enabled():
            _bg_task(_sync_user_to_supabase, {
                "user_id": user_id,
                "username": username,
                "discriminator": discriminator,
                "avatar": avatar,
                "access_token": access_token,
                "refresh_token": refresh_token,
                "expires_at": expires_at,
                "scope": scope,
                "joined_guild": joined_guild,
                "last_seen_at": now_iso_z,
                "ip_hash": ip_hash
            })

        return True
    except Exception as exc:
        log.error(f"[oauth_db] Error saving OAuth user: {exc}")
        return False


def get_oauth_user(user_id: str) -> dict | None:
    """Retrieve an authorized user by user ID."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM oauth_users WHERE user_id = ?", (str(user_id),))
            row = cursor.fetchone()
            if row:
                return dict(row)
    except Exception as exc:
        log.error(f"[oauth_db] Error fetching user {user_id}: {exc}")
    return None


def get_oauth_stats() -> dict:
    """Get total count of authorized users and joined guild members."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*), SUM(joined_guild) FROM oauth_users")
            total, joined = cursor.fetchone()
            return {
                "total_authorized": total or 0,
                "joined_guild": joined or 0
            }
    except Exception as exc:
        log.error(f"[oauth_db] Error fetching stats: {exc}")
        return {"total_authorized": 0, "joined_guild": 0}


def save_session(session_token: str, user_info: dict, max_age_days: int = 30):
    """Save an active user session to persistent database (writes to SQLite and background syncs to Supabase)."""
    try:
        now = time.time()
        expires_at = now + (max_age_days * 86400)

        # 1. Save to SQLite locally
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO user_sessions (
                    session_token, user_id, username, raw_username, avatar_url, joined_guild, created_at, expires_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session_token,
                str(user_info.get("user_id")),
                user_info.get("username", "Member"),
                user_info.get("raw_username", ""),
                user_info.get("avatar_url", ""),
                1 if user_info.get("joined_guild") else 0,
                user_info.get("created_at", now),
                expires_at
            ))
            conn.commit()

        # 2. Asynchronously sync to Supabase
        if _is_supabase_enabled():
            _bg_task(_sync_session_to_supabase, {
                "session_token": session_token,
                "user_id": user_info.get("user_id"),
                "username": user_info.get("username", "Member"),
                "raw_username": user_info.get("raw_username", ""),
                "avatar_url": user_info.get("avatar_url", ""),
                "joined_guild": user_info.get("joined_guild"),
                "created_at": user_info.get("created_at", now),
                "expires_at": expires_at
            })
    except Exception as exc:
        log.error(f"[oauth_db] Error saving session: {exc}")


def get_session(session_token: str) -> dict | None:
    """Retrieve an active unexpired user session from local SQLite or Supabase cloud database."""
    try:
        now = time.time()
        # 1. Check local SQLite cache first (fastest)
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_sessions WHERE session_token = ? AND expires_at > ?", (session_token, now))
            row = cursor.fetchone()
            if row:
                return {
                    "user_id": row["user_id"],
                    "username": row["username"],
                    "raw_username": row["raw_username"],
                    "avatar_url": row["avatar_url"],
                    "joined_guild": bool(row["joined_guild"]),
                    "created_at": row["created_at"],
                }

        # 2. Fallback to Supabase cloud database if not found locally
        return _fetch_session_from_supabase(session_token)
    except Exception as exc:
        log.error(f"[oauth_db] Error fetching session: {exc}")
    return None


def delete_session(session_token: str):
    """Delete a user session upon logout (from both SQLite and Supabase)."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("DELETE FROM user_sessions WHERE session_token = ?", (session_token,))
            conn.commit()

        if _is_supabase_enabled():
            _bg_task(_delete_session_from_supabase, session_token)
    except Exception as exc:
        log.error(f"[oauth_db] Error deleting session: {exc}")
