from tictactoe import tictactoe
import os


class Game:
    def __init__(self, playerX, playerO):
        self.results = {
            "X": "Player X wins!",
            "O": "Player O wins!",
            "D": "It's a tie!",
        }
        self.game = tictactoe()
        self.players = (playerX, playerO)

    def game_loop(self):
        os.system("cls" if os.name == "nt" else "clear")
        print(self.game.show_board())
        i = 0
        while True:
            if self.game.get_result():
                print(self.results[self.game.get_result()])
                break
            input("press enter")
            self.game.player_move(
                self.players[i % 2].find_move(self.game.get_board()),
                self.players[i % 2].player_type,
            )
            os.system("cls" if os.name == "nt" else "clear")
            print(self.game.show_board())
            i += 1
