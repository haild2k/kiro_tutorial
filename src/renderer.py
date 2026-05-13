"""
renderer.py — Renderer class for 4x4 Tic-Tac-Toe.

Handles all terminal output with optional ANSI color support.
"""

import os
import sys

from board import Board


class Color:
    RED    = '\033[91m'
    BLUE   = '\033[94m'
    YELLOW = '\033[93m'
    GREEN  = '\033[92m'
    RESET  = '\033[0m'


class Renderer:
    def __init__(self) -> None:
        self.color_enabled: bool = self._detect_color_support()

    def _detect_color_support(self) -> bool:
        """
        Detect whether the terminal supports ANSI escape codes.

        Returns False when stdout is not a TTY (e.g. piped/redirected).
        On Windows, requires ANSICON or WT_SESSION environment variable.
        On Unix/Linux/macOS, defaults to True when stdout is a TTY.
        """
        if not sys.stdout.isatty():
            return False
        if os.name == 'nt':
            return 'ANSICON' in os.environ or 'WT_SESSION' in os.environ
        return True

    def _colorize(self, text: str, color: str) -> str:
        """Wrap text with ANSI color codes if color is enabled, otherwise return plain text."""
        if self.color_enabled:
            return f"{color}{text}{Color.RESET}"
        return text

    def render_board(self, board: Board, winning_cells: list[int] | None = None) -> None:
        """
        Print the 4×4 board to the terminal.

        - Empty cell: displays cell number (right-aligned in 2 chars)
        - X cell: displays 'X' in red
        - O cell: displays 'O' in blue
        - winning_cells: highlighted in the winner's color

        Format:
          N |  N |  N |  N
        ----+----+----+----
        """
        if winning_cells is None:
            winning_cells = []

        rows = []
        for row in range(4):
            cells = []
            for col in range(4):
                cell_number = Board.coords_to_cell(row, col)
                symbol = board.get_symbol(cell_number)

                if symbol is None:
                    # Empty cell: show cell number, right-aligned in 2 chars
                    cell_str = f"{cell_number:2d}"
                elif symbol == 'X':
                    if cell_number in winning_cells:
                        cell_str = f" {self._colorize('X', Color.RED)}"
                    else:
                        cell_str = f" {self._colorize('X', Color.RED)}"
                else:  # 'O'
                    if cell_number in winning_cells:
                        cell_str = f" {self._colorize('O', Color.BLUE)}"
                    else:
                        cell_str = f" {self._colorize('O', Color.BLUE)}"

                cells.append(cell_str)

            rows.append(' | '.join(cells))

        separator = '----+----+----+----'
        print()
        for i, row_str in enumerate(rows):
            print(row_str)
            if i < 3:
                print(separator)
        print()

    def render_turn_prompt(self, symbol: str) -> None:
        """Print 'Player X's turn' in yellow."""
        message = f"Player {symbol}'s turn"
        print(self._colorize(message, Color.YELLOW))

    def render_victory(self, symbol: str) -> None:
        """Print victory message in green."""
        message = f"Player {symbol} wins!"
        print(self._colorize(message, Color.GREEN))

    def render_draw(self) -> None:
        """Print draw message."""
        print("It's a draw!")

    def render_error(self, message: str) -> None:
        """Print error message in red."""
        print(self._colorize(message, Color.RED))

    def render_farewell(self) -> None:
        """Print farewell message."""
        print("Thanks for playing! Goodbye.")
