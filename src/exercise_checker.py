from __future__ import annotations

import sqlite3

from .utils import clamp, normalise_answer, now_iso


def check_answer(user_answer: str, correct_answer: str, exercise_type: str = "") -> dict:
    user = normalise_answer(user_answer)
    correct = normalise_answer(correct_answer)
    accepted = [normalise_answer(part) for part in correct_answer.split("|")]
    is_correct = user in accepted or user == correct
    if not is_correct and exercise_type.startswith("translation") and correct in user:
        is_correct = True
    return {
        "is_correct": is_correct,
        "error_type": classify_error(user_answer, correct_answer, exercise_type) if not is_correct else "",
        "normalised_user": user,
        "normalised_correct": correct,
    }


def classify_error(user_answer: str, correct_answer: str, exercise_type: str) -> str:
    user = normalise_answer(user_answer)
    correct = normalise_answer(correct_answer)
    if exercise_type == "article_choice":
        return "article_error"
    if "____" in user or exercise_type == "verb_conjugation":
        return "verb_conjugation_error"
    if exercise_type == "order_words":
        return "word_order_error"
    if exercise_type.startswith("translation"):
        return "translation_error"
    if abs(len(user) - len(correct)) <= 2:
        return "spelling_error"
    return "vocabulary_error"


def save_attempt(
    conn: sqlite3.Connection,
    user_id: int,
    exercise: dict,
    user_answer: str,
    seconds: int = 0,
) -> dict:
    result = check_answer(user_answer, exercise["correct_answer"], exercise["exercise_type"])
    conn.execute(
        """
        INSERT INTO user_attempts(user_id, exercise_id, user_answer, correct_answer, is_correct, error_type,
        grammar_topic, vocabulary_topic, time_spent_seconds, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            int(exercise["exercise_id"]),
            user_answer,
            exercise["correct_answer"],
            int(result["is_correct"]),
            result["error_type"],
            exercise.get("grammar_topic", ""),
            exercise.get("vocabulary_topic", ""),
            seconds,
            now_iso(),
        ),
    )
    update_mastery(conn, user_id, "grammar", exercise.get("grammar_topic", ""), bool(result["is_correct"]), seconds)
    update_mastery(conn, user_id, "vocabulary", exercise.get("vocabulary_topic", ""), bool(result["is_correct"]), seconds)
    conn.commit()
    return result


def update_mastery(conn: sqlite3.Connection, user_id: int, topic_type: str, topic_name: str, is_correct: bool, seconds: int = 0) -> None:
    if not topic_name:
        return
    row = conn.execute(
        "SELECT mastery_score, attempts, correct_attempts FROM mastery_state WHERE user_id=? AND topic_type=? AND topic_name=?",
        (user_id, topic_type, topic_name),
    ).fetchone()
    delta = 7 if is_correct else -10
    if is_correct and seconds and seconds < 10:
        delta += 2
    if row:
        score = clamp(float(row["mastery_score"]) + delta)
        attempts = int(row["attempts"]) + 1
        correct = int(row["correct_attempts"]) + (1 if is_correct else 0)
        conn.execute(
            """
            UPDATE mastery_state
            SET mastery_score=?, attempts=?, correct_attempts=?, last_practiced=?, next_review=datetime('now', '+1 day')
            WHERE user_id=? AND topic_type=? AND topic_name=?
            """,
            (score, attempts, correct, now_iso(), user_id, topic_type, topic_name),
        )
    else:
        conn.execute(
            """
            INSERT INTO mastery_state(user_id, topic_type, topic_name, mastery_score, attempts, correct_attempts, last_practiced, next_review)
            VALUES (?, ?, ?, ?, 1, ?, ?, datetime('now', '+1 day'))
            """,
            (user_id, topic_type, topic_name, 55 + delta, 1 if is_correct else 0, now_iso()),
        )
