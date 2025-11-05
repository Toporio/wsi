from tictactoe import tictactoe
from minmaxPlayer import minmaxPlayer
import os

"""
only for testing purposes
"""


class Player:
    def __init__(self, player_type):
        self.player_type = player_type

    def find_move(self, current_game_board):
        available_moves = tictactoe(current_game_board).get_available_moves()
        x = int(input("your turn: "))
        return x


results = {"X": "Player X wins!", "O": "Player O wins!", "D": "It's a tie!"}
game = tictactoe()
playerX = minmaxPlayer("O", 2)
playerO = Player("X")
players = (playerO, playerX)

print(game.show_board())
i = 0
while True:
    if game.get_result():
        print(results[game.get_result()])
        break
    game.player_move(
        players[i % 2].find_move(game.get_board()), players[i % 2].player_type
    )
    os.system("cls" if os.name == "nt" else "clear")
    print(game.show_board())
    i += 1
