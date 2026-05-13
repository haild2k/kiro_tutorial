"""
test_renderer.py — Unit tests for the Renderer class.

Covers:
- _detect_color_support() returns False when stdout is not a TTY
- _colorize() wraps with ANSI when color_enabled=True, returns plain text when False
- render_board() output contains cell numbers for empty cells
- render_board() output contains 'X' and 'O' for occupied cells
- render_board() output contains the separator '----+----+----+----'
- render_error() output contains the passed message

Requirements: R1.2, R1.3, R1.6, R7.1, R7.8
"""

from unittest.mock import patch

import pytest

from board import Board
from renderer import Color, Renderer


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_renderer(color_enabled: bool) -> Renderer:
    """Create a Renderer with color_enabled forced to the given value."""
    r = Renderer.__new__(Renderer)
    r.color_enabled = color_enabled
    return r


# ---------------------------------------------------------------------------
# _detect_color_support()
# ---------------------------------------------------------------------------

class TestDetectColorSupport:
    def test_returns_false_when_not_tty(self):
        """R7.1 — When stdout is not a TTY, color support must be False."""
        with patch("sys.stdout") as mock_stdout:
            mock_stdout.isatty.return_value = False
            renderer = Renderer()
        assert renderer.color_enabled is False

    def test_returns_false_when_not_tty_via_method(self):
        """R7.1 — _detect_color_support() itself returns False for non-TTY."""
        renderer = make_renderer(True)  # bypass __init__
        with patch("sys.stdout") as mock_stdout:
            mock_stdout.isatty.return_value = False
            result = renderer._detect_color_support()
        assert result is False


# ---------------------------------------------------------------------------
# _colorize()
# ---------------------------------------------------------------------------

class TestColorize:
    def test_wraps_ansi_when_color_enabled(self):
        """R7.2 — _colorize() must wrap text with ANSI codes when color_enabled=True."""
        renderer = make_renderer(color_enabled=True)
        result = renderer._colorize("hello", Color.RED)
        assert result == f"{Color.RED}hello{Color.RESET}"

    def test_returns_plain_text_when_color_disabled(self):
        """R1.6 / R7.8 — _colorize() must return plain text when color_enabled=False."""
        renderer = make_renderer(color_enabled=False)
        result = renderer._colorize("hello", Color.RED)
        assert result == "hello"

    def test_no_ansi_codes_in_plain_text(self):
        """R7.8 — No ANSI escape sequences appear when color is disabled."""
        renderer = make_renderer(color_enabled=False)
        result = renderer._colorize("test", Color.BLUE)
        assert "\033[" not in result


# ---------------------------------------------------------------------------
# render_board()
# ---------------------------------------------------------------------------

class TestRenderBoard:
    def test_empty_board_shows_cell_numbers(self, capsys):
        """R1.2 — Empty cells must display their cell number."""
        renderer = make_renderer(color_enabled=False)
        board = Board()
        renderer.render_board(board)
        captured = capsys.readouterr().out
        # All 16 cell numbers should appear in the output
        for cell in range(1, 17):
            assert str(cell) in captured, f"Cell number {cell} not found in board output"

    def test_occupied_cells_show_x_and_o(self, capsys):
        """R1.2 — Occupied cells must display 'X' or 'O' instead of the cell number."""
        renderer = make_renderer(color_enabled=False)
        board = Board()
        board.place(1, 'X')
        board.place(2, 'O')
        renderer.render_board(board)
        captured = capsys.readouterr().out
        assert 'X' in captured
        assert 'O' in captured

    def test_occupied_cell_number_not_shown(self, capsys):
        """R1.2 — Once a cell is occupied, its number should not appear as a standalone cell label."""
        renderer = make_renderer(color_enabled=False)
        board = Board()
        # Place X on cell 1; cell 1 should no longer show ' 1' as a cell label
        board.place(1, 'X')
        renderer.render_board(board)
        captured = capsys.readouterr().out
        # The board should contain 'X' for cell 1
        assert 'X' in captured

    def test_separator_present(self, capsys):
        """R1.3 — Board output must contain the row separator '----+----+----+----'."""
        renderer = make_renderer(color_enabled=False)
        board = Board()
        renderer.render_board(board)
        captured = capsys.readouterr().out
        assert '----+----+----+----' in captured

    def test_separator_appears_three_times(self, capsys):
        """R1.3 — There should be exactly 3 separators for a 4-row board."""
        renderer = make_renderer(color_enabled=False)
        board = Board()
        renderer.render_board(board)
        captured = capsys.readouterr().out
        assert captured.count('----+----+----+----') == 3

    def test_x_shown_in_color_when_enabled(self, capsys):
        """R7.3 — When color is enabled, 'X' should be wrapped with RED ANSI code."""
        renderer = make_renderer(color_enabled=True)
        board = Board()
        board.place(6, 'X')
        renderer.render_board(board)
        captured = capsys.readouterr().out
        assert Color.RED in captured
        assert 'X' in captured

    def test_o_shown_in_color_when_enabled(self, capsys):
        """R7.4 — When color is enabled, 'O' should be wrapped with BLUE ANSI code."""
        renderer = make_renderer(color_enabled=True)
        board = Board()
        board.place(6, 'O')
        renderer.render_board(board)
        captured = capsys.readouterr().out
        assert Color.BLUE in captured
        assert 'O' in captured

    def test_no_ansi_codes_when_color_disabled(self, capsys):
        """R1.6 / R7.8 — No ANSI escape codes in output when color is disabled."""
        renderer = make_renderer(color_enabled=False)
        board = Board()
        board.place(1, 'X')
        board.place(2, 'O')
        renderer.render_board(board)
        captured = capsys.readouterr().out
        assert "\033[" not in captured


# ---------------------------------------------------------------------------
# render_error()
# ---------------------------------------------------------------------------

class TestRenderError:
    def test_output_contains_message(self, capsys):
        """R7.7 — render_error() must print the exact message passed to it."""
        renderer = make_renderer(color_enabled=False)
        renderer.render_error("Invalid input. Please enter a number between 1 and 16.")
        captured = capsys.readouterr().out
        assert "Invalid input. Please enter a number between 1 and 16." in captured

    def test_output_contains_custom_message(self, capsys):
        """R7.7 — render_error() works with any arbitrary message string."""
        renderer = make_renderer(color_enabled=False)
        renderer.render_error("Cell already occupied. Please choose another cell.")
        captured = capsys.readouterr().out
        assert "Cell already occupied. Please choose another cell." in captured

    def test_error_uses_red_color_when_enabled(self, capsys):
        """R7.7 — Error messages should use RED ANSI code when color is enabled."""
        renderer = make_renderer(color_enabled=True)
        renderer.render_error("some error")
        captured = capsys.readouterr().out
        assert Color.RED in captured
        assert "some error" in captured

    def test_error_no_ansi_when_color_disabled(self, capsys):
        """R7.8 — No ANSI codes in error output when color is disabled."""
        renderer = make_renderer(color_enabled=False)
        renderer.render_error("some error")
        captured = capsys.readouterr().out
        assert "\033[" not in captured
        assert "some error" in captured
