#!/usr/bin/env python3
"""SQLite-backed authentication helpers for OptiAppsCreator."""

from __future__ import annotations

import base64
import hashlib
import hmac
import os
import secrets
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:  # Keep runtime usable before dependencies are installed.
    def load_dotenv(*args, **kwargs):
        return False


SCRIPT_DIR = Path(__file__).resolve().parent
load_dotenv(SCRIPT_DIR / ".env")


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def utc_iso(dt: datetime | None = None) -> str:
    return (dt or utc_now()).isoformat()


def parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value)


def get_db_path() -> Path:
    configured = os.getenv("AUTH_DB_PATH", "data/users.db")
    path = Path(configured)
    if not path.is_absolute():
        path = SCRIPT_DIR / path
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def connect(db_path: str | Path | None = None) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path or get_db_path()))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path: str | Path | None = None) -> None:
    with connect(db_path) as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                initial_password_hash TEXT,
                must_change_password INTEGER NOT NULL DEFAULT 1,
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS login_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT NOT NULL,
                ip_address TEXT NOT NULL,
                success INTEGER NOT NULL,
                reason TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS password_reset_tokens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                token_hash TEXT NOT NULL UNIQUE,
                purpose TEXT NOT NULL,
                used INTEGER NOT NULL DEFAULT 0,
                expires_at TEXT NOT NULL,
                created_at TEXT NOT NULL,
                used_at TEXT,
                request_ip TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session_token_hash TEXT NOT NULL UNIQUE,
                ip_address TEXT,
                user_agent TEXT,
                created_at TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                revoked_at TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS user_projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                UNIQUE(user_id, name),
                FOREIGN KEY(user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS user_designs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                model TEXT NOT NULL,
                name TEXT NOT NULL,
                design_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                UNIQUE(project_id, model, name),
                FOREIGN KEY(project_id) REFERENCES user_projects(id) ON DELETE CASCADE
            );
            """
        )


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    iterations = 390000
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return "pbkdf2_sha256${}${}${}".format(
        iterations,
        base64.b64encode(salt).decode("ascii"),
        base64.b64encode(digest).decode("ascii"),
    )


def verify_password(password: str, password_hash: str | None) -> bool:
    if not password_hash:
        return False
    try:
        algorithm, iterations_s, salt_s, digest_s = password_hash.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        salt = base64.b64decode(salt_s)
        expected = base64.b64decode(digest_s)
        digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, int(iterations_s))
        return hmac.compare_digest(digest, expected)
    except Exception:
        return False


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def row_to_dict(row: sqlite3.Row | None) -> dict[str, Any] | None:
    return dict(row) if row else None


def get_user_by_username(username: str) -> dict[str, Any] | None:
    init_db()
    with connect() as conn:
        return row_to_dict(conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone())


def get_user_by_email(email: str) -> dict[str, Any] | None:
    init_db()
    with connect() as conn:
        return row_to_dict(conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone())


def upsert_user(username: str, email: str, password: str, db_path: str | Path | None = None) -> None:
    init_db(db_path)
    now = utc_iso()
    pwd_hash = hash_password(password)
    with connect(db_path) as conn:
        existing = conn.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email)).fetchone()
        if existing:
            conn.execute(
                """
                UPDATE users
                SET username = ?, email = ?, password_hash = ?, initial_password_hash = NULL,
                    must_change_password = 0, is_active = 1, updated_at = ?
                WHERE id = ?
                """,
                (username, email, pwd_hash, now, existing["id"]),
            )
        else:
            conn.execute(
                """
                INSERT INTO users (username, email, password_hash, initial_password_hash,
                                   must_change_password, is_active, created_at, updated_at)
                VALUES (?, ?, ?, NULL, 0, 1, ?, ?)
                """,
                (username, email, pwd_hash, now, now),
            )


def record_login(user_id: int | None, username: str, ip_address: str, success: bool, reason: str | None = None) -> None:
    init_db()
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO login_events (user_id, username, ip_address, success, reason, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, username, ip_address, 1 if success else 0, reason, utc_iso()),
        )


def create_reset_token(user_id: int, purpose: str, hours_valid: int, request_ip: str | None = None) -> str:
    init_db()
    token = secrets.token_urlsafe(32)
    with connect() as conn:
        conn.execute(
            """
            UPDATE password_reset_tokens
            SET used = 1, used_at = ?
            WHERE user_id = ? AND purpose = ? AND used = 0
            """,
            (utc_iso(), user_id, purpose),
        )
        conn.execute(
            """
            INSERT INTO password_reset_tokens
                (user_id, token_hash, purpose, used, expires_at, created_at, request_ip)
            VALUES (?, ?, ?, 0, ?, ?, ?)
            """,
            (user_id, hash_token(token), purpose, utc_iso(utc_now() + timedelta(hours=hours_valid)), utc_iso(), request_ip),
        )
    return token


def validate_reset_token(token: str) -> dict[str, Any] | None:
    init_db()
    with connect() as conn:
        row = conn.execute(
            """
            SELECT t.*, u.username, u.email
            FROM password_reset_tokens t
            JOIN users u ON u.id = t.user_id
            WHERE t.token_hash = ? AND t.used = 0
            """,
            (hash_token(token),),
        ).fetchone()
        data = row_to_dict(row)
        if not data or parse_dt(data["expires_at"]) <= utc_now():
            return None
        return data


def reset_password_with_token(token: str, new_password: str) -> bool:
    token_data = validate_reset_token(token)
    if not token_data:
        return False
    now = utc_iso()
    with connect() as conn:
        conn.execute(
            """
            UPDATE users
            SET password_hash = ?, initial_password_hash = NULL, must_change_password = 0, updated_at = ?
            WHERE id = ?
            """,
            (hash_password(new_password), now, token_data["user_id"]),
        )
        conn.execute(
            "UPDATE password_reset_tokens SET used = 1, used_at = ? WHERE id = ?",
            (now, token_data["id"]),
        )
        conn.execute(
            """
            UPDATE password_reset_tokens
            SET used = 1, used_at = ?
            WHERE user_id = ? AND used = 0
            """,
            (now, token_data["user_id"]),
        )
    return True


def create_session(user_id: int, ip_address: str | None, user_agent: str | None, hours_valid: int) -> str:
    init_db()
    token = secrets.token_urlsafe(32)
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO sessions (user_id, session_token_hash, ip_address, user_agent, created_at, expires_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, hash_token(token), ip_address, user_agent, utc_iso(), utc_iso(utc_now() + timedelta(hours=hours_valid))),
        )
    return token


def get_session_user(session_token: str | None) -> dict[str, Any] | None:
    if not session_token:
        return None
    init_db()
    with connect() as conn:
        row = conn.execute(
            """
            SELECT s.id AS session_id, s.expires_at, s.revoked_at,
                   u.id, u.username, u.email, u.is_active
            FROM sessions s
            JOIN users u ON u.id = s.user_id
            WHERE s.session_token_hash = ?
            """,
            (hash_token(session_token),),
        ).fetchone()
        data = row_to_dict(row)
        if not data or data["revoked_at"] or parse_dt(data["expires_at"]) <= utc_now() or not data["is_active"]:
            return None
        return data


def revoke_session(session_token: str | None) -> None:
    if not session_token:
        return
    init_db()
    with connect() as conn:
        conn.execute(
            "UPDATE sessions SET revoked_at = ? WHERE session_token_hash = ? AND revoked_at IS NULL",
            (utc_iso(), hash_token(session_token)),
        )
