"""
board.py — Board class for 4x4 Tic-Tac-Toe.

Manages the 4×4 grid state. Cells are numbered 1–16, stored internally
as a 2D list (4×4).
"""

EMPTY = None
SIZE = 4


class Board:
    def __init__(self) -> None:
        # grid[row][col] = None | 'X' | 'O'
        self.grid: list[list[str | None]] = [[EMPTY] * SIZE for _ in range(SIZE)]
        self.moves_made: int = 0

    def reset(self) -> None:
        """Reset the entire grid to empty state and moves_made to 0."""
        self.grid = [[EMPTY] * SIZE for _ in range(SIZE)]
        self.moves_made = 0

    @staticmethod
    def cell_to_coords(cell_number: int) -> tuple[int, int]:
        """Convert cell number (1–16) to (row, col) 0-indexed.

        cell 1 → (0, 0), cell 4 → (0, 3), cell 5 → (1, 0), cell 16 → (3, 3)
        """
        row = (cell_number - 1) // SIZE
        col = (cell_number - 1) % SIZE
        return row, col

    @staticmethod
    def coords_to_cell(row: int, col: int) -> int:
        """Convert (row, col) 0-indexed to cell number (1–16)."""
        return row * SIZE + col + 1

    def is_empty(self, cell_number: int) -> bool:
        """Return True if the cell is unoccupied."""
        row, col = Board.cell_to_coords(cell_number)
        return self.grid[row][col] is EMPTY

    def is_full(self) -> bool:
        """Return True when all 16 cells have been filled."""
        return self.moves_made == SIZE * SIZE

    def get_symbol(self, cell_number: int) -> str | None:
        """Return the symbol at the given cell, or None if empty."""
        row, col = Board.cell_to_coords(cell_number)
        return self.grid[row][col]

    def place(self, cell_number: int, symbol: str) -> None:
        """Place symbol on the cell and increment moves_made.

        Raises:
            ValueError: if the cell is already occupied.
        """
        if not self.is_empty(cell_number):
            raise ValueError(
                f"Cell {cell_number} is already occupied by '{self.get_symbol(cell_number)}'."
            )
        row, col = Board.cell_to_coords(cell_number)
        self.grid[row][col] = symbol
        self.moves_made += 1
