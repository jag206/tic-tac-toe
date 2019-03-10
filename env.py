from enum import IntEnum
import numpy as np


class Player(IntEnum):
    UNASSIGNED = 0
    X = 1
    O = 2

class Environment:
    def __init__(self):
        self.board = np.array([Player.UNASSIGNED, Player.UNASSIGNED, Player.UNASSIGNED, Player.UNASSIGNED, Player.UNASSIGNED, Player.UNASSIGNED, Player.UNASSIGNED, Player.UNASSIGNED, Player.UNASSIGNED])
        self.next_go = Player.X

    def _render(self, idx):
        val = self.board[idx]
        if val == Player.UNASSIGNED:
            return " "
        if val == Player.X:
            return "X"
        if val == Player.O:
            return "O"

        raise Exception("Unknown player!")

    def _change_go(self):
        if self.next_go == Player.X:
            self.next_go = Player.O
        elif self.next_go == Player.O:
            self.next_go = Player.X
        else:
            raise Exception("Unknown player!")

    def _check_win(self):
        if self.board[0] == self.board[1] and self.board[1] == self.board[2]:
            if self.board[0] > Player.UNASSIGNED:
                return True

        if self.board[3] == self.board[4] and self.board[4] == self.board[5]:
            if self.board[3] > Player.UNASSIGNED:
                return True

        if self.board[6] == self.board[7] and self.board[7] == self.board[8]:
            if self.board[6] > Player.UNASSIGNED:
                return True

        if self.board[0] == self.board[3] and self.board[3] == self.board[6]:
            if self.board[0] > Player.UNASSIGNED:
                return True

        if self.board[1] == self.board[4] and self.board[4] == self.board[7]:
            if self.board[1] > Player.UNASSIGNED:
                return True

        if self.board[2] == self.board[5] and self.board[5] == self.board[8]:
            if self.board[2] > Player.UNASSIGNED:
                return True

        if self.board[0] == self.board[4] and self.board[4] == self.board[8]:
            if self.board[0] > Player.UNASSIGNED:
                return True

        if self.board[2] == self.board[4] and self.board[4] == self.board[6]:
            if self.board[2] > Player.UNASSIGNED:
                return True

        return False

    def play(self, idx):
        # check if valid
        if self.board[idx] > Player.UNASSIGNED:
            return False, False

        self.board[idx] = self.next_go
        if self._check_win():
            return True, True

        self._change_go()
        return True, False

    def who_next(self):
        if self.next_go == Player.X:
            return "X"
        if self.next_go == Player.O:
            return "O"

        raise Exception("Unknown player!")

    def render(self):
        print(" {} | {} | {} ".format(self._render(0), self._render(1), self._render(2)))
        print("-----------")
        print(" {} | {} | {} ".format(self._render(3), self._render(4), self._render(5)))
        print("-----------")
        print(" {} | {} | {} ".format(self._render(6), self._render(7), self._render(8)))
        print("\n")