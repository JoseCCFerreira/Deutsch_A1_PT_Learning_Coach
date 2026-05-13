from __future__ import annotations

import sqlite3

import pandas as pd


def load_vocabulary(conn: sqlite3.Connection, topic: str | None = None, article: str | None = None) -> pd.DataFrame:
    sql = "SELECT * FROM vocabulary WHERE 1=1"
    params: list[str] = []
    if topic and topic != "Todos":
        sql += " AND topic = ?"
        params.append(topic)
    if article and article != "Todos":
        sql += " AND article = ?"
        params.append(article)
    sql += " ORDER BY difficulty, topic, german"
    return pd.read_sql_query(sql, conn, params=params)


def article_badge(article: str) -> str:
    colors = {"der": "#2563eb", "die": "#db2777", "das": "#047857"}
    color = colors.get(article, "#64748b")
    return f"<span style='background:{color};color:white;padding:4px 8px;border-radius:6px;font-weight:800'>{article or 'sem artigo'}</span>"


def mark_word(conn: sqlite3.Connection, user_id: int, vocab_id: int, result: str) -> None:
    score = 85 if result == "known" else 35
    conn.execute(
        """
        INSERT INTO mastery_state(user_id, topic_type, topic_name, mastery_score, attempts, correct_attempts, last_practiced, next_review)
        SELECT ?, 'vocabulary', german, ?, 1, ?, datetime('now'), datetime('now', '+1 day')
        FROM vocabulary WHERE vocab_id = ?
        ON CONFLICT(user_id, topic_type, topic_name) DO UPDATE SET
          mastery_score=excluded.mastery_score,
          attempts=mastery_state.attempts + 1,
          correct_attempts=mastery_state.correct_attempts + excluded.correct_attempts,
          last_practiced=datetime('now'),
          next_review=datetime('now', '+1 day')
        """,
        (user_id, score, 1 if result == "known" else 0, vocab_id),
    )
    conn.commit()
