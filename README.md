# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Game purpose:** A number guessing game where the player tries to guess a secret number within a limited number of attempts. The difficulty setting controls the range of possible numbers and the number of guesses allowed.
- [x] **Bugs found:** Hint messages were reversed (too high said "Go HIGHER", too low said "Go LOWER"); wrong guesses could add points instead of subtracting; Hard difficulty had a smaller range than Normal making it easier; decimal input like "5.7" was silently accepted; string vs integer comparison produced incorrect results on even-numbered attempts; the New Game button did not reset score, status, or history.
- [x] **Fixes applied:** Swapped hint messages in `check_guess()`; unified wrong-guess scoring to always subtract 5 in `update_score()`; widened Hard range to 1–200; rejected decimal input with an error message; fixed type comparison by converting both values to int; fully reset all session state on New Game; wrapped input in `st.form` so pressing Enter submits a guess.

## 📸 Demo Walkthrough

1. Clone the repo and set up a virtual environment: `python3 -m venv .venv && source .venv/bin/activate`
2. Install dependencies: `pip install -r requirements.txt`
3. Launch the game: `streamlit run app.py` — the app opens in your browser automatically.
4. Select a difficulty in the sidebar (Easy: 1–20, Normal: 1–100, Hard: 1–200). The attempt limit and range update immediately.
5. Type a guess into the input field and press **Enter** or click **Submit Guess**.
6. The game returns a hint — "Go HIGHER!" if your guess was too low, "Go LOWER!" if it was too high — and updates your score.
7. Continue guessing, following the hints to narrow down the secret number.
8. If you run out of attempts, the game reveals the secret number and displays your final score.
9. If you guess correctly, balloons appear and the game congratulates you with your final score.
10. Click **New Game** at any point to reset the score, history, and secret number and start a fresh round on the selected difficulty.

## 🧪 Test Results

```
============================= test session starts ==============================
platform darwin -- Python 3.14.4, pytest-9.0.3, pluggy-1.6.0
collected 23 items

tests/test_game_logic.py::test_easy_range PASSED
tests/test_game_logic.py::test_normal_range PASSED
tests/test_game_logic.py::test_hard_range_is_wider_than_normal PASSED
tests/test_game_logic.py::test_unknown_difficulty_defaults_to_normal PASSED
tests/test_game_logic.py::test_parse_guess_none_returns_error PASSED
tests/test_game_logic.py::test_parse_guess_empty_string_returns_error PASSED
tests/test_game_logic.py::test_parse_guess_valid_integer PASSED
tests/test_game_logic.py::test_parse_guess_decimal_is_rejected PASSED
tests/test_game_logic.py::test_parse_guess_non_numeric_returns_error PASSED
tests/test_game_logic.py::test_parse_guess_negative_number_is_accepted PASSED
tests/test_game_logic.py::test_check_guess_correct_returns_win PASSED
tests/test_game_logic.py::test_check_guess_too_high_returns_correct_outcome PASSED
tests/test_game_logic.py::test_check_guess_too_low_returns_correct_outcome PASSED
tests/test_game_logic.py::test_check_guess_too_high_message_says_go_lower PASSED
tests/test_game_logic.py::test_check_guess_too_low_message_says_go_higher PASSED
tests/test_game_logic.py::test_check_guess_int_vs_string_secret_win PASSED
tests/test_game_logic.py::test_check_guess_int_vs_string_secret_lexicographic_bug PASSED
tests/test_game_logic.py::test_update_score_win_on_first_attempt_gives_max_points PASSED
tests/test_game_logic.py::test_update_score_win_never_goes_below_minimum PASSED
tests/test_game_logic.py::test_update_score_too_low_subtracts_five PASSED
tests/test_game_logic.py::test_update_score_too_high_always_subtracts_points PASSED
tests/test_game_logic.py::test_update_score_unknown_outcome_leaves_score_unchanged PASSED
tests/test_game_logic.py::test_update_score_win_decreases_with_more_attempts PASSED

============================== 23 passed in 0.02s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
