from __future__ import annotations

import sqlite3

import pandas as pd


def mastery_status(score: float) -> str:
    if score <= 30:
        return "Fraco"
    if score <= 60:
        return "Em desenvolvimento"
    if score <= 80:
        return "Bom"
    return "Forte"


def recommend_next(conn: sqlite3.Connection, user_id: int = 1) -> dict:
    mastery = pd.read_sql_query("SELECT * FROM mastery_state WHERE user_id=?", conn, params=(user_id,))
    due = pd.read_sql_query(
        "SELECT COUNT(*) AS due_count FROM review_queue WHERE user_id=? AND datetime(due_date) <= datetime('now')",
        conn,
        params=(user_id,),
    )["due_count"].iloc[0]
    attempts = pd.read_sql_query("SELECT * FROM user_attempts WHERE user_id=? ORDER BY created_at DESC LIMIT 50", conn, params=(user_id,))
    if mastery.empty:
        return {
            "lesson": "Cumprimentos",
            "grammar_topic": "Verbo sein",
            "vocabulary_topic": "cumprimentos",
            "exercise_type": "multiple_choice",
            "difficulty": 1,
            "reason": "Ainda não há histórico. Começa pelos primeiros passos.",
            "due_reviews": int(due),
        }
    weakest = mastery.sort_values(["mastery_score", "attempts"]).iloc[0]
    acc = attempts["is_correct"].mean() if not attempts.empty else 0
    difficulty = 2 if acc >= 0.8 else 1
    if acc < 0.5:
        difficulty = 1
    return {
        "lesson": "Treino adaptativo",
        "grammar_topic": weakest["topic_name"] if weakest["topic_type"] == "grammar" else "Artigos der die das",
        "vocabulary_topic": weakest["topic_name"] if weakest["topic_type"] == "vocabulary" else "pessoal",
        "exercise_type": _weak_error_type(attempts),
        "difficulty": difficulty,
        "reason": f"O tópico mais fraco é '{weakest['topic_name']}' com domínio {weakest['mastery_score']:.0f}/100.",
        "due_reviews": int(due),
    }


def _weak_error_type(attempts: pd.DataFrame) -> str:
    if attempts.empty or attempts["error_type"].dropna().empty:
        return "article_choice"
    errors = attempts[attempts["is_correct"] == 0]
    if errors.empty:
        return "translation_pt_de"
    return errors["error_type"].value_counts().idxmax()
