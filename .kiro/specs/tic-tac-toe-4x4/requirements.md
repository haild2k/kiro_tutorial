# Requirements Document

## Introduction

Trò chơi Tic-Tac-Toe 4x4 là một trò chơi hai người chơi trên bàn cờ 4x4 ô vuông, chạy hoàn toàn trong terminal. Người chơi lần lượt đặt ký hiệu của mình (X hoặc O) vào các ô trống. Người chơi đầu tiên tạo được 4 ký hiệu liên tiếp theo hàng ngang, hàng dọc hoặc đường chéo sẽ thắng. Trò chơi hỗ trợ màu sắc cơ bản trong terminal để phân biệt người chơi và trạng thái bàn cờ.

## Glossary

- **Game**: Hệ thống trò chơi Tic-Tac-Toe 4x4 chạy trong terminal.
- **Board**: Bàn cờ 4x4 gồm 16 ô được đánh số từ 1 đến 16.
- **Cell**: Một ô đơn lẻ trên Board, có thể trống hoặc chứa ký hiệu của một người chơi.
- **Player**: Người chơi, gồm Player_X (dùng ký hiệu X) và Player_O (dùng ký hiệu O).
- **Move**: Hành động đặt ký hiệu vào một Cell trống trên Board.
- **Win_Condition**: Trạng thái khi một Player có 4 ký hiệu liên tiếp trên cùng hàng ngang, hàng dọc hoặc đường chéo.
- **Draw_Condition**: Trạng thái khi tất cả 16 Cell đã được điền mà không có Player nào đạt Win_Condition.
- **Renderer**: Thành phần chịu trách nhiệm hiển thị Board và thông báo ra terminal với màu sắc.
- **Input_Handler**: Thành phần xử lý đầu vào từ bàn phím của Player.
- **Win_Checker**: Thành phần kiểm tra Win_Condition và Draw_Condition sau mỗi Move.

---

## Requirements

### Requirement 1: Khởi tạo và hiển thị bàn cờ

**User Story:** As a Player, I want to see a clear 4x4 board at the start of the game, so that I can understand the layout and available cells.

#### Acceptance Criteria

1. WHEN a new game session starts, THE Game SHALL initialize a 4x4 Board with 16 empty Cells numbered 1 to 16.
2. WHEN THE Renderer displays the Board, it SHALL show the Cell number for each empty Cell and the player's symbol (X or O) for each occupied Cell.
3. WHEN THE Renderer displays the Board, it SHALL render a visible separator character between each Cell in a row and between each row, such that each Cell boundary is distinguishable.
4. IF color support is active, THEN THE Renderer SHALL render Player_X's symbol (X) and Player_O's symbol (O) in visually different colors.
5. IF color support is active, THEN THE Renderer SHALL render Cell numbers in a color that differs from both Player_X's color and Player_O's color.
6. IF the terminal does not support color, THEN THE Renderer SHALL display the Board using symbols only, without any color formatting.

---

### Requirement 2: Luân phiên lượt chơi

**User Story:** As a Player, I want the game to alternate turns between Player X and Player O, so that both players have equal opportunity to make moves.

#### Acceptance Criteria

1. WHEN a new game session starts, THE Game SHALL assign Player_X as the active player for the first Move.
2. WHEN the active Player places their symbol on an unoccupied Cell, THE Game SHALL transfer the active player role to the other Player.
3. WHEN Player_X is the active player and places their symbol on an unoccupied Cell, THE Game SHALL set Player_O as the next active player.
4. WHEN Player_O is the active player and places their symbol on an unoccupied Cell, THE Game SHALL set Player_X as the next active player.
5. WHEN it is a Player's turn, THE Renderer SHALL display that Player's name and symbol before presenting the Move prompt.
6. IF a Player attempts to make a Move when it is not their turn, THE Game SHALL reject the Move and not change the active player.

---

### Requirement 3: Nhập và xác thực nước đi

**User Story:** As a Player, I want to enter a cell number to place my symbol, so that I can make my move on the board.

#### Acceptance Criteria

1. WHEN it is a Player's turn, THE Input_Handler SHALL prompt the current Player to enter a Cell number between 1 and 16 inclusive.
2. WHEN the Player enters a valid Cell number corresponding to an empty Cell, THE Game SHALL place the Player's symbol in that Cell.
3. IF the Player enters a value that is not an integer, THEN THE Input_Handler SHALL display an error message stating "Invalid input. Please enter a number between 1 and 16." and re-prompt the same Player.
4. IF the Player enters an integer outside the range 1 to 16 inclusive, THEN THE Input_Handler SHALL display an error message stating "Invalid input. Please enter a number between 1 and 16." and re-prompt the same Player.
5. IF any other validation failure occurs for the Player's input, THEN THE Input_Handler SHALL display an error message stating "Invalid input. Please enter a number between 1 and 16." and re-prompt the same Player.
6. IF the Player enters a Cell number corresponding to an already-occupied Cell, THEN THE Input_Handler SHALL display an error message stating "Cell already occupied. Please choose another cell." and re-prompt the same Player.
7. WHEN a valid Move is made, THE Renderer SHALL redisplay the updated Board within 1 second after the Move is applied.

