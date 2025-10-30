from tictactoe import tictactoe
from minmaxPlayer import minmaxPlayer
from game import Game


def main():
    game = Game(minmaxPlayer("X", 10), minmaxPlayer("O", 10))
    game.game_loop()


if __name__ == "__main__":
    main()
