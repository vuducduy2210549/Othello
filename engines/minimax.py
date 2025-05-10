from engines import Engine
from copy import deepcopy

class MiniMaxEngine(Engine):
    def __init__(self):
        self.alpha_beta = False
        print("Call normal Min max\n")

    def get_move(self, board, color, move_num=None,
                 time_remaining=None, time_opponent=None):
        moves = board.get_legal_moves(color)
        return max(moves, key=lambda move: self._get_cost(board, color, move))

    def _get_cost(self, board, color, move):

        newboard = deepcopy(board)
        newboard.execute_move(move, color)

        num_pieces_op = len(newboard.get_squares(color*-1))
        num_pieces_me = len(newboard.get_squares(color))

        return num_pieces_me - num_pieces_op

engine = MiniMaxEngine
