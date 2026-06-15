import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score


# =============================================================================
# get_range_for_difficulty()
# =============================================================================

def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20


def test_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 100


def test_hard_range_is_wider_than_normal():
    # Hard should be harder to guess, meaning a WIDER range (more numbers).
    # Bug: Hard returns (1, 50) which is actually EASIER than Normal (1, 100).
    _, hard_high = get_range_for_difficulty("Hard")
    _, normal_high = get_range_for_difficulty("Normal")
    assert hard_high > normal_high, (
        f"Hard upper bound ({hard_high}) should be greater than Normal ({normal_high}) "
        "to make guessing harder, not easier."
    )


def test_unknown_difficulty_defaults_to_normal():
    low, high = get_range_for_difficulty("Unknown")
    assert low == 1
    assert high == 100


# =============================================================================
# parse_guess()
# =============================================================================

def test_parse_guess_none_returns_error():
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None
    assert err is not None


def test_parse_guess_empty_string_returns_error():
    # Empty input must return an error — not silently pass or crash.
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err is not None


def test_parse_guess_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None


def test_parse_guess_decimal_is_rejected():
    # "5.7" is not a valid whole-number guess and should return an error.
    # Bug: the current implementation silently truncates it to 5 via int(float("5.7")),
    # which can fool the player into thinking 5.7 was accepted as-is.
    ok, value, err = parse_guess("5.7")
    assert ok is False, (
        "Decimal input '5.7' should be rejected with an error, "
        "not silently truncated to 5."
    )


def test_parse_guess_non_numeric_returns_error():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err is not None


def test_parse_guess_negative_number_is_accepted():
    # Negative numbers are technically valid integers; the function should parse them.
    ok, value, err = parse_guess("-5")
    assert ok is True
    assert value == -5


# =============================================================================
# check_guess()
# =============================================================================

def test_check_guess_correct_returns_win():
    # check_guess returns a (outcome, message) tuple.
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"


def test_check_guess_too_high_returns_correct_outcome():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"


def test_check_guess_too_low_returns_correct_outcome():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


def test_check_guess_too_high_message_says_go_lower():
    # When the guess is too high, the player needs to guess LOWER.
    # Bug: the message currently says "📈 Go HIGHER!" — the arrow and direction are backwards.
    outcome, message = check_guess(60, 50)
    assert "LOWER" in message.upper(), (
        f"Guess too high → hint should say 'Go LOWER', but got: '{message}'"
    )


def test_check_guess_too_low_message_says_go_higher():
    # When the guess is too low, the player needs to guess HIGHER.
    # Bug: the message currently says "📉 Go LOWER!" — backwards.
    outcome, message = check_guess(40, 50)
    assert "HIGHER" in message.upper(), (
        f"Guess too low → hint should say 'Go HIGHER', but got: '{message}'"
    )


def test_check_guess_int_vs_string_secret_win():
    # app.py converts the secret to a string on even-numbered attempts before passing
    # it to check_guess. Winning with an int guess against a string secret should work.
    outcome, message = check_guess(50, "50")
    assert outcome == "Win"


def test_check_guess_int_vs_string_secret_lexicographic_bug():
    # When secret is a string, Python falls back to lexicographic comparison.
    # "9" > "50" because '9' > '5' character-by-character — even though 9 < 50.
    # Bug: check_guess(9, "50") returns "Too High" instead of "Too Low".
    outcome, message = check_guess(9, "50")
    assert outcome == "Too Low", (
        f"guess=9, secret='50': expected 'Too Low' (9 < 50), got '{outcome}'. "
        "Lexicographic string comparison gives the wrong result."
    )


# =============================================================================
# update_score()
# =============================================================================

def test_update_score_win_on_first_attempt_gives_max_points():
    # Winning on attempt 1 should award the highest score.
    # Bug: app.py increments attempts BEFORE calling update_score, so
    # attempt_number is always at least 2 on the first real guess, reducing the reward.
    score = update_score(0, "Win", 1)
    # Expected: 100 - 10 * (1 + 1) = 80
    assert score == 80


def test_update_score_win_never_goes_below_minimum():
    # Even a very late win should award at least 10 points.
    score = update_score(0, "Win", 10)
    assert score >= 10


def test_update_score_too_low_subtracts_five():
    score = update_score(50, "Too Low", 1)
    assert score == 45


def test_update_score_too_high_always_subtracts_points():
    # Too High and Too Low should behave consistently — both wrong guesses.
    # Bug: on even attempt_number, Too High adds 5 points instead of subtracting,
    # rewarding the player for a wrong guess.
    score_odd = update_score(50, "Too High", 1)   # odd attempt → -5
    score_even = update_score(50, "Too High", 2)  # even attempt → currently +5 (bug)

    assert score_odd == 45, f"Too High on odd attempt should subtract 5, got {score_odd}"
    assert score_even == 45, (
        f"Too High on even attempt should also subtract 5, not add 5. Got {score_even}."
    )


def test_update_score_unknown_outcome_leaves_score_unchanged():
    score = update_score(50, "SomethingElse", 1)
    assert score == 50


def test_update_score_win_decreases_with_more_attempts():
    # More attempts before winning should yield a lower score.
    early_win = update_score(0, "Win", 1)
    late_win = update_score(0, "Win", 5)
    assert early_win > late_win, (
        f"Winning earlier (attempt 1, score={early_win}) should outscore "
        f"winning later (attempt 5, score={late_win})."
    )
