import random
import operator

from piece import Color

class ChessEngine:
    def __init__(self, game):
        self.game = game

    def choose_random_move(self):
        move = random.choice(self.game.find_all_legal_moves())
        print("Computer chose this move: {}".format(move))
        return move

    @staticmethod
    def evaluate_position(position):
        # TODO: continue implementing
        for square in positon:
            if square.is_empty(): continue



