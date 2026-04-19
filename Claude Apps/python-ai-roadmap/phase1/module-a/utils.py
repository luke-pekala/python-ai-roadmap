import random


def get_range(difficulty: str) -> tuple[int, int]:
    ranges = {
        "easy": (1, 20),
        "medium": (1, 100),
        "hard": (1, 500),
    }
    return ranges.get(difficulty.lower(), (1, 100))


def get_secret(low: int, high: int) -> int:
    return random.randint(low, high)


def check_guess(guess: int, secret: int) -> str:
    if guess < secret:
        return "too low"
    elif guess > secret:
        return "too high"
    else:
        return "correct"