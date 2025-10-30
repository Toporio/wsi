class tictactoe:
    """
    board: simple 1d array, cells id from 1 to 9
    """

    def __init__(self, board=[]):
        if len(board) == 0:
            self._board = ["-" for _ in range(9)]
        else:
            self._board = board.copy()

    def player_move(self, player_choice, player):
        if player_choice in self.get_available_moves() and player in ["X", "O"]:
            self._board[player_choice - 1] = player

    def check_draw(self):
        for cell in self.get_board():
            if cell == "-":
                return False
        return True

    def get_available_moves(self):
        return [i for i in range(1, 10) if self.get_cell(i) == "-"]

    def get_result(self):
        if self.check_draw():
            return "D"
        for player in ["X", "O"]:
            if self.check_winner(player):
                return player
        return False

    def check_winner(self, player):
        conditions = [
            (1, 2, 3),
            (4, 5, 6),
            (7, 8, 9),
            (1, 4, 7),
            (2, 5, 8),
            (3, 6, 9),
            (1, 5, 9),
            (3, 5, 7),
        ]
        for condition in conditions:
            if all(self.get_cell(i) == player for i in condition):
                return True
        return False

    def reset_board(self):
        self._board = ["-" for _ in range(9)]

    def get_cell(self, picked_cell):
        return self._board[picked_cell - 1]

    def get_board(self):
        return self._board

    def show_board(self):
        return (
            f" {self.get_cell(1)} | {self.get_cell(2)} | {self.get_cell(3)} \n"
            f"-----------\n"
            f" {self.get_cell(4)} | {self.get_cell(5)} | {self.get_cell(6)} \n"
            f"-----------\n"
            f" {self.get_cell(7)} | {self.get_cell(8)} | {self.get_cell(9)} "
        )

    def __str__(self):
        return str(self._board)
