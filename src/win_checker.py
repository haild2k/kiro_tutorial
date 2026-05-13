"""
win_checker.py — WinChecker + GameResult for 4x4 Tic-Tac-Toe.

Evaluates win/draw/ongoing conditions after each move by checking
all 10 lines: 4 rows, 4 columns, main diagonal, anti-diagonal.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from board import Board


@dataclass
class GameResult:
    status: str               # 'win' | 'draw' | 'ongoing'
    winner: str | None        # 'X' | 'O' | None
    winning_cells: list[int] = field(default_factory=list)  # 4 cell numbers, empty if no win


class WinChecker:
    def _get_all_lines(self) -> list[list[int]]:
        """Return all 10 lines to check (rows → columns → diagonals)."""
        rows = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16],
        ]
        cols = [
            [1, 5, 9, 13],
            [2, 6, 10, 14],
            [3, 7, 11, 15],
            [4, 8, 12, 16],
        ]
        diagonals = [
            [1, 6, 11, 16],   # main diagonal (top-left → bottom-right)
            [4, 7, 10, 13],   # anti-diagonal (top-right → bottom-left)
        ]
        return rows + cols + diagonals

    def _check_line(self, board: Board, cells: list[int]) -> GameResult | None:
        """Check if all 4 cells in the line share the same non-None symbol.

        Returns a GameResult with status='win' if a winner is found, else None.
        """
        symbols = [board.get_symbol(c) for c in cells]
        first = symbols[0]
        if first is not None and all(s == first for s in symbols):
            return GameResult(status="win", winner=first, winning_cells=list(cells))
        return None

    def check(self, board: Board) -> GameResult:
        """Check the board for win, draw, or ongoing state.

        Evaluation order: rows → columns → diagonals → draw → ongoing.
        Win takes priority over draw (R5.4).
        """
        for line in self._get_all_lines():
            result = self._check_line(board, line)
            if result is not None:
                return result

        if board.is_full():
            return GameResult(status="draw", winner=None, winning_cells=[])

        return GameResult(status="ongoing", winner=None, winning_cells=[])
