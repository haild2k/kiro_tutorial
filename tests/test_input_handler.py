"""
test_input_handler.py — Unit tests for the InputHandler class.

Covers:
- get_move() returns valid cell when input is correct
- get_move() calls render_error and loops when input is not a number
- get_move() calls render_error and loops when input is out of range 1–16
- get_move() calls render_error and loops when cell is already occupied
- get_play_again() returns True for 'y' and 'Y'
- get_play_again() returns False for 'n' and 'N'
- get_play_again() loops when input is invalid

Requirements: R3.1–R3.6, R6.1, R6.4
"""

from unittest.mock import MagicMock, call, patch

import pytest

from board import Board
from input_handler import InputHandler


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_handler() -> tuple[InputHandler, MagicMock]:
    """Return an InputHandler with a mock Renderer."""
    mock_renderer = MagicMock()
    handler = InputHandler(mock_renderer)
    return handler, mock_renderer


# ---------------------------------------------------------------------------
# get_move() — valid input
# ---------------------------------------------------------------------------

class TestGetMoveValidInput:
    """R3.1, R3.2 — get_move() returns the cell number when input is valid."""

    def test_returns_valid_cell_number(self):
        """get_move() should return the integer cell number on valid input."""
        handler, _ = make_handler()
        board = Board()

        with patch("builtins.input", return_value="5"):
            result = handler.get_move(board)

        assert result == 5

    def test_returns_cell_1_boundary(self):
        """get_move() should accept cell 1 (lower boundary)."""
        handler, _ = make_handler()
        board = Board()

        with patch("builtins.input", return_value="1"):
            result = handler.get_move(board)

        assert result == 1

    def test_returns_cell_16_boundary(self):
        """get_move() should accept cell 16 (upper boundary)."""
        handler, _ = make_handler()
        board = Board()

        with patch("builtins.input", return_value="16"):
            result = handler.get_move(board)

        assert result == 16

    def test_strips_whitespace_from_input(self):
        """get_move() should handle input with surrounding whitespace."""
        handler, _ = make_handler()
        board = Board()

        with patch("builtins.input", return_value="  8  "):
            result = handler.get_move(board)

        assert result == 8

    def test_no_error_called_on_valid_input(self):
        """render_error() must NOT be called when input is valid."""
        handler, mock_renderer = make_handler()
        board = Board()

        with patch("builtins.input", return_value="7"):
            handler.get_move(board)

        mock_renderer.render_error.assert_not_called()


# ---------------------------------------------------------------------------
# get_move() — non-integer input
# ---------------------------------------------------------------------------

class TestGetMoveNonIntegerInput:
    """R3.3 — get_move() calls render_error and re-prompts on non-integer input."""

    def test_calls_render_error_on_non_integer(self):
        """render_error() must be called with the range message for non-integer input."""
        handler, mock_renderer = make_handler()
        board = Board()

        with patch("builtins.input", side_effect=["abc", "5"]):
            handler.get_move(board)

        mock_renderer.render_error.assert_called_once_with(
            "Invalid input. Please enter a number between 1 and 16."
        )

    def test_loops_until_valid_after_non_integer(self):
        """get_move() must keep looping until a valid integer is entered."""
        handler, mock_renderer = make_handler()
        board = Board()

        with patch("builtins.input", side_effect=["abc", "xyz", "3"]):
            result = handler.get_move(board)

        assert result == 3
        assert mock_renderer.render_error.call_count == 2

    def test_empty_string_triggers_error(self):
        """Empty string input should trigger render_error."""
        handler, mock_renderer = make_handler()
        board = Board()

        with patch("builtins.input", side_effect=["", "10"]):
            result = handler.get_move(board)

        assert result == 10
        mock_renderer.render_error.assert_called_once_with(
            "Invalid input. Please enter a number between 1 and 16."
        )

    def test_float_string_triggers_error(self):
        """Float string like '3.5' should trigger render_error (not a valid integer)."""
        handler, mock_renderer = make_handler()
        board = Board()

        with patch("builtins.input", side_effect=["3.5", "4"]):
            result = handler.get_move(board)

        assert result == 4
        mock_renderer.render_error.assert_called_once_with(
            "Invalid input. Please enter a number between 1 and 16."
        )


# ---------------------------------------------------------------------------
# get_move() — out-of-range input
# ---------------------------------------------------------------------------

class TestGetMoveOutOfRange:
    """R3.4 — get_move() calls render_error and re-prompts when input is outside 1–16."""

    def test_calls_render_error_on_zero(self):
        """Cell 0 is out of range — render_error must be called."""
        handler, mock_renderer = make_handler()
        board = Board()

        with patch("builtins.input", side_effect=["0", "6"]):
            result = handler.get_move(board)

        assert result == 6
        mock_renderer.render_error.assert_called_once_with(
            "Invalid input. Please enter a number between 1 and 16."
        )

    def test_calls_render_error_on_17(self):
        """Cell 17 is out of range — render_error must be called."""
        handler, mock_renderer = make_handler()
        board = Board()

        with patch("builtins.input", side_effect=["17", "9"]):
            result = handler.get_move(board)

        assert result == 9
        mock_renderer.render_error.assert_called_once_with(
            "Invalid input. Please enter a number between 1 and 16."
        )

    def test_calls_render_error_on_negative(self):
        """Negative numbers are out of range — render_error must be called."""
        handler, mock_renderer = make_handler()
        board = Board()

        with patch("builtins.input", side_effect=["-1", "2"]):
            result = handler.get_move(board)

        assert result == 2
        mock_renderer.render_error.assert_called_once_with(
            "Invalid input. Please enter a number between 1 and 16."
        )

    def test_loops_multiple_out_of_range(self):
        """get_move() must loop for each out-of-range input."""
        handler, mock_renderer = make_handler()
        board = Board()

        with patch("builtins.input", side_effect=["0", "100", "-5", "12"]):
            result = handler.get_move(board)

        assert result == 12
        assert mock_renderer.render_error.call_count == 3


