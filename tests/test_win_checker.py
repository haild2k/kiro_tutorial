"""
test_win_checker.py — Unit tests for WinChecker class.

Covers:
- Win by row (all 4 rows)          — R4.2
- Win by column (all 4 columns)    — R4.3
- Win by main diagonal [1,6,11,16] — R4.4
- Win by anti-diagonal [4,7,10,13] — R4.5
- Draw when board is full, no winner — R4.8, R5.1
- Ongoing when board is not full, no winner — R5.1
- Win takes priority over draw on the last move — R5.4
- winning_cells returns exactly 4 cell numbers — R4.1
"""

import pytest
from board import Board
from win_checker import WinChecker, GameResult


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_board(*moves: tuple[int, str]) -> Board:
    """Create a Board and place the given (cell, symbol) pairs in order."""
    board = Board()
    for cell, symbol in moves:
        board.place(cell, symbol)
    return board


def fill_board_no_winner(board: Board) -> None:
    """Fill all 16 cells with a pattern that produces no winner.

    Pattern (X=X, O=O):
      X X O O
      O O X X
      X X O O
      O O X X
    Cells:  1  2  3  4
            5  6  7  8
            9 10 11 12
           13 14 15 16

    Verification — no 4-in-a-row on any line:
      Rows:    XXOO, OOXX, XXOO, OOXX  — no 4 same
      Cols:    XOOX, XOOX, OXOX... wait, let's verify manually.
      Col1: 1X,5O,9X,13O → XOXO ✓
      Col2: 2X,6O,10X,14O → XOXO ✓
      Col3: 3O,7X,11O,15X → OXOX ✓
      Col4: 4O,8X,12O,16X → OXOX ✓
      Main diag [1,6,11,16]: X,O,O,X → XOOX ✓
      Anti diag [4,7,10,13]: O,X,X,O → OXXO ✓
    """
    pattern = [
        (1, "X"), (2, "X"), (3, "O"), (4, "O"),
        (5, "O"), (6, "O"), (7, "X"), (8, "X"),
        (9, "X"), (10, "X"), (11, "O"), (12, "O"),
        (13, "O"), (14, "O"), (15, "X"), (16, "X"),
    ]
    for cell, symbol in pattern:
        board.place(cell, symbol)


# ---------------------------------------------------------------------------
# Win by row — R4.2
# ---------------------------------------------------------------------------

class TestWinByRow:
    def setup_method(self):
        self.checker = WinChecker()

    def test_win_row_1(self):
        """Row 1: cells [1,2,3,4] — R4.2"""
        board = make_board((1, "X"), (2, "X"), (3, "X"), (4, "X"))
        result = self.checker.check(board)
        assert result.status == "win"
        assert result.winner == "X"
        assert sorted(result.winning_cells) == [1, 2, 3, 4]

    def test_win_row_2(self):
        """Row 2: cells [5,6,7,8] — R4.2"""
        board = make_board((5, "O"), (6, "O"), (7, "O"), (8, "O"))
        result = self.checker.check(board)
        assert result.status == "win"
        assert result.winner == "O"
        assert sorted(result.winning_cells) == [5, 6, 7, 8]

    def test_win_row_3(self):
        """Row 3: cells [9,10,11,12] — R4.2"""
        board = make_board((9, "X"), (10, "X"), (11, "X"), (12, "X"))
        result = self.checker.check(board)
        assert result.status == "win"
        assert result.winner == "X"
        assert sorted(result.winning_cells) == [9, 10, 11, 12]

    def test_win_row_4(self):
        """Row 4: cells [13,14,15,16] — R4.2"""
        board = make_board((13, "O"), (14, "O"), (15, "O"), (16, "O"))
        result = self.checker.check(board)
        assert result.status == "win"
        assert result.winner == "O"
        assert sorted(result.winning_cells) == [13, 14, 15, 16]


# ---------------------------------------------------------------------------
# Win by column — R4.3
# ---------------------------------------------------------------------------

