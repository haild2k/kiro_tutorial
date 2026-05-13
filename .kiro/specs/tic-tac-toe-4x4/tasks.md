# Implementation Plan: Tic-Tac-Toe 4x4

## Overview

Triển khai trò chơi Tic-Tac-Toe 4x4 bằng Python 3.10+ theo kiến trúc 5 module độc lập. Mỗi task xây dựng tuần tự từ data layer (Board) → logic layer (WinChecker) → I/O layer (Renderer, InputHandler) → orchestration (Game) → entry point (main.py). Tests được viết song song với từng module.

## Tasks

- [-] 1. Thiết lập cấu trúc dự án và khung kiểm thử
  - Tạo thư mục `src/` và `tests/`
  - Tạo các file `src/__init__.py`, `tests/__init__.py` (rỗng) để Python nhận diện package
  - Tạo file `pytest.ini` hoặc `pyproject.toml` cấu hình pytest với `testpaths = tests`
  - _Requirements: R1, R3, R4, R5_

- [ ] 2. Implement Board module
  - [~] 2.1 Implement `src/board.py` — Board class
    - Định nghĩa hằng số `EMPTY = None`, `SIZE = 4`
    - Implement `__init__`: khởi tạo `self.grid` (list 2D 4×4) và `self.moves_made = 0`
    - Implement `reset()`: đặt lại toàn bộ grid về `None`, `moves_made = 0`
    - Implement `cell_to_coords(cell_number)`: chuyển 1–16 → `(row, col)` 0-indexed
    - Implement `coords_to_cell(row, col)`: chuyển `(row, col)` → cell number
    - Implement `is_empty(cell_number)`: trả về `True` nếu cell còn trống
    - Implement `is_full()`: trả về `True` khi `moves_made == 16`
    - Implement `get_symbol(cell_number)`: trả về symbol hoặc `None`
    - Implement `place(cell_number, symbol)`: đặt symbol, tăng `moves_made`, raise `ValueError` nếu đã chiếm
    - _Requirements: R1.1, R3.2, R3.6_

  - [ ]* 2.2 Viết unit tests cho Board
    - Test `reset()` trả về grid trống, `moves_made == 0`
    - Test `cell_to_coords` cho các cell biên: 1→(0,0), 4→(0,3), 5→(1,0), 16→(3,3)
    - Test `place()` thành công và tăng `moves_made`
    - Test `place()` raise `ValueError` khi cell đã chiếm
    - Test `is_empty()` trước và sau khi đặt symbol
    - Test `is_full()` khi `moves_made == 16`
    - _Requirements: R1.1, R3.2, R3.6_

- [ ] 3. Implement WinChecker module
  - [~] 3.1 Implement `src/win_checker.py` — WinChecker + GameResult
    - Định nghĩa `GameResult` dataclass với các field: `status: str`, `winner: str | None`, `winning_cells: list[int]`
    - Implement `_get_all_lines()`: trả về 10 đường (4 hàng, 4 cột, 2 đường chéo) dưới dạng `list[list[int]]`
      - Rows: `[1,2,3,4]`, `[5,6,7,8]`, `[9,10,11,12]`, `[13,14,15,16]`
      - Cols: `[1,5,9,13]`, `[2,6,10,14]`, `[3,7,11,15]`, `[4,8,12,16]`
      - Main diag: `[1,6,11,16]`, Anti diag: `[4,7,10,13]`
    - Implement `_check_line(board, cells)`: kiểm tra 4 cell có cùng symbol không phải `None`; trả về `GameResult(status='win', ...)` hoặc `None`
    - Implement `check(board)`: duyệt tất cả 10 đường theo thứ tự rows→cols→diagonals; nếu không thắng và `board.is_full()` trả về draw; ngược lại trả về ongoing
    - _Requirements: R4.1, R4.2, R4.3, R4.4, R4.5, R5.1, R5.4_

  - [ ]* 3.2 Viết unit tests cho WinChecker
    - Test thắng theo hàng ngang (mỗi hàng)
    - Test thắng theo cột dọc (mỗi cột)
    - Test thắng theo đường chéo chính `[1,6,11,16]`
    - Test thắng theo đường chéo phụ `[4,7,10,13]`
    - Test draw khi board đầy, không ai thắng
    - Test ongoing khi board chưa đầy, chưa thắng
    - Test win ưu tiên hơn draw khi nước cuối vừa thắng vừa lấp đầy board (R5.4)
    - Test `winning_cells` trả về đúng 4 cell numbers
    - _Requirements: R4.1–R4.8, R5.1, R5.4_

