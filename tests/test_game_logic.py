from logic_utils import check_guess
from streamlit.testing.v1 import AppTest

def test_new_game_resets_status_after_win():
    at = AppTest.from_file("app.py")
    at.run()

    # Simulate a finished game
    at.session_state.status = "won"
    at.session_state.history = [10, 20, 42]
    at.session_state.attempts = 3

    # Click "New Game"
    at.button[1].click().run()

    assert at.session_state.status == "playing"
    assert at.session_state.history == []
    assert at.session_state.attempts == 0

def test_new_game_resets_status_after_loss():
    at = AppTest.from_file("app.py")
    at.run()

    at.session_state.status = "lost"
    at.session_state.history = [5, 15, 25, 35, 45, 55, 65, 75]
    at.session_state.attempts = 8

    at.button[1].click().run()

    assert at.session_state.status == "playing"
    assert at.session_state.history == []
    assert at.session_state.attempts == 0

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"
