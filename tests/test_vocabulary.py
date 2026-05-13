from src.db import connect, create_schema, ensure_default_user
from src.seed_data import seed_database
from src.vocabulary import load_vocabulary


def test_load_vocabulary_has_a1_words(tmp_path):
    conn = connect(tmp_path / "test.db")
    create_schema(conn)
    ensure_default_user(conn)
    seed_database(conn)
    vocab = load_vocabulary(conn)
    assert len(vocab) >= 200
    assert {"german", "portuguese", "topic"}.issubset(vocab.columns)