- [~] 4. Checkpoint — Đảm bảo Board và WinChecker hoạt động đúng
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 5. Implement Renderer module
  - [~] 5.1 Implement `src/renderer.py` — Color constants + Renderer
    - Định nghĩa class `Color` với các hằng số ANSI: `RED`, `BLUE`, `YELLOW`, `GREEN`, `RESET`
    - Implement `__init__`: gọi `_detect_color_support()` và lưu vào `self.color_enabled`
    - Implement `_detect_color_support()`: kiểm tra `sys.stdout.isatty()`; trên Windows kiểm tra `ANSICON` hoặc `WT_SESSION`; Unix mặc định `True`
    - Implement `_colorize(text, color)`: bọc text với ANSI nếu `color_enabled`, ngược lại trả về text gốc
    - Implement `render_board(board, winning_cells=None)`: in bàn cờ 4×4 với format `  N |  N |  N |  N` và separator `----+----+----+----`; ô trống hiển thị số cell, ô X hiển thị 'X' (đỏ), ô O hiển thị 'O' (xanh); `winning_cells` được highlight màu người thắng
    - Implement `render_turn_prompt(symbol)`: in `"Player X's turn"` bằng màu vàng
    - Implement `render_victory(symbol)`: in thông báo thắng bằng màu xanh lá
    - Implement `render_draw()`: in `"It's a draw!"`
    - Implement `render_error(message)`: in thông báo lỗi bằng màu đỏ
    - Implement `render_farewell()`: in thông báo tạm biệt
    - _Requirements: R1.2, R1.3, R1.4, R1.5, R1.6, R2.5, R4.6, R5.2, R7.1–R7.8_

  - [ ]* 5.2 Viết unit tests cho Renderer
    - Test `_detect_color_support()` trả về `False` khi không phải TTY (mock `sys.stdout.isatty` → `False`)
    - Test `_colorize()` bọc ANSI khi `color_enabled=True`, trả về text gốc khi `False`
    - Test `render_board()` output chứa số cell cho ô trống
    - Test `render_board()` output chứa 'X' và 'O' cho ô đã chiếm
    - Test `render_board()` output chứa separator `----+----+----+----`
    - Test `render_error()` output chứa message được truyền vào
    - _Requirements: R1.2, R1.3, R1.6, R7.1, R7.8_

- [ ] 6. Implement InputHandler module
  - [~] 6.1 Implement `src/input_handler.py` — InputHandler
    - Implement `__init__(renderer)`: lưu `self.renderer`
    - Implement `get_move(board)`: vòng lặp đọc stdin; xử lý `ValueError` (không phải số) → gọi `renderer.render_error("Invalid input. Please enter a number between 1 and 16.")`; ngoài phạm vi 1–16 → cùng thông báo lỗi; ô đã chiếm → `renderer.render_error("Cell already occupied. Please choose another cell.")`; trả về cell number hợp lệ
    - Implement `get_play_again(player_symbol)`: vòng lặp đọc stdin với prompt `"Play again? (y/n): "`; chấp nhận `y/Y` → `True`, `n/N` → `False`; input khác → lặp lại prompt
    - _Requirements: R3.1, R3.2, R3.3, R3.4, R3.5, R3.6, R6.1, R6.4_

  - [ ]* 6.2 Viết unit tests cho InputHandler
    - Test `get_move()` trả về cell hợp lệ khi input đúng (mock `input()`)
    - Test `get_move()` gọi `render_error` và lặp lại khi input không phải số
    - Test `get_move()` gọi `render_error` và lặp lại khi input ngoài phạm vi 1–16
    - Test `get_move()` gọi `render_error` và lặp lại khi cell đã chiếm
    - Test `get_play_again()` trả về `True` với 'y' và 'Y'
    - Test `get_play_again()` trả về `False` với 'n' và 'N'
    - Test `get_play_again()` lặp lại khi input không hợp lệ
    - _Requirements: R3.1–R3.6, R6.1, R6.4_

