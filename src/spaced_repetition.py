from __future__ import annotations

import sqlite3
from datetime import datetime, timedelta

import pandas as pd


QUALITY = {"Não sabia": 0, "Difícil": 3, "Médio": 4, "Fácil": 5}


def schedule_sm2(ease_factor: float, interval_days: int, repetitions: int, result_label: str) -> dict:
    quality = QUALITY.get(result_label, 0)
    if quality < 3:
        repetitions = 0
        interval_days = 1
    else:
        repetitions += 1
        if repetitions == 1:
            interval_days = 1
        elif repetitions == 2:
            interval_days = 6
        else:
            interval_days = max(1, round(interval_days * ease_factor))
    ease_factor = max(1.3, ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))
    due_date = datetime.now() + timedelta(days=interval_days)
    return {
        "ease_factor": round(ease_factor, 2),
        "interval_days": interval_days,
        "repetitions": repetitions,
        "due_date": due_date.isoformat(timespec="seconds"),
        "last_result": result_label,
    }


def due_reviews(conn: sqlite3.Connection, user_id: int = 1) -> pd.DataFrame:
    return pd.read_sql_query(
        """
        SELECT r.*, v.german, v.portuguese, v.article, v.example_de, v.example_pt, v.topic
        FROM review_queue r
        LEFT JOIN vocabulary v ON r.item_type='vocabulary' AND r.item_id=v.vocab_id
        WHERE r.user_id=? AND datetime(r.due_date) <= datetime('now')
        ORDER BY r.due_date
        """,
        conn,
        params=(user_id,),
    )


def update_review(conn: sqlite3.Connection, review_id: int, result_label: str) -> None:
    row = conn.execute("SELECT * FROM review_queue WHERE review_id=?", (review_id,)).fetchone()
    if not row:
        return
    updated = schedule_sm2(row["ease_factor"], row["interval_days"], row["repetitions"], result_label)
    conn.execute(
        """
        UPDATE review_queue SET ease_factor=?, interval_days=?, repetitions=?, due_date=?, last_result=?
        WHERE review_id=?
        """,
        (
            updated["ease_factor"],
            updated["interval_days"],
            updated["repetitions"],
            updated["due_date"],
            updated["last_result"],
            review_id,
        ),
    )
    conn.commit()
