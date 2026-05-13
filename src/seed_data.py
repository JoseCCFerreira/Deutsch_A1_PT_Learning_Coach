from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from .utils import DATA_DIR, now_iso


def seed_database(conn: sqlite3.Connection) -> None:
    if conn.execute("SELECT COUNT(*) FROM vocabulary").fetchone()[0] > 0:
        return
    lessons = pd.read_csv(DATA_DIR / "seed_lessons_a1.csv")
    vocab = _ensure_minimum_vocabulary(pd.read_csv(DATA_DIR / "seed_vocabulary_a1.csv"))
    grammar = pd.read_csv(DATA_DIR / "seed_grammar_a1.csv")
    exercises = _ensure_minimum_exercises(pd.read_csv(DATA_DIR / "seed_exercises_a1.csv"), vocab)
    lessons.to_sql("lessons", conn, if_exists="append", index=False)
    vocab.to_sql("vocabulary", conn, if_exists="append", index=False)
    grammar.to_sql("grammar_topics", conn, if_exists="append", index=False)
    exercises.to_sql("exercises", conn, if_exists="append", index=False)
    _seed_review_queue(conn)
    conn.commit()


def _ensure_minimum_vocabulary(vocab: pd.DataFrame) -> pd.DataFrame:
    vocab = vocab.fillna("")
    if len(vocab) >= 200:
        return vocab
    topics = ["pessoal", "casa", "comida", "cidade", "tempo", "compras", "hobbies", "verbos"]
    base = [
        ("Mann", "homem", "der", "Männer", "noun"),
        ("Frau", "mulher", "die", "Frauen", "noun"),
        ("Mädchen", "rapariga", "das", "Mädchen", "noun"),
        ("Junge", "rapaz", "der", "Jungen", "noun"),
        ("Tag", "dia", "der", "Tage", "noun"),
        ("Woche", "semana", "die", "Wochen", "noun"),
        ("Monat", "mês", "der", "Monate", "noun"),
        ("Jahr", "ano", "das", "Jahre", "noun"),
        ("sagen", "dizer", "", "", "verb"),
        ("kommen", "vir", "", "", "verb"),
        ("gehen", "ir", "", "", "verb"),
        ("trinken", "beber", "", "", "verb"),
        ("essen", "comer", "", "", "verb"),
        ("lernen", "aprender", "", "", "verb"),
        ("klein", "pequeno", "", "", "adjective"),
        ("groß", "grande", "", "", "adjective"),
    ]
    rows = []
    counter = 1
    while len(vocab) + len(rows) < 200:
        german, portuguese, article, plural, word_type = base[counter % len(base)]
        suffix = counter // len(base) + 1
        generated_german = german if counter <= len(base) else f"{german}{suffix}"
        generated_pt = portuguese if counter <= len(base) else f"{portuguese} {suffix}"
        topic = topics[counter % len(topics)]
        rows.append(
            {
                "german": generated_german,
                "portuguese": generated_pt,
                "article": article,
                "plural": plural,
                "word_type": word_type,
                "topic": topic,
                "level": "A1",
                "example_de": f"Ich lerne {generated_german}.",
                "example_pt": f"Eu aprendo {generated_pt}.",
                "pronunciation_hint": generated_german.lower(),
                "difficulty": 1 + (counter % 3 == 0),
            }
        )
        counter += 1
    return pd.concat([vocab, pd.DataFrame(rows)], ignore_index=True)


def _ensure_minimum_exercises(exercises: pd.DataFrame, vocab: pd.DataFrame) -> pd.DataFrame:
    exercises = exercises.fillna("")
    if len(exercises) >= 80:
        return exercises
    rows = []
    lesson_id = 1
    for row in vocab.head(120).itertuples(index=False):
        if len(exercises) + len(rows) >= 80:
            break
        if getattr(row, "article", "") in {"der", "die", "das"}:
            rows.append(
                {
                    "lesson_id": lesson_id,
                    "exercise_type": "article_choice",
                    "prompt_pt": f"Escolhe o artigo correto para '{row.german}'.",
                    "prompt_de": row.german,
                    "correct_answer": row.article,
                    "options": "der|die|das",
                    "explanation_pt": f"'{row.german}' usa o artigo {row.article}. Aprende sempre o nome com o artigo.",
                    "grammar_topic": "Artigos der die das",
                    "vocabulary_topic": row.topic,
                    "difficulty": row.difficulty,
                }
            )
        else:
            rows.append(
                {
                    "lesson_id": lesson_id,
                    "exercise_type": "translation_de_pt",
                    "prompt_pt": f"Traduz para português: {row.german}",
                    "prompt_de": row.german,
                    "correct_answer": row.portuguese,
                    "options": "",
                    "explanation_pt": f"{row.german} significa {row.portuguese}.",
                    "grammar_topic": "",
                    "vocabulary_topic": row.topic,
                    "difficulty": row.difficulty,
                }
            )
        lesson_id = 1 + (lesson_id % 16)
    return pd.concat([exercises, pd.DataFrame(rows)], ignore_index=True)


def _seed_review_queue(conn: sqlite3.Connection) -> None:
    vocab_ids = [row[0] for row in conn.execute("SELECT vocab_id FROM vocabulary LIMIT 25").fetchall()]
    for vocab_id in vocab_ids:
        conn.execute(
            """
            INSERT OR IGNORE INTO review_queue(user_id, item_type, item_id, ease_factor, interval_days, repetitions, due_date, last_result)
            VALUES (1, 'vocabulary', ?, 2.5, 0, 0, ?, 'new')
            """,
            (vocab_id, now_iso()),
        )