- [~] 7. Checkpoint — Đảm bảo Renderer và InputHandler hoạt động đúng
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 8. Implement Game module và entry point
  - [~] 8.1 Implement `src/game.py` — Game class
    - Implement `__init__`: khởi tạo `Board`, `WinChecker`, `Renderer`, `InputHandler`; set `self.current_symbol = 'X'`
    - Implement `_switch_player()`: chuyển `current_symbol` từ `'X'` → `'O'` hoặc ngược lại
    - Implement `_ask_play_again()`: gọi `input_handler.get_play_again('X')` rồi `get_play_again('O')`; trả về `True` chỉ khi cả hai đều `True`; nếu Player X từ chối, không hỏi Player O
    - Implement `_play_session()`: reset board, set `current_symbol = 'X'`, render board; vòng lặp: render turn prompt → lấy move → place → check result → render board với winning_cells → nếu win/draw render kết quả và break → switch player
    - Implement `run()`: vòng lặp gọi `_play_session()`; sau mỗi session gọi `_ask_play_again()`; nếu `False` render farewell và break
    - _Requirements: R2.1–R2.6, R4.7, R4.8, R5.3, R6.1–R6.5_

  - [~] 8.2 Implement `src/main.py` — Entry point
    - Import `Game` từ `game`
    - Định nghĩa `main()`: tạo `Game()` và gọi `game.run()`
    - Guard `if __name__ == '__main__': main()`
    - _Requirements: R1.1_

  - [ ]* 8.3 Viết unit tests cho Game
    - Test `_switch_player()`: X→O và O→X
    - Test `_ask_play_again()` trả về `True` khi cả hai đồng ý (mock `get_play_again`)
    - Test `_ask_play_again()` trả về `False` khi Player X từ chối (không gọi Player O)
    - Test `_ask_play_again()` trả về `False` khi Player O từ chối
    - Test `_play_session()` kết thúc khi có người thắng (mock board/win_checker)
    - Test `_play_session()` kết thúc khi hòa (mock board/win_checker)
    - _Requirements: R2.1–R2.4, R4.7, R5.3, R6.1–R6.5_

- [~] 9. Final checkpoint — Đảm bảo toàn bộ test suite pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks đánh dấu `*` là optional, có thể bỏ qua để triển khai MVP nhanh hơn
- Mỗi task tham chiếu đến requirements cụ thể để đảm bảo traceability
- Chạy tests: `python -m pytest tests/`
- Chạy game: `python src/main.py`
- Không có external dependencies — chỉ dùng stdlib Python 3.10+
- Mock `input()` và `sys.stdout` trong tests để tránh phụ thuộc vào terminal thực

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1"] },
    { "id": 1, "tasks": ["2.1"] },
    { "id": 2, "tasks": ["2.2", "3.1"] },
    { "id": 3, "tasks": ["3.2", "5.1"] },
    { "id": 4, "tasks": ["5.2", "6.1"] },
    { "id": 5, "tasks": ["6.2", "8.1"] },
    { "id": 6, "tasks": ["8.2", "8.3"] }
  ]
}
```
