"""
test_board.py — Unit tests for the Board class.

Requirements: R1.1, R3.2, R3.6
"""

import pytest
from src.board import Board, EMPTY, SIZE


class TestBoardReset:
    """Tests for Board.reset() — R1.1"""

    def test_reset_clears_all_cells(self):
        """reset() should set every cell back to EMPTY (None)."""
        board = Board()
        board.place(1, 'X')
        board.place(6, 'O')
        board.place(16, 'X')

        board.reset()

        for row in board.grid:
            for cell in row:
                assert cell is EMPTY

    def test_reset_sets_moves_made_to_zero(self):
        """reset() should reset moves_made to 0."""
        board = Board()
        board.place(1, 'X')
        board.place(2, 'O')

        board.reset()

        assert board.moves_made == 0

    def test_reset_on_fresh_board_is_idempotent(self):
        """reset() on an already-empty board should leave it empty."""
        board = Board()
        board.reset()

        assert board.moves_made == 0
        for row in board.grid:
            for cell in row:
                assert cell is EMPTY

    def test_reset_grid_dimensions_preserved(self):
        """After reset(), grid must still be 4×4."""
        board = Board()
        board.place(5, 'X')
        board.reset()

        assert len(board.grid) == SIZE
        for row in board.grid:
            assert len(row) == SIZE


class TestCellToCoords:
    """Tests for Board.cell_to_coords() — R1.1"""

    def test_cell_1_maps_to_top_left(self):
        assert Board.cell_to_coords(1) == (0, 0)

    def test_cell_4_maps_to_top_right(self):
        assert Board.cell_to_coords(4) == (0, 3)

    def test_cell_5_maps_to_second_row_first_col(self):
        assert Board.cell_to_coords(5) == (1, 0)

    def test_cell_16_maps_to_bottom_right(self):
        assert Board.cell_to_coords(16) == (3, 3)

    def test_cell_8_maps_to_second_row_last_col(self):
        assert Board.cell_to_coords(8) == (1, 3)

    def test_cell_9_maps_to_third_row_first_col(self):
        assert Board.cell_to_coords(9) == (2, 0)

    def test_cell_13_maps_to_bottom_left(self):
        assert Board.cell_to_coords(13) == (3, 0)


class TestPlace:
    """Tests for Board.place() — R3.2, R3.6"""

    def test_place_sets_symbol_in_correct_cell(self):
        """place() should store the symbol at the correct grid position."""
        board = Board()
        board.place(6, 'X')

        row, col = Board.cell_to_coords(6)
        assert board.grid[row][col] == 'X'

    def test_place_increments_moves_made(self):
        """place() should increment moves_made by 1 each call."""
        board = Board()
        assert board.moves_made == 0

        board.place(1, 'X')
        assert board.moves_made == 1

        board.place(2, 'O')
        assert board.moves_made == 2

    def test_place_multiple_symbols(self):
        """place() should correctly store different symbols for both players."""
        board = Board()
        board.place(1, 'X')
        board.place(16, 'O')

        assert board.get_symbol(1) == 'X'
        assert board.get_symbol(16) == 'O'

    def test_place_raises_value_error_on_occupied_cell(self):
        """place() should raise ValueError when the cell is already occupied — R3.6"""
        board = Board()
        board.place(5, 'X')

        with pytest.raises(ValueError):
            board.place(5, 'O')

    def test_place_raises_value_error_does_not_change_symbol(self):
        """After a failed place(), the original symbol must remain unchanged."""
        board = Board()
        board.place(5, 'X')

        with pytest.raises(ValueError):
            board.place(5, 'O')

        assert board.get_symbol(5) == 'X'

    def test_place_raises_value_error_does_not_increment_moves(self):
        """After a failed place(), moves_made must not be incremented."""
        board = Board()
        board.place(5, 'X')
        moves_before = board.moves_made

        with pytest.raises(ValueError):
            board.place(5, 'O')

        assert board.moves_made == moves_before


class TestIsEmpty:
    """Tests for Board.is_empty() — R3.2"""

    def test_all_cells_empty_on_new_board(self):
        """Every cell should be empty on a freshly created board."""
        board = Board()
        for cell in range(1, 17):
            assert board.is_empty(cell) is True

    def test_cell_not_empty_after_place(self):
        """is_empty() should return False after a symbol is placed."""
        board = Board()
        board.place(7, 'X')

        assert board.is_empty(7) is False

    def test_other_cells_still_empty_after_place(self):
        """Placing on one cell should not affect other cells."""
        board = Board()
        board.place(7, 'X')

        for cell in range(1, 17):
            if cell != 7:
                assert board.is_empty(cell) is True

    def test_cell_empty_again_after_reset(self):
        """is_empty() should return True for all cells after reset()."""
        board = Board()
        board.place(3, 'O')
        board.reset()

        assert board.is_empty(3) is True


class TestIsFull:
    """Tests for Board.is_full() — R1.1"""

    def test_not_full_on_new_board(self):
        """A new board should not be full."""
        board = Board()
        assert board.is_full() is False

    def test_not_full_with_partial_moves(self):
        """Board should not be full with fewer than 16 moves."""
        board = Board()
        for cell in range(1, 16):  # 15 moves
            symbol = 'X' if cell % 2 == 1 else 'O'
            board.place(cell, symbol)

        assert board.is_full() is False

    def test_full_when_moves_made_equals_16(self):
        """is_full() should return True when all 16 cells are occupied."""
        board = Board()
        symbols = ['X', 'O'] * 8  # alternating, 16 total
        for cell, symbol in zip(range(1, 17), symbols):
            board.place(cell, symbol)

        assert board.moves_made == 16
        assert board.is_full() is True

    def test_not_full_after_reset_from_full(self):
        """After reset(), a previously full board should not be full."""
        board = Board()
        symbols = ['X', 'O'] * 8
        for cell, symbol in zip(range(1, 17), symbols):
            board.place(cell, symbol)

        board.reset()

        assert board.is_full() is False
