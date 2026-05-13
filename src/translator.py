from __future__ import annotations

import sqlite3

import pandas as pd

from .utils import normalise_answer, now_iso


TEMPLATES = {
    "ich komme aus portugal": ("Eu venho de Portugal / Sou de Portugal.", '"kommen aus" usa-se para dizer origem.'),
    "ich wohne in braga": ("Eu moro em Braga.", '"wohnen in" usa-se para dizer onde se vive.'),
    "ich heiße carlos": ("Eu chamo-me Carlos.", '"heißen" significa chamar-se.'),
    "eu venho de portugal": ("Ich komme aus Portugal.", 'Em A1 usa: "Ich komme aus + país".'),
    "eu moro em braga": ("Ich wohne in Braga.", 'Em A1 usa: "Ich wohne in + cidade".'),
    "eu chamo-me carlos": ("Ich heiße Carlos.", 'Para nome: "Ich heiße..."'),
}


def translate_offline(conn: sqlite3.Connection, text: str, source_language: str, target_language: str, user_id: int = 1) -> dict:
    key = normalise_answer(text)
    if key in TEMPLATES:
        translated, grammar = TEMPLATES[key]
    else:
        translated = _word_by_word(conn, text)
        grammar = "Tradução aproximada por dicionário local A1. Pode não respeitar toda a gramática da frase."
    breakdown = word_breakdown(conn, text)
    result = {
        "translated_text": translated,
        "explanation_pt": grammar,
        "breakdown": breakdown,
        "practice": similar_practice(text),
        "approximate": key not in TEMPLATES,
    }
    conn.execute(
        """
        INSERT INTO translation_history(user_id, source_text, source_language, target_language, translated_text, explanation_pt, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (user_id, text, source_language, target_language, translated, grammar, now_iso()),
    )
    conn.commit()
    return result


def _word_by_word(conn: sqlite3.Connection, text: str) -> str:
    vocab = pd.read_sql_query("SELECT german, portuguese FROM vocabulary", conn)
    dictionary = {normalise_answer(r.german): r.portuguese for r in vocab.itertuples(index=False)}
    dictionary.update({normalise_answer(r.portuguese): r.german for r in vocab.itertuples(index=False)})
    words = [dictionary.get(normalise_answer(token.strip(".,!?")), token) for token in text.split()]
    return " ".join(words)


def word_breakdown(conn: sqlite3.Connection, text: str) -> list[tuple[str, str]]:
    vocab = pd.read_sql_query("SELECT german, portuguese FROM vocabulary", conn)
    dictionary = {normalise_answer(r.german): r.portuguese for r in vocab.itertuples(index=False)}
    dictionary.update({normalise_answer(r.portuguese): r.german for r in vocab.itertuples(index=False)})
    return [(token.strip(".,!?"), dictionary.get(normalise_answer(token.strip(".,!?")), "desconhecido no dicionário A1 local")) for token in text.split()]


def similar_practice(text: str) -> list[str]:
    key = normalise_answer(text)
    if "komme" in key or "venho" in key:
        return ["Eu venho de Braga.", "Ela vem da Alemanha.", "Nós vimos de Portugal."]
    if "wohne" in key or "moro" in key:
        return ["Eu moro em Lisboa.", "Ele mora no Porto.", "Nós moramos em Braga."]
    return ["Ich heiße Carlos.", "Ich komme aus Portugal.", "Ich wohne in Braga."]
