from __future__ import annotations

from pathlib import Path

from gtts import gTTS

from .utils import DATA_DIR, normalise_answer


def generate_tts(text: str, language: str = "de") -> Path | None:
    audio_dir = DATA_DIR / "audio_tmp"
    audio_dir.mkdir(parents=True, exist_ok=True)
    path = audio_dir / f"{abs(hash(text))}.mp3"
    if path.exists():
        return path
    try:
        gTTS(text=text, lang=language).save(str(path))
        return path
    except Exception:
        return None


def pronunciation_feedback(expected: str, typed: str) -> dict:
    expected_norm = normalise_answer(expected)
    typed_norm = normalise_answer(typed)
    score = 100 if expected_norm == typed_norm else max(0, 100 - abs(len(expected_norm) - len(typed_norm)) * 8)
    tips = []
    for sound in ["ich", "ch", "sch", "ei", "ie", "eu", "ä", "ö", "ü"]:
        if sound in expected_norm:
            tips.append(f"Treina o som '{sound}' nesta frase.")
    if expected_norm != typed_norm:
        tips.append("Compara palavra por palavra com a frase esperada.")
    return {"score": score, "feedback_pt": " ".join(tips) or "Boa tentativa. Repete em voz alta para ganhar fluidez."}


def cleanup_audio() -> None:
    audio_dir = DATA_DIR / "audio_tmp"
    if not audio_dir.exists():
        return
    for path in audio_dir.glob("*.mp3"):
        path.unlink(missing_ok=True)
