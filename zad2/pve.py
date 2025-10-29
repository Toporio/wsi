from tictactoe import tictactoe
from minmaxPlayer import minmaxPlayer
import os


class Player:
    def __init__(self, player_type):
        self.player_type = player_type

    def find_move(self, current_game_board):
        available_moves = tictactoe(current_game_board).get_available_moves()
        x = 0
        try:
            x = int(input("your turn: "))
        except:
            self.find_move(current_game_board)
        if x not in available_moves:
            self.find_move(current_game_board)
        return x


game = tictactoe()
playerX = minmaxPlayer("X", 1)
playerO = Player("O")
players = (playerX, playerO)

print(game.show_board())
i = 0
while True:
    if game.get_result():
        print("aha")
        game.reset_board()
        i = 0
    game.player_move(
        players[i % 2].find_move(game.get_board()), players[i % 2].player_type
    )
    os.system("cls" if os.name == "nt" else "clear")
    print(game.show_board())
    i += 1
