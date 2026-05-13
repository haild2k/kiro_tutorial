"""
game.py — Game class for 4x4 Tic-Tac-Toe.

Orchestrates the full game loop: session management, turn alternation,
win/draw detection, and play-again flow. Delegates all I/O to Renderer
and InputHandler.
"""

from board import Board
from input_handler import InputHandler
from renderer import Renderer
from win_checker import WinChecker


class Game:
    def __init__(self) -> None:
        self.board = Board()
        self.win_checker = WinChecker()
        self.renderer = Renderer()
        self.input_handler = InputHandler(self.renderer)
        self.current_symbol: str = 'X'

    def _switch_player(self) -> None:
        """Toggle current_symbol between 'X' and 'O'."""
        self.current_symbol = 'O' if self.current_symbol == 'X' else 'X'

    def _ask_play_again(self) -> bool:
        """
        Ask Player X then Player O whether they want to play again.

        Returns True only if both agree. If Player X declines, Player O
        is not asked (R6.1, R6.3, R6.5).
        """
        x_wants = self.input_handler.get_play_again('X')
        if not x_wants:
            return False
        o_wants = self.input_handler.get_play_again('O')
        return o_wants

    def _play_session(self) -> None:
        """
        Run a single complete game session.

        1. Reset board and set Player X as the first mover (R2.1).
        2. Render the initial board.
        3. Loop:
           a. Render turn prompt (R2.5).
           b. Get a valid move from InputHandler.
           c. Place the symbol on the board.
           d. Check for win/draw.
           e. Render the updated board (with winning_cells if applicable).
           f. If win or draw, render the result and break (R4.7, R4.8, R5.3).
           g. Otherwise switch player (R2.2–R2.4).
        """
        self.board.reset()
        self.current_symbol = 'X'
        self.renderer.render_board(self.board)

        while True:
            # a. Show whose turn it is
            self.renderer.render_turn_prompt(self.current_symbol)

            # b. Get a valid move
            cell = self.input_handler.get_move(self.board)

            # c. Place the symbol
            self.board.place(cell, self.current_symbol)

            # d. Evaluate the board
            result = self.win_checker.check(self.board)

            # e. Render updated board (highlight winning cells when present)
            self.renderer.render_board(self.board, result.winning_cells)

            # f. End session on win or draw
            if result.status == 'win':
                self.renderer.render_victory(self.current_symbol)
                break
            elif result.status == 'draw':
                self.renderer.render_draw()
                break

            # g. Hand off to the other player
            self._switch_player()

    def run(self) -> None:
        """
        Main entry point: run game sessions until players choose to stop.

        After each session, ask both players if they want to play again
        (R6.1–R6.5). If either declines, display a farewell message and exit.
        """
        while True:
            self._play_session()
            if not self._ask_play_again():
                self.renderer.render_farewell()
                break
