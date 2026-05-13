"""
input_handler.py — InputHandler class for 4x4 Tic-Tac-Toe.

Reads and validates player input from stdin. No side effects beyond
print() and input() calls.
"""

from board import Board
from renderer import Renderer

_ERR_INVALID = "Invalid input. Please enter a number between 1 and 16."
_ERR_OCCUPIED = "Cell already occupied. Please choose another cell."


class InputHandler:
    def __init__(self, renderer: Renderer) -> None:
        self.renderer = renderer

    def get_move(self, board: Board) -> int:
        """
        Loop until a valid cell number (1–16, unoccupied) is entered.

        Handles:
        - Non-integer input (ValueError) → render_error with range message
        - Integer outside 1–16 → render_error with range message
        - Already-occupied cell → render_error with occupied message

        Returns the valid cell number.
        """
        while True:
            raw = input("Enter cell number (1-16): ").strip()
            try:
                cell = int(raw)
            except ValueError:
                self.renderer.render_error(_ERR_INVALID)
                continue

            if cell < 1 or cell > 16:
                self.renderer.render_error(_ERR_INVALID)
                continue

            if not board.is_empty(cell):
                self.renderer.render_error(_ERR_OCCUPIED)
                continue

            return cell

    def get_play_again(self, player_symbol: str) -> bool:
        """
        Ask a player whether they want to play again.

        Loops until 'y'/'Y' (returns True) or 'n'/'N' (returns False)
        is entered. Any other input re-displays the prompt.
        """
        while True:
            answer = input("Play again? (y/n): ").strip()
            if answer in ('y', 'Y'):
                return True
            if answer in ('n', 'N'):
                return False
            # Invalid input — silently re-prompt (R6.4)