class TestWinByColumn:
    def setup_method(self):
        self.checker = WinChecker()

    def test_win_col_1(self):
        """Column 1: cells [1,5,9,13] — R4.3"""
        board = make_board((1, "X"), (5, "X"), (9, "X"), (13, "X"))
        result = self.checker.check(board)
        assert result.status == "win"
        assert result.winner == "X"
        assert sorted(result.winning_cells) == [1, 5, 9, 13]

    def test_win_col_2(self):
        """Column 2: cells [2,6,10,14] — R4.3"""
        board = make_board((2, "O"), (6, "O"), (10, "O"), (14, "O"))
        result = self.checker.check(board)
        assert result.status == "win"
        assert result.winner == "O"
        assert sorted(result.winning_cells) == [2, 6, 10, 14]

    def test_win_col_3(self):
        """Column 3: cells [3,7,11,15] — R4.3"""
        board = make_board((3, "X"), (7, "X"), (11, "X"), (15, "X"))
        result = self.checker.check(board)
        assert result.status == "win"
        assert result.winner == "X"
        assert sorted(result.winning_cells) == [3, 7, 11, 15]

    def test_win_col_4(self):
        """Column 4: cells [4,8,12,16] — R4.3"""
        board = make_board((4, "O"), (8, "O"), (12, "O"), (16, "O"))
        result = self.checker.check(board)
        assert result.status == "win"
        assert result.winner == "O"
        assert sorted(result.winning_cells) == [4, 8, 12, 16]


# ---------------------------------------------------------------------------
# Win by diagonal — R4.4, R4.5
# ---------------------------------------------------------------------------

class TestWinByDiagonal:
    def setup_method(self):
        self.checker = WinChecker()

    def test_win_main_diagonal(self):
        """Main diagonal: cells [1,6,11,16] — R4.4"""
        board = make_board((1, "X"), (6, "X"), (11, "X"), (16, "X"))
        result = self.checker.check(board)
        assert result.status == "win"
        assert result.winner == "X"
        assert sorted(result.winning_cells) == [1, 6, 11, 16]

    def test_win_anti_diagonal(self):
        """Anti-diagonal: cells [4,7,10,13] — R4.5"""
        board = make_board((4, "O"), (7, "O"), (10, "O"), (13, "O"))
        result = self.checker.check(board)
        assert result.status == "win"
        assert result.winner == "O"
        assert sorted(result.winning_cells) == [4, 7, 10, 13]


# ---------------------------------------------------------------------------
# Draw — R4.8, R5.1
# ---------------------------------------------------------------------------

class TestDraw:
    def setup_method(self):
        self.checker = WinChecker()

    def test_draw_when_board_full_no_winner(self):
        """Board full with no winner → draw — R4.8, R5.1"""
        board = Board()
        fill_board_no_winner(board)
        assert board.is_full()
        result = self.checker.check(board)
        assert result.status == "draw"
        assert result.winner is None
        assert result.winning_cells == []

    def test_draw_result_has_no_winning_cells(self):
        """Draw result must have empty winning_cells — R5.1"""
        board = Board()
        fill_board_no_winner(board)
        result = self.checker.check(board)
        assert result.winning_cells == []


# ---------------------------------------------------------------------------
# Ongoing — R5.1
# ---------------------------------------------------------------------------

class TestOngoing:
    def setup_method(self):
        self.checker = WinChecker()

    def test_ongoing_empty_board(self):
        """Empty board → ongoing — R5.1"""
        board = Board()
        result = self.checker.check(board)
        assert result.status == "ongoing"
        assert result.winner is None

    def test_ongoing_partial_board_no_winner(self):
        """Partially filled board with no winner → ongoing — R5.1"""
        board = make_board((1, "X"), (2, "O"), (3, "X"))
        result = self.checker.check(board)
        assert result.status == "ongoing"
        assert result.winner is None

    def test_ongoing_result_has_no_winning_cells(self):
        """Ongoing result must have empty winning_cells — R5.1"""
        board = make_board((1, "X"), (6, "O"))
        result = self.checker.check(board)
        assert result.winning_cells == []


# ---------------------------------------------------------------------------
# Win takes priority over draw on the last move — R5.4
# ---------------------------------------------------------------------------

