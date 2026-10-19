"""Small SQLite persistence layer for MigrationMatch.

The UI remains session-first for fast interactions, while users, saved cities,
and recommendation searches are persisted between Streamlit reruns.
"""
from __future__ import annotations

import hashlib
import hmac
import sqlite3
from pathlib import Path
from typing import Any


DB_PATH = Path(__file__).resolve().parent / "migrationmatch.db"


def _connect() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db() -> None:
    with _connect() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                email TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                role TEXT NOT NULL,
                skill TEXT,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS saved_cities (
                email TEXT NOT NULL,
                city TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (email, city),
                FOREIGN KEY (email) REFERENCES users(email) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS recommendation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                skill TEXT NOT NULL,
                region TEXT,
                top_city TEXT,
                top_score REAL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (email) REFERENCES users(email) ON DELETE CASCADE
            );
            """
        )


def hash_password(password: str) -> str:
    return hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), b"migrationmatch-v1", 120_000
    ).hex()


def verify_password(password: str, password_hash: str) -> bool:
    return hmac.compare_digest(hash_password(password), password_hash)


def seed_demo_users() -> None:
    demo_users = [
        ("jasleen@gmail.com", "Jasleen Kaur", "Verified User", "Electrician", "password"),
    ]
    with _connect() as connection:
        connection.execute("DELETE FROM users WHERE email = ?", ("ramesh@example.com",))
        for email, name, role, skill, password in demo_users:
            connection.execute(
                """
                INSERT OR IGNORE INTO users (email, name, role, skill, password_hash)
                VALUES (?, ?, ?, ?, ?)
                """,
                (email, name, role, skill, hash_password(password)),
            )


def load_users() -> dict[str, dict[str, Any]]:
    with _connect() as connection:
        rows = connection.execute(
            "SELECT email, name, role, skill, password_hash FROM users"
        ).fetchall()
    return {
        row["email"]: {
            "name": row["name"],
            "role": row["role"],
            "skill": row["skill"],
            "password_hash": row["password_hash"],
        }
        for row in rows
    }


def save_user(email: str, name: str, role: str, skill: str, password: str) -> None:
    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO users (email, name, role, skill, password_hash)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(email) DO UPDATE SET
                name = excluded.name,
                role = excluded.role,
                skill = excluded.skill,
                password_hash = excluded.password_hash
            """,
            (email.strip().lower(), name.strip(), role, skill, hash_password(password)),
        )


def load_saved_cities(email: str, fallback: list[str] | None = None) -> list[str]:
    with _connect() as connection:
        rows = connection.execute(
            "SELECT city FROM saved_cities WHERE email = ? ORDER BY created_at",
            (email,),
        ).fetchall()
    return [row["city"] for row in rows] or list(fallback or [])


def set_saved_city(email: str, city: str, saved: bool) -> None:
    with _connect() as connection:
        if saved:
            connection.execute(
                "INSERT OR IGNORE INTO saved_cities (email, city) VALUES (?, ?)",
                (email, city),
            )
        else:
            connection.execute(
                "DELETE FROM saved_cities WHERE email = ? AND city = ?",
                (email, city),
            )


def save_recommendation(
    email: str, skill: str, region: str | None, top_city: str, top_score: float
) -> None:
    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO recommendation_history (email, skill, region, top_city, top_score)
            VALUES (?, ?, ?, ?, ?)
            """,
            (email, skill, region, top_city, float(top_score)),
        )
