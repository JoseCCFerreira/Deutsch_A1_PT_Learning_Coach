from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from .schema import SQLITE_SCHEMA
from .utils import DB_PATH, ensure_dirs, now_iso


def connect(path: str | Path = DB_PATH) -> sqlite3.Connection:
    ensure_dirs()
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def create_schema(conn: sqlite3.Connection) -> None:
    for statement in SQLITE_SCHEMA:
        conn.execute(statement)
    conn.commit()


def ensure_default_user(conn: sqlite3.Connection, name: str = "Carlos") -> int:
    row = conn.execute("SELECT user_id FROM user_profile ORDER BY user_id LIMIT 1").fetchone()
    if row:
        return int(row["user_id"])
    cur = conn.execute(
        "INSERT INTO user_profile(name, native_language, target_language, current_level, created_at) VALUES (?, 'Portuguese', 'German', 'A1', ?)",
        (name, now_iso()),
    )
    conn.commit()
    return int(cur.lastrowid)


def query_df(conn: sqlite3.Connection, sql: str, params: tuple = ()) -> pd.DataFrame:
    return pd.read_sql_query(sql, conn, params=params)


def init_database() -> int:
    with connect() as conn:
        create_schema(conn)
        return ensure_default_user(conn)
