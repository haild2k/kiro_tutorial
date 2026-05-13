# Technical Design Document

## Overview

Trò chơi Tic-Tac-Toe 4x4 được triển khai bằng **Python 3** (không cần thư viện ngoài), chạy hoàn toàn trong terminal. Kiến trúc chia thành 5 module độc lập, mỗi module tương ứng với một thành phần logic trong requirements. Entry point `main.py` chỉ khởi tạo và kết nối các thành phần.

---

## System Architecture

```
main.py
  └── Game
        ├── Board              (trạng thái bàn cờ)
        ├── WinChecker         (kiểm tra thắng/hòa)
        ├── Renderer           (hiển thị terminal + màu ANSI)
        └── InputHandler       (đọc stdin + xác thực)
```

Luồng dữ liệu một chiều: `Game` điều phối, truyền `Board` vào các thành phần khác — không có global state.

---

## Module Design

### 1. `board.py` — Board

Quản lý trạng thái 4×4 grid. Cells được đánh số 1–16, lưu nội bộ dưới dạng list 2D (4×4).

```python
EMPTY = None  # ô trống
SIZE = 4

class Board:
    def __init__(self) -> None:
        # grid[row][col] = None | 'X' | 'O'
        self.grid: list[list[str | None]]
        self.moves_made: int  # đếm số nước đã đi

    def reset(self) -> None:
        """Khởi tạo lại toàn bộ grid về trạng thái trống."""

    def place(self, cell_number: int, symbol: str) -> None:
        """Đặt symbol vào cell. Raises ValueError nếu cell đã chiếm."""

    def is_empty(self, cell_number: int) -> bool:
        """Trả về True nếu cell còn trống."""

    def is_full(self) -> bool:
        """Trả về True khi tất cả 16 cells đã được điền."""

    def get_symbol(self, cell_number: int) -> str | None:
        """Trả về symbol tại cell, hoặc None nếu trống."""

    @staticmethod
    def cell_to_coords(cell_number: int) -> tuple[int, int]:
        """Chuyển đổi cell number (1–16) sang (row, col) 0-indexed."""
        # cell 1 → (0,0), cell 4 → (0,3), cell 5 → (1,0), ...
        row = (cell_number - 1) // SIZE
        col = (cell_number - 1) % SIZE
        return row, col

    @staticmethod
    def coords_to_cell(row: int, col: int) -> int:
        """Chuyển đổi (row, col) sang cell number."""
```

**Mapping cell number → (row, col):**

| Cell | Row | Col |
|------|-----|-----|
| 1–4  | 0   | 0–3 |
| 5–8  | 1   | 0–3 |
| 9–12 | 2   | 0–3 |
| 13–16| 3   | 0–3 |

---

### 2. `win_checker.py` — WinChecker

Kiểm tra Win_Condition và Draw_Condition sau mỗi nước đi. Trả về kết quả dưới dạng `GameResult`.

```python
from dataclasses import dataclass

@dataclass
class GameResult:
    status: str          # 'win' | 'draw' | 'ongoing'
    winner: str | None   # 'X' | 'O' | None
    winning_cells: list[int]  # cell numbers của 4 ô thắng (rỗng nếu không thắng)

class WinChecker:
    def check(self, board: Board) -> GameResult:
        """
        Kiểm tra theo thứ tự: rows → columns → main diagonal → anti-diagonal → draw.
        Trả về GameResult với status phù hợp.
        """

    def _check_line(self, board: Board, cells: list[int]) -> GameResult | None:
        """
        Kiểm tra một đường (4 cells). Trả về GameResult nếu thắng, None nếu không.
        """

    def _get_all_lines(self) -> list[list[int]]:
        """
        Trả về tất cả 10 đường cần kiểm tra:
        - 4 hàng ngang
        - 4 cột dọc
        - 1 đường chéo chính (1,6,11,16)
        - 1 đường chéo phụ (4,7,10,13)
        """
```

