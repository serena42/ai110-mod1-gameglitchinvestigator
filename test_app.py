from streamlit.testing.v1 import AppTest


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
