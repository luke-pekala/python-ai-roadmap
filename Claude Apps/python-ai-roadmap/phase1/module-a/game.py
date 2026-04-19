from utils import get_range, get_secret, check_guess


def play_game() -> None:
    print("\n=== Number Guesser ===")
    difficulty = input("Choose difficulty (easy / medium / hard): ").strip()
    low, high = get_range(difficulty)
    secret = get_secret(low, high)
    attempts = 0

    print(f"\nI'm thinking of a number between {low} and {high}. Go!\n")

    while True:
        try:
            guess = int(input("Your guess: "))
        except ValueError:
            print("Please enter a whole number.")
            continue

        attempts += 1
        result = check_guess(guess, secret)

        if result == "correct":
            print(f"\nCorrect! You got it in {attempts} attempt{'s' if attempts != 1 else ''}.")
            break
        else:
            print(f"  {result.capitalize()} — try again.")

    replay = input("\nPlay again? (y/n): ").strip().lower()
    if replay == "y":
        play_game()


if __name__ == "__main__":
    play_game()