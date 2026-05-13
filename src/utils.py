from __future__ import annotations

from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "deutsch_a1.db"
CONFIG_DIR = PROJECT_ROOT / "config"


def now_iso() -> str:
    return datetime.now().replace(microsecond=0).isoformat()


def ensure_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "audio_tmp").mkdir(parents=True, exist_ok=True)


def normalise_answer(text: str | None) -> str:
    return " ".join((text or "").strip().lower().replace("ß", "ss").split())


def clamp(value: float, low: float = 0, high: float = 100) -> float:
    return max(low, min(high, value))