**10 đường kiểm tra (cell numbers):**

```
Rows:        [1,2,3,4], [5,6,7,8], [9,10,11,12], [13,14,15,16]
Columns:     [1,5,9,13], [2,6,10,14], [3,7,11,15], [4,8,12,16]
Main diag:   [1,6,11,16]
Anti diag:   [4,7,10,13]
```

---

### 3. `renderer.py` — Renderer

Xử lý toàn bộ output ra terminal. Phát hiện ANSI support khi khởi tạo.

```python
class Color:
    RED    = '\033[91m'
    BLUE   = '\033[94m'
    YELLOW = '\033[93m'
    GREEN  = '\033[92m'
    RESET  = '\033[0m'

class Renderer:
    def __init__(self) -> None:
        self.color_enabled: bool  # True nếu terminal hỗ trợ ANSI

    def _detect_color_support(self) -> bool:
        """
        Kiểm tra sys.stdout.isatty() và platform.
        Trả về False trên Windows nếu không có ANSI support.
        """

    def _colorize(self, text: str, color: str) -> str:
        """Bọc text với ANSI color nếu color_enabled, ngược lại trả về text gốc."""

    def render_board(self, board: Board, winning_cells: list[int] = None) -> None:
        """
        In bàn cờ 4×4 ra terminal.
        - Ô trống: hiển thị cell number (màu trắng/default)
        - Ô X: hiển thị 'X' (đỏ)
        - Ô O: hiển thị 'O' (xanh dương)
        - winning_cells: highlight bằng màu của người thắng
        Format mỗi ô: 2 ký tự (căn phải), ngăn cách bởi ' | '
        Ngăn cách hàng bởi '-----------'
        """

    def render_turn_prompt(self, symbol: str) -> None:
        """In 'Player X's turn' bằng màu vàng."""

    def render_victory(self, symbol: str) -> None:
        """In thông báo thắng bằng màu xanh lá."""

    def render_draw(self) -> None:
        """In "It's a draw!" bằng màu trắng/default."""

    def render_error(self, message: str) -> None:
        """In thông báo lỗi bằng màu đỏ."""

    def render_farewell(self) -> None:
        """In thông báo tạm biệt."""
```

**Board display format (ví dụ):**

```
  1 |  2 |  3 |  4
----+----+----+----
  5 |  X |  7 |  8
----+----+----+----
  9 | 10 | 11 |  O
----+----+----+----
 13 | 14 | 15 | 16
```

---

### 4. `input_handler.py` — InputHandler

Đọc và xác thực đầu vào từ stdin. Không có side effect ngoài print và input().

```python
class InputHandler:
    def __init__(self, renderer: Renderer) -> None:
        self.renderer = renderer  # dùng để in thông báo lỗi

    def get_move(self, board: Board) -> int:
        """
        Vòng lặp cho đến khi nhận được cell number hợp lệ (1–16, ô trống).
        Xử lý:
        - ValueError (không phải số nguyên) → thông báo lỗi range
        - Ngoài phạm vi 1–16 → thông báo lỗi range
        - Ô đã chiếm → thông báo lỗi occupied
        Trả về cell number hợp lệ.
        """

    def get_play_again(self, player_symbol: str) -> bool:
        """
        Hỏi một người chơi có muốn chơi lại không.
        Vòng lặp cho đến khi nhận 'y'/'Y' hoặc 'n'/'N'.
        Trả về True nếu 'y'/'Y', False nếu 'n'/'N'.
        """
```

**Validation logic trong `get_move`:**

```
input → strip → try int() → ValueError? → error "Invalid input..."
                           → value < 1 or > 16? → error "Invalid input..."
                           → board.is_empty(cell)? → False → error "Cell already occupied..."
                           → return cell
```

---

### 5. `game.py` — Game

Điều phối toàn bộ game loop. Không trực tiếp in ra terminal — ủy quyền cho Renderer.

