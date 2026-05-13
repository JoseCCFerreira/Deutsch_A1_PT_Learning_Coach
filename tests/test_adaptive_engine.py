from src.adaptive_engine import mastery_status, recommend_next
from src.db import connect, create_schema, ensure_default_user
from src.seed_data import seed_database


def test_mastery_status_labels():
    assert mastery_status(20) == "Fraco"
    assert mastery_status(90) == "Forte"


def test_adaptive_recommendation_default(tmp_path):
    conn = connect(tmp_path / "test.db")
    create_schema(conn)
    ensure_default_user(conn)
    seed_database(conn)
    rec = recommend_next(conn)
    assert "lesson" in rec
    assert rec["difficulty"] >= 1
