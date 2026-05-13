from src.exercise_checker import check_answer, classify_error


def test_check_answer_accepts_exact_answer():
    result = check_answer("Ich komme aus Portugal.", "Ich komme aus Portugal.", "translation_pt_de")
    assert result["is_correct"] is True


def test_article_error_classification():
    assert classify_error("die", "der", "article_choice") == "article_error"