```python
class Game:
    def __init__(self) -> None:
        self.board = Board()
        self.win_checker = WinChecker()
        self.renderer = Renderer()
        self.input_handler = InputHandler(self.renderer)
        self.current_symbol: str  # 'X' hoặc 'O'

    def run(self) -> None:
        """Entry point: chạy vòng lặp game cho đến khi người chơi từ chối chơi lại."""

    def _play_session(self) -> None:
        """
        Một ván chơi hoàn chỉnh:
        1. Reset board, set current_symbol = 'X'
        2. Render board
        3. Vòng lặp:
           a. Render turn prompt
           b. Lấy move từ InputHandler
           c. Đặt symbol lên board
           d. Render board (với winning_cells nếu có)
           e. Kiểm tra GameResult
           f. Nếu win/draw → render kết quả → break
           g. Chuyển lượt
        """

    def _switch_player(self) -> None:
        """Chuyển current_symbol từ 'X' sang 'O' hoặc ngược lại."""

    def _ask_play_again(self) -> bool:
        """
        Hỏi lần lượt Player X rồi Player O.
        Trả về True chỉ khi cả hai đều đồng ý.
        """
```

**Game loop flow:**

```
run()
  └── while True:
        _play_session()
          ├── board.reset()
          ├── renderer.render_board()
          └── while not game_over:
                renderer.render_turn_prompt(symbol)
                cell = input_handler.get_move(board)
                board.place(cell, symbol)
                result = win_checker.check(board)
                renderer.render_board(board, result.winning_cells)
                if result.status == 'win':
                    renderer.render_victory(symbol)
                    break
                elif result.status == 'draw':
                    renderer.render_draw()
                    break
                _switch_player()
        if not _ask_play_again():
            renderer.render_farewell()
            break
```

---

### 6. `main.py` — Entry Point

```python
from game import Game

def main() -> None:
    game = Game()
    game.run()

if __name__ == '__main__':
    main()
```

---

## File Structure

```
src/
  board.py           # Board class
  win_checker.py     # WinChecker + GameResult
  renderer.py        # Renderer + Color constants
  input_handler.py   # InputHandler
  game.py            # Game (game loop)
  main.py            # Entry point
```

---

## Data Flow

```
InputHandler.get_move(board)
    → returns cell: int
    → Game calls board.place(cell, symbol)
    → Game calls win_checker.check(board) → GameResult
    → Game calls renderer.render_board(board, winning_cells)
    → if win/draw: renderer.render_victory/draw()
    → else: game._switch_player()
```

---

## ANSI Color Detection

```python
import sys
import os

def _detect_color_support(self) -> bool:
    # Không phải TTY (pipe/redirect) → không hỗ trợ màu
    if not sys.stdout.isatty():
        return False
    # Windows: kiểm tra ANSICON hoặc Windows Terminal
    if os.name == 'nt':
        return 'ANSICON' in os.environ or 'WT_SESSION' in os.environ
    # Unix/Linux/macOS: mặc định hỗ trợ
    return True
```

---

## Tech Stack

| Item | Choice |
|------|--------|
| Language | Python 3.10+ |
| Dependencies | Không có (stdlib only) |
| Run | `python src/main.py` |
| Test | `python -m pytest tests/` |

---

## Requirements Traceability

| Requirement | Module(s) |
|-------------|-----------|
| R1: Khởi tạo và hiển thị bàn cờ | `Board`, `Renderer` |
| R2: Luân phiên lượt chơi | `Game` |
| R3: Nhập và xác thực nước đi | `InputHandler`, `Renderer` |
| R4: Phát hiện điều kiện thắng | `WinChecker`, `Renderer`, `Game` |
| R5: Phát hiện điều kiện hòa | `WinChecker`, `Renderer`, `Game` |
| R6: Kết thúc và chơi lại | `Game`, `InputHandler` |
| R7: Hỗ trợ màu sắc terminal | `Renderer` |
