from tictactoe import tictactoe
from minmaxPlayer import minmaxPlayer
import os

results = {"X": "Player X wins!", "O": "Player O wins!", "D": "It's a tie!"}
game = tictactoe()
playerX = minmaxPlayer("X", 1)
playerO = minmaxPlayer("O", 1)
players = (playerX, playerO)
os.system("cls" if os.name == "nt" else "clear")
print(game.show_board())
i = 0
while True:
    if game.get_result():
        print(results[game.get_result()])
        break
    input("press enter")
    game.player_move(
        players[i % 2].find_move(game.get_board()), players[i % 2].player_type
    )
    os.system("cls" if os.name == "nt" else "clear")
    print(game.show_board())
    i += 1
