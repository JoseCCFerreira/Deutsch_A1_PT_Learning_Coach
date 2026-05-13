from __future__ import annotations

import sqlite3

import pandas as pd


def progress_summary(conn: sqlite3.Connection, user_id: int = 1) -> dict:
    attempts = pd.read_sql_query("SELECT * FROM user_attempts WHERE user_id=?", conn, params=(user_id,))
    mastery = pd.read_sql_query("SELECT * FROM mastery_state WHERE user_id=?", conn, params=(user_id,))
    vocab_count = pd.read_sql_query("SELECT COUNT(*) AS n FROM vocabulary", conn)["n"].iloc[0]
    learned = len(mastery[(mastery["topic_type"] == "vocabulary") & (mastery["mastery_score"] >= 60)]) if not mastery.empty else 0
    due = pd.read_sql_query(
        "SELECT COUNT(*) AS n FROM review_queue WHERE user_id=? AND datetime(due_date) <= datetime('now')",
        conn,
        params=(user_id,),
    )["n"].iloc[0]
    accuracy = attempts["is_correct"].mean() if not attempts.empty else 0
    overall = min(100, round((accuracy * 45) + (learned / max(vocab_count, 1) * 35) + (min(len(attempts), 100) / 100 * 20)))
    weakest_grammar = _weakest(mastery, "grammar")
    weakest_vocab = _weakest(mastery, "vocabulary")
    return {
        "overall_progress": overall,
        "vocabulary_total": int(vocab_count),
        "vocabulary_learned": int(learned),
        "due_reviews": int(due),
        "accuracy": float(accuracy or 0),
        "attempts": int(len(attempts)),
        "weakest_grammar": weakest_grammar,
        "weakest_vocabulary": weakest_vocab,
        "streak": study_streak(attempts),
    }


def accuracy_by(conn: sqlite3.Connection, column: str, user_id: int = 1) -> pd.DataFrame:
    allowed = {"grammar_topic", "vocabulary_topic", "exercise_type", "error_type"}
    if column not in allowed:
        raise ValueError("Coluna inválida.")
    return pd.read_sql_query(
        f"""
        SELECT {column} AS topic, COUNT(*) AS attempts, AVG(is_correct) AS accuracy
        FROM user_attempts
        WHERE user_id=? AND COALESCE({column}, '') <> ''
        GROUP BY {column}
        ORDER BY accuracy ASC, attempts DESC
        """,
        conn,
        params=(user_id,),
    )


def mastery_table(conn: sqlite3.Connection, user_id: int = 1) -> pd.DataFrame:
    return pd.read_sql_query("SELECT * FROM mastery_state WHERE user_id=? ORDER BY mastery_score", conn, params=(user_id,))


def progress_over_time(conn: sqlite3.Connection, user_id: int = 1) -> pd.DataFrame:
    return pd.read_sql_query(
        """
        SELECT date(created_at) AS day, COUNT(*) AS attempts, AVG(is_correct) AS accuracy
        FROM user_attempts
        WHERE user_id=?
        GROUP BY date(created_at)
        ORDER BY day
        """,
        conn,
        params=(user_id,),
    )


def _weakest(mastery: pd.DataFrame, topic_type: str) -> str:
    if mastery.empty:
        return "Ainda sem dados"
    subset = mastery[mastery["topic_type"] == topic_type]
    if subset.empty:
        return "Ainda sem dados"
    return str(subset.sort_values("mastery_score").iloc[0]["topic_name"])


def study_streak(attempts: pd.DataFrame) -> int:
    if attempts.empty:
        return 0
    days = pd.to_datetime(attempts["created_at"]).dt.date.drop_duplicates().sort_values(ascending=False).tolist()
    streak = 0
    today = pd.Timestamp.today().date()
    for day in days:
        if (today - day).days == streak:
            streak += 1
        elif (today - day).days > streak:
            break
    return streak
