from utils import get_range, check_guess


def test_easy_range():
    low, high = get_range("easy")
    assert low == 1 and high == 20


def test_medium_range():
    low, high = get_range("medium")
    assert low == 1 and high == 100


def test_hard_range():
    low, high = get_range("hard")
    assert low == 1 and high == 500


def test_invalid_defaults_to_medium():
    _, high = get_range("nonsense")
    assert high == 100


def test_too_low():
    assert check_guess(5, 10) == "too low"


def test_too_high():
    assert check_guess(15, 10) == "too high"


def test_correct():
    assert check_guess(10, 10) == "correct"