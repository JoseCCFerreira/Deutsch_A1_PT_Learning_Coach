from __future__ import annotations

from .audio import pronunciation_feedback


def evaluate_speaking(expected_text_de: str, typed_attempt: str) -> dict:
    result = pronunciation_feedback(expected_text_de, typed_attempt)
    result["feedback_pt"] += " Se não conseguires usar microfone, lê em voz alta e escreve o que disseste."
    return result
