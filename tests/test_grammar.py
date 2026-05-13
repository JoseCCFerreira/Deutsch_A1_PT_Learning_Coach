from src.db import connect, create_schema, ensure_default_user
from src.grammar import load_grammar_topics
from src.seed_data import seed_database


def test_grammar_topics_seeded(tmp_path):
    conn = connect(tmp_path / "test.db")
    create_schema(conn)
    ensure_default_user(conn)
    seed_database(conn)
    grammar = load_grammar_topics(conn)
    assert len(grammar) >= 20
    assert "Verbo sein" in grammar["topic_name"].tolist()
