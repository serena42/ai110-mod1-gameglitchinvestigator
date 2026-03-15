from streamlit.testing.v1 import AppTest
from logic_utils import check_guess


def test_guess_persists_on_rerun():
    at = AppTest.from_file("app.py").run()

    # Type a first guess and submit
    at.text_input("raw_guess").set_value("42").run()
    at.button[0].click().run()

    # Change the guess and submit again — should use new value, not old
    at.text_input("raw_guess").set_value("75").run()
    at.button[0].click().run()

    # The history should contain both guesses, not 42 twice
    assert 42 in at.session_state["history"], "First guess was not recorded"
    assert 75 in at.session_state["history"], "Second guess was not registered — state bug may still be present"


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