# ---------------------------------------------------------------------------
# get_move() — occupied cell
# ---------------------------------------------------------------------------

class TestGetMoveOccupiedCell:
    """R3.6 — get_move() calls render_error and re-prompts when cell is occupied."""

    def test_calls_render_error_on_occupied_cell(self):
        """render_error() must be called with the occupied message for an occupied cell."""
        handler, mock_renderer = make_handler()
        board = Board()
        board.place(5, 'X')

        with patch("builtins.input", side_effect=["5", "6"]):
            result = handler.get_move(board)

        assert result == 6
        mock_renderer.render_error.assert_called_once_with(
            "Cell already occupied. Please choose another cell."
        )

    def test_loops_until_empty_cell_chosen(self):
        """get_move() must keep looping until an unoccupied cell is entered."""
        handler, mock_renderer = make_handler()
        board = Board()
        board.place(1, 'X')
        board.place(2, 'O')
        board.place(3, 'X')

        with patch("builtins.input", side_effect=["1", "2", "3", "4"]):
            result = handler.get_move(board)

        assert result == 4
        assert mock_renderer.render_error.call_count == 3
        for c in mock_renderer.render_error.call_args_list:
            assert c == call("Cell already occupied. Please choose another cell.")

    def test_occupied_error_message_differs_from_range_error(self):
        """Occupied cell error message must be distinct from range error message."""
        handler, mock_renderer = make_handler()
        board = Board()
        board.place(8, 'O')

        with patch("builtins.input", side_effect=["abc", "8", "9"]):
            result = handler.get_move(board)

        assert result == 9
        assert mock_renderer.render_error.call_count == 2
        calls = mock_renderer.render_error.call_args_list
        assert calls[0] == call("Invalid input. Please enter a number between 1 and 16.")
        assert calls[1] == call("Cell already occupied. Please choose another cell.")


# ---------------------------------------------------------------------------
# get_play_again() — valid responses
# ---------------------------------------------------------------------------

class TestGetPlayAgainValidInput:
    """R6.1, R6.4 — get_play_again() returns True for y/Y and False for n/N."""

    def test_returns_true_for_lowercase_y(self):
        """'y' should return True."""
        handler, _ = make_handler()

        with patch("builtins.input", return_value="y"):
            result = handler.get_play_again('X')

        assert result is True

    def test_returns_true_for_uppercase_y(self):
        """'Y' should return True."""
        handler, _ = make_handler()

        with patch("builtins.input", return_value="Y"):
            result = handler.get_play_again('X')

        assert result is True

    def test_returns_false_for_lowercase_n(self):
        """'n' should return False."""
        handler, _ = make_handler()

        with patch("builtins.input", return_value="n"):
            result = handler.get_play_again('O')

        assert result is False

    def test_returns_false_for_uppercase_n(self):
        """'N' should return False."""
        handler, _ = make_handler()

        with patch("builtins.input", return_value="N"):
            result = handler.get_play_again('O')

        assert result is False


# ---------------------------------------------------------------------------
# get_play_again() — invalid input loops
# ---------------------------------------------------------------------------

class TestGetPlayAgainInvalidInput:
    """R6.4 — get_play_again() re-prompts silently on invalid input."""

    def test_loops_on_invalid_then_accepts_y(self):
        """Invalid input should be discarded and prompt repeated until 'y'."""
        handler, _ = make_handler()

        with patch("builtins.input", side_effect=["maybe", "yes", "y"]):
            result = handler.get_play_again('X')

        assert result is True

    def test_loops_on_invalid_then_accepts_n(self):
        """Invalid input should be discarded and prompt repeated until 'n'."""
        handler, _ = make_handler()

        with patch("builtins.input", side_effect=["no", "nope", "n"]):
            result = handler.get_play_again('O')

        assert result is False

    def test_loops_on_empty_string(self):
        """Empty string is invalid — prompt must repeat."""
        handler, _ = make_handler()

        with patch("builtins.input", side_effect=["", "Y"]):
            result = handler.get_play_again('X')

        assert result is True

    def test_loops_on_numeric_input(self):
        """Numeric input is invalid for play-again — prompt must repeat."""
        handler, _ = make_handler()

        with patch("builtins.input", side_effect=["1", "N"]):
            result = handler.get_play_again('X')

        assert result is False

    def test_no_render_error_called_for_invalid_play_again(self):
        """R6.4 — Invalid play-again input silently re-prompts (no render_error call)."""
        handler, mock_renderer = make_handler()

        with patch("builtins.input", side_effect=["bad", "y"]):
            handler.get_play_again('X')

        mock_renderer.render_error.assert_not_called()

    def test_input_called_multiple_times_on_invalid(self):
        """input() must be called once per prompt iteration."""
        handler, _ = make_handler()

        with patch("builtins.input", side_effect=["x", "z", "n"]) as mock_input:
            result = handler.get_play_again('O')

        assert result is False
        assert mock_input.call_count == 3
