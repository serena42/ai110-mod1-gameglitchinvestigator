def get_range_for_difficulty(difficulty: str) -> tuple[int, int]:
    """Return the inclusive (low, high) number range for a given difficulty level.

    Args:
        difficulty: One of "Easy", "Normal", or "Hard".

    Returns:
        A tuple (low, high) representing the inclusive guessing range.
        Defaults to (1, 100) for unrecognized difficulty values.
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str) -> tuple[bool, int | None, str | None]:
    """Parse raw user input into a validated integer guess.

    Accepts integer strings and float strings (truncated to int).
    Rejects None, empty strings, and non-numeric input.

    Args:
        raw: The raw string value from the text input widget.

    Returns:
        A tuple (ok, value, error) where:
            - ok (bool): True if parsing succeeded.
            - value (int | None): The parsed integer, or None on failure.
            - error (str | None): A user-facing error message, or None on success.
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret) -> tuple[str, str]:
    """Compare a guess to the secret number and return an outcome and hint message.

    Handles a deliberate bug in the original code where the secret is sometimes
    passed as a string (on even-numbered attempts), requiring a type-safe fallback.

    Args:
        guess: The player's integer guess.
        secret: The secret number (int or str depending on caller).

    Returns:
        A tuple (outcome, message) where outcome is one of:
            - "Win": guess matches secret.
            - "Too High": guess is greater than secret.
            - "Too Low": guess is less than secret.
        And message is a user-facing hint string.
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        if guess > secret:
            return "Too High", "📈 Go LOWER!"
        else:
            return "Too Low", "📉 Go HIGHER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📈 Go LOWER!"
        return "Too Low", "📉 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """Calculate and return the updated score based on the latest guess outcome.

    Winning awards points on a decreasing scale (100 minus 10 per attempt),
    with a minimum of 10 points. Incorrect guesses subtract 5 points, except
    "Too High" guesses on even-numbered attempts which add 5 (a known scoring quirk).

    Args:
        current_score: The player's score before this guess.
        outcome: The result string from check_guess ("Win", "Too High", or "Too Low").
        attempt_number: The 1-based attempt count for the current game.

    Returns:
        The updated integer score.
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
