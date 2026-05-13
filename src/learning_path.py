from __future__ import annotations

import sqlite3

import pandas as pd


def load_lessons(conn: sqlite3.Connection) -> pd.DataFrame:
    return pd.read_sql_query("SELECT * FROM lessons ORDER BY order_index", conn)


def recommended_lesson(conn: sqlite3.Connection) -> dict:
    lessons = load_lessons(conn)
    if lessons.empty:
        return {"title_pt": "Primeiros passos", "description_pt": "Começa por cumprimentos e apresentação."}
    return lessons.iloc[0].to_dict()