---

### Requirement 4: Phát hiện điều kiện thắng

**User Story:** As a Player, I want the game to detect when I have won, so that the game ends and my victory is announced.

#### Acceptance Criteria

1. WHEN a Player completes a Move, THE Win_Checker SHALL evaluate all 4 rows, all 4 columns, the main diagonal, and the anti-diagonal for a Win_Condition before evaluating for a Draw_Condition.
2. WHEN THE Win_Checker detects 4 consecutive identical symbols in any row of the Board, THE Game SHALL declare the Player who owns that symbol as the winner.
3. WHEN THE Win_Checker detects 4 consecutive identical symbols in any column of the Board, THE Game SHALL declare the Player who owns that symbol as the winner.
4. WHEN THE Win_Checker detects 4 consecutive identical symbols along the main diagonal (top-left to bottom-right) of the Board, THE Game SHALL declare the Player who owns that symbol as the winner.
5. WHEN THE Win_Checker detects 4 consecutive identical symbols along the anti-diagonal (top-right to bottom-left) of the Board, THE Game SHALL declare the Player who owns that symbol as the winner.
6. WHEN a winner is declared, THE Renderer SHALL display a victory message that includes the winning Player's name and symbol, and SHALL render the 4 winning Cells using the winning Player's assigned color.
7. WHEN a winner is declared, THE Game SHALL stop accepting new Moves.
8. WHEN a Move results in no Win_Condition and all 16 Cells are occupied, THE Game SHALL declare a Draw_Condition and stop accepting new Moves.

---

### Requirement 5: Phát hiện điều kiện hòa

**User Story:** As a Player, I want the game to detect a draw, so that the game ends properly when no winner is possible.

#### Acceptance Criteria

1. AFTER each Move is applied, IF all 16 Cells are occupied AND THE Win_Checker has not detected a Win_Condition for either Player, THEN THE Game SHALL declare a Draw_Condition.
2. WHEN a Draw_Condition is declared, THE Renderer SHALL display a message indicating the game ended in a draw, visible as distinct terminal output separate from the Board.
3. WHEN a Draw_Condition is declared, THE Game SHALL stop accepting new Moves.
4. IF a Win_Condition is detected on the same Move that fills the last Cell, THEN THE Game SHALL declare a Win_Condition and SHALL NOT declare a Draw_Condition.

---

### Requirement 6: Kết thúc trò chơi và chơi lại

**User Story:** As a Player, I want to be prompted to play again after the game ends, so that I can start a new game without restarting the program.

#### Acceptance Criteria

1. WHEN the Game ends due to a Win_Condition or Draw_Condition, THE Game SHALL prompt Player_X first, then Player_O, each with the message "Play again? (y/n): ", waiting for a valid response from each before proceeding.
2. WHEN both Player_X and Player_O individually enter "y" or "Y" at the play-again prompt, THE Game SHALL reset the Board to its initial state and start a new game session with Player_X taking the first Move.
3. WHEN either Player_X or Player_O enters "n" or "N" at the play-again prompt, THE Game SHALL display a farewell message and terminate the program.
4. IF a Player enters a value other than "y", "Y", "n", or "N" at the play-again prompt, THEN THE Input_Handler SHALL re-display the prompt "Play again? (y/n): " and discard the invalid input, repeating until a valid response is received.
5. WHEN Player_X enters "y" or "Y" and Player_O enters "n" or "N" (or vice versa), THE Game SHALL display a farewell message and terminate the program.

---

### Requirement 7: Hỗ trợ màu sắc terminal

**User Story:** As a Player, I want the terminal output to use colors, so that I can easily distinguish game elements at a glance.

#### Acceptance Criteria

1. WHEN the Game starts, THE Renderer SHALL detect whether the terminal supports ANSI escape codes and set a color-support flag accordingly.
2. IF color support is active, THEN THE Renderer SHALL use ANSI escape codes to apply color formatting to all colored output.
3. IF color support is active, THEN THE Renderer SHALL display Player_X's symbol (X) in red color.
4. IF color support is active, THEN THE Renderer SHALL display Player_O's symbol (O) in blue color.
5. IF color support is active, THEN THE Renderer SHALL display the current player indicator and turn prompt in yellow color.
6. IF color support is active, THEN THE Renderer SHALL display victory messages in green color.
7. IF color support is active, THEN THE Renderer SHALL display error messages in red color.
8. IF color support is not active, THEN THE Renderer SHALL display all output as plain text without any ANSI escape codes, and all game functionality SHALL remain fully operational.
