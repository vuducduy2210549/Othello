from engines import Engine
import random

class RandomEngine(Engine):

    def get_move(self, board, color, move_num=None,
                 time_remaining=None, time_opponent=None):
        legal_moves = board.get_legal_moves(color)

    
        return random.choice(legal_moves)

engine = RandomEngine