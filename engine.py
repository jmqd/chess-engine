import random
import operator
import logging

from piece import Color
from position import Position

EVEN_EVALUATION = 0.0

class ChessEngine:
    def __init__(self, game: object) -> None:
        self.game = game

    def choose_random_move(self) -> tuple:
        move = random.choice(self.game.find_all_legal_moves())
        print("Computer chose this move: {}".format(move))
        return move

    @staticmethod
    def evaluate_position_materially(position: Position) -> float:
        # TODO: continue implementing
        evaluation = EVEN_EVALUATION
        for square in position:
            if square.is_empty():
                logging.info("empty square")
                continue
            if square.piece.color == Color.white:
                logging.info('white %s, adding %s', square.piece, square.piece.value)
                evaluation += square.piece.value
            if square.piece.color == Color.black:
                logging.info('black %s, subtracting %s', square.piece, square.piece.value)
                evaluation -= square.piece.value
        return evaluation

