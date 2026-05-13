from __future__ import annotations

import sqlite3

import pandas as pd


def load_grammar_topics(conn: sqlite3.Connection) -> pd.DataFrame:
    return pd.read_sql_query("SELECT * FROM grammar_topics ORDER BY difficulty, topic_name", conn)


def get_topic(conn: sqlite3.Connection, topic_name: str) -> pd.Series | None:
    df = pd.read_sql_query("SELECT * FROM grammar_topics WHERE topic_name = ?", conn, params=(topic_name,))
    return None if df.empty else df.iloc[0]
