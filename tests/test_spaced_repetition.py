from src.spaced_repetition import schedule_sm2


def test_sm2_easy_increases_interval():
    result = schedule_sm2(2.5, 1, 1, "Fácil")
    assert result["repetitions"] == 2
    assert result["interval_days"] >= 6


def test_sm2_fail_resets():
    result = schedule_sm2(2.5, 10, 3, "Não sabia")
    assert result["repetitions"] == 0
    assert result["interval_days"] == 1
