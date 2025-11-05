from tictactoe import tictactoe
from math import inf
import random


class minmaxPlayer:
    """
    player_type: X or O
    Player X  -> max function
    Player O  -> min function
    """

    def __init__(self, player_type, depth):
        self.cells_value = [3, 2, 3, 2, 4, 2, 3, 2, 3]
        self.depth = depth
        self.score_table = {"D": 0, "X": 100, "O": -100}
        if player_type == "X":
            self.player_type = player_type
            self.is_maximizing = True
        elif player_type == "O":
            self.player_type = player_type
            self.is_maximizing = False
        else:
            raise ValueError("wrong player")

    def find_move(self, current_board_state):
        best_score = -inf if self.is_maximizing else inf
        best_move = None
        for i in range(9):
            if current_board_state[i] == "-":
                current_board_state[i] = self.player_type
                score = self.minmax(
                    current_board_state, not self.is_maximizing, self.depth
                )
                current_board_state[i] = "-"

                if self.is_maximizing and score > best_score:
                    best_score = score
                    best_move = i
                elif not self.is_maximizing and score < best_score:
                    best_score = score
                    best_move = i

        return best_move + 1

    def eval_board(self, board_game):
        result = 0
        for i in range(9):
            if board_game[i] == "X":
                result += self.cells_value[i]
            if board_game[i] == "O":
                result -= self.cells_value[i]
        return result

    def minmax(self, board_game, is_maximizing, depth):
        result = tictactoe(board_game).get_result()
        current_player = "X" if is_maximizing else "O"

        if result:
            return self.score_table[result]
        if depth == 1:
            return self.eval_board(board_game)
        if is_maximizing:
            best_score = -inf
            for i in range(9):
                if board_game[i] == "-":
                    board_game[i] = current_player
                    score = self.minmax(board_game, False, depth - 1)
                    board_game[i] = "-"
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = inf
            for i in range(9):
                if board_game[i] == "-":
                    board_game[i] = current_player
                    score = self.minmax(board_game, True, depth - 1)
                    board_game[i] = "-"
                    best_score = min(score, best_score)
            return best_score
