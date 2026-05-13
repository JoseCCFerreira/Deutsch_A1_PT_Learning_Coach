from __future__ import annotations

from .utils import normalise_answer


EXPECTED_PATTERNS = ["ich heiße", "ich komme aus", "ich wohne in", "ich arbeite", "ich lerne"]


def evaluate_writing(prompt_pt: str, user_text_de: str) -> dict:
    text = normalise_answer(user_text_de)
    score = 40
    feedback = []
    if any(pattern in text for pattern in EXPECTED_PATTERNS):
        score += 25
    if "ich" in text:
        score += 10
    if "." in user_text_de:
        score += 5
    if "bin" in text or "heiße" in user_text_de.lower() or "heisse" in text:
        score += 10
    if not user_text_de.strip():
        return {"score": 0, "corrected_text_de": "", "feedback_pt": "Escreve pelo menos uma frase.", "grammar_errors": "empty", "vocabulary_errors": ""}
    if "Ich" not in user_text_de:
        feedback.append("Em alemão, começa o pronome 'Ich' com maiúscula no início da frase.")
    if not any(pattern in text for pattern in EXPECTED_PATTERNS):
        feedback.append("Tenta usar uma estrutura A1 como 'Ich heiße...', 'Ich komme aus...' ou 'Ich wohne in...'.")
    corrected = user_text_de.strip()
    if corrected and corrected[0].islower():
        corrected = corrected[0].upper() + corrected[1:]
    return {
        "score": min(score, 100),
        "corrected_text_de": corrected,
        "feedback_pt": " ".join(feedback) or "Bom trabalho. A frase está adequada para A1.",
        "grammar_errors": "; ".join(feedback),
        "vocabulary_errors": "",
    }