class TestWinPriorityOverDraw:
    def setup_method(self):
        self.checker = WinChecker()

    def test_win_on_last_move_not_draw(self):
        """Win on the move that fills the last cell → win, not draw — R5.4

        Fill 15 cells with a no-winner pattern, then place the 16th cell
        so that it completes a winning line.

        Board layout (X=X, O=O, last move = cell 16 = X):
          X  O  X  O
          O  X  O  X
          X  O  X  O
          O  X  O  X  ← cell 16 completes main diagonal? No.

        Instead use a targeted setup:
          Place X on cells 1, 6, 11 (3/4 of main diagonal).
          Fill remaining 12 cells with alternating O/X to avoid any other win.
          Last move: X on cell 16 → completes main diagonal [1,6,11,16].
        """
        board = Board()
        # Place 3 corners of main diagonal for X
        board.place(1, "X")
        board.place(6, "X")
        board.place(11, "X")
        # Fill the other 12 cells (all except cell 16) without creating a win
        # Use O for cells that would otherwise form a line, X elsewhere safely
        other_cells_symbols = [
            (2, "O"), (3, "O"), (4, "O"),
            (5, "O"), (7, "O"), (8, "O"),
            (9, "O"), (10, "O"), (12, "O"),
            (13, "O"), (14, "O"), (15, "O"),
        ]
        for cell, sym in other_cells_symbols:
            board.place(cell, sym)

        # Board should have 15 moves, not full yet
        assert board.moves_made == 15
        assert not board.is_full()

        # Place the last cell — completes main diagonal [1,6,11,16] for X
        board.place(16, "X")
        assert board.is_full()

        result = self.checker.check(board)
        assert result.status == "win", (
            f"Expected 'win' but got '{result.status}' — win must take priority over draw (R5.4)"
        )
        assert result.winner == "X"
        assert sorted(result.winning_cells) == [1, 6, 11, 16]


# ---------------------------------------------------------------------------
# winning_cells correctness — R4.1
# ---------------------------------------------------------------------------

class TestWinningCells:
    def setup_method(self):
        self.checker = WinChecker()

    def test_winning_cells_has_exactly_4_cells_row(self):
        """winning_cells contains exactly 4 cell numbers for a row win — R4.1"""
        board = make_board((1, "X"), (2, "X"), (3, "X"), (4, "X"))
        result = self.checker.check(board)
        assert len(result.winning_cells) == 4

    def test_winning_cells_has_exactly_4_cells_col(self):
        """winning_cells contains exactly 4 cell numbers for a column win — R4.1"""
        board = make_board((1, "O"), (5, "O"), (9, "O"), (13, "O"))
        result = self.checker.check(board)
        assert len(result.winning_cells) == 4

    def test_winning_cells_has_exactly_4_cells_main_diag(self):
        """winning_cells contains exactly 4 cell numbers for main diagonal win — R4.1"""
        board = make_board((1, "X"), (6, "X"), (11, "X"), (16, "X"))
        result = self.checker.check(board)
        assert len(result.winning_cells) == 4

    def test_winning_cells_has_exactly_4_cells_anti_diag(self):
        """winning_cells contains exactly 4 cell numbers for anti-diagonal win — R4.1"""
        board = make_board((4, "O"), (7, "O"), (10, "O"), (13, "O"))
        result = self.checker.check(board)
        assert len(result.winning_cells) == 4

    def test_winning_cells_values_are_valid_cell_numbers(self):
        """All winning_cells values must be valid cell numbers (1–16) — R4.1"""
        board = make_board((5, "X"), (6, "X"), (7, "X"), (8, "X"))
        result = self.checker.check(board)
        assert all(1 <= c <= 16 for c in result.winning_cells)

    def test_winning_cells_empty_for_draw(self):
        """winning_cells is empty for a draw result — R4.8"""
        board = Board()
        fill_board_no_winner(board)
        result = self.checker.check(board)
        assert result.winning_cells == []

    def test_winning_cells_empty_for_ongoing(self):
        """winning_cells is empty for an ongoing result — R5.1"""
        board = make_board((1, "X"), (2, "O"))
        result = self.checker.check(board)
        assert result.winning_cells == []
