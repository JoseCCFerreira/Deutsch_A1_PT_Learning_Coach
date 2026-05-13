from src.db import connect, create_schema, ensure_default_user
from src.seed_data import seed_database
from src.translator import translate_offline


def test_translation_fallback_template(tmp_path):
    conn = connect(tmp_path / "test.db")
    create_schema(conn)
    ensure_default_user(conn)
    seed_database(conn)
    result = translate_offline(conn, "Ich komme aus Portugal.", "de", "pt")
    assert "Portugal" in result["translated_text"]
    assert result["breakdown"]
