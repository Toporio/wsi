from tictactoe import tictactoe
from minmaxPlayer import minmaxPlayer
from game import Game


def main():
    d = 2
    game = Game(minmaxPlayer("X", d), minmaxPlayer("O", d))
    game.game_loop()


if __name__ == "__main__":
    main()
