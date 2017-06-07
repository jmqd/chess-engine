import random
import operator

from piece import Color
from position import Position


class ChessEngine:
    def __init__(self, game: object) -> None:
        self.game = game

    def choose_random_move(self) -> tuple:
        move = random.choice(self.game.find_all_legal_moves())
        print("Computer chose this move: {}".format(move))
        return move

    @staticmethod
    def evaluate_position(position: Position) -> float:
        # TODO: continue implementing
        for square in positon:
            if square.is_empty(): continue



