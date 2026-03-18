from streamlit.testing.v1 import AppTest
from logic_utils import check_guess


def test_guess_persists_on_rerun():
    at = AppTest.from_file("app.py").run()

    # Type a guess and submit in one step
    at.text_input("raw_guess").set_value("42").run()
    at.button[0].click().run()

    # The guess should appear in history — confirms value survived the rerun
    assert 42 in at.session_state["history"], "Guess was not recorded — state bug may still be present"


def test_hint_too_high():
    outcome, message = check_guess(80, 50)
    assert outcome == "Too High"
    assert "LOWER" in message, f"Expected hint to say LOWER, got: {message}"


def test_hint_too_low():
    outcome, message = check_guess(20, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message, f"Expected hint to say HIGHER, got: {message}"


def test_hint_correct():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"


def test_hint_persists_after_rerun():
    at = AppTest.from_file("app.py").run()

    # Submit a guess
    at.text_input("raw_guess").set_value("1").run()
    at.button[0].click().run()

    # Simulate a rerun without clicking submit (e.g. user just looks at the page)
    at.run()

    # The hint should still be visible via session state
    assert at.session_state["last_message"] is not None, "Hint disappeared after rerun"


def test_new_game_resets_score():
    at = AppTest.from_file("app.py").run()

    # Submit a guess to build up some score activity
    at.text_input("raw_guess").set_value("1").run()
    at.button[0].click().run()

    # Click New Game
    at.button[1].click().run()

    assert at.session_state["score"] == 0, "Score was not reset on new game"


def test_new_game_resets_status():
    at = AppTest.from_file("app.py").run()

    # Force a won status
    at.session_state["status"] = "won"
    at.run()

    # Click New Game
    at.button[1].click().run()

    assert at.session_state["status"] == "playing", "Status was not reset to playing on new game"


# --- Edge case tests for parse_guess ---

from logic_utils import parse_guess


def test_parse_guess_empty_string():
    # Empty input should fail gracefully with a helpful message
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert "guess" in err.lower(), f"Expected prompt to enter a guess, got: {err}"


def test_parse_guess_non_numeric_string():
    # Letters should fail with a clear error, not crash
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert "number" in err.lower(), f"Expected 'not a number' error, got: {err}"


def test_parse_guess_negative_number():
    # Negative numbers are valid integers — should parse successfully
    ok, value, err = parse_guess("-5")
    assert ok is True
    assert value == -5
    assert err is None


def test_parse_guess_float_string():
    # Floats like "7.9" should be truncated to int, not rejected
    ok, value, err = parse_guess("7.9")
    assert ok is True
    assert value == 7
    assert err is None


def test_parse_guess_none_input():
    # None input (e.g. before user types anything) should fail gracefully
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None
