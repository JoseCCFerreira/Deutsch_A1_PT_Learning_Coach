from __future__ import annotations

import random
import sqlite3

import pandas as pd


def load_exercises(conn: sqlite3.Connection, grammar_topic: str | None = None, vocabulary_topic: str | None = None) -> pd.DataFrame:
    sql = "SELECT * FROM exercises WHERE 1=1"
    params: list[str] = []
    if grammar_topic:
        sql += " AND grammar_topic = ?"
        params.append(grammar_topic)
    if vocabulary_topic:
        sql += " AND vocabulary_topic = ?"
        params.append(vocabulary_topic)
    sql += " ORDER BY RANDOM() LIMIT 50"
    return pd.read_sql_query(sql, conn, params=params)


def generate_article_exercise(vocab_row: dict) -> dict:
    return {
        "exercise_id": -int(vocab_row["vocab_id"]),
        "exercise_type": "article_choice",
        "prompt_pt": f"Escolhe o artigo correto para '{vocab_row['german']}'.",
        "prompt_de": vocab_row["german"],
        "correct_answer": vocab_row["article"],
        "options": "der|die|das",
        "explanation_pt": f"'{vocab_row['german']}' usa {vocab_row['article']}. Aprende sempre artigo + palavra.",
        "grammar_topic": "Artigos der die das",
        "vocabulary_topic": vocab_row["topic"],
        "difficulty": vocab_row["difficulty"],
    }


def generate_dynamic_exercise(conn: sqlite3.Connection, weak_topic: str | None = None) -> dict:
    if weak_topic:
        df = load_exercises(conn, vocabulary_topic=weak_topic)
        if not df.empty:
            return df.iloc[0].to_dict()
    nouns = pd.read_sql_query("SELECT * FROM vocabulary WHERE article IN ('der','die','das') ORDER BY RANDOM() LIMIT 1", conn)
    if not nouns.empty:
        return generate_article_exercise(nouns.iloc[0].to_dict())
    exercises = load_exercises(conn)
    if exercises.empty:
        raise ValueError("Não há exercícios disponíveis.")
    return exercises.iloc[0].to_dict()


def options_for(exercise: dict) -> list[str]:
    raw = exercise.get("options", "") or ""
    if raw:
        return [part.strip() for part in raw.split("|") if part.strip()]
    distractors = ["Ich komme aus Portugal.", "Ich wohne in Braga.", "Danke.", "Guten Morgen."]
    return random.sample(distractors, min(4, len(distractors)))
