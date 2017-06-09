import random
import logging
from operator import __iadd__, __isub__

from piece import Color
from piece import Pawn
from piece import King
from piece import Rook
from piece import Bishop
from piece import Queen
from piece import Knight

from position import Position

EVEN_EVALUATION = 0.0
WHITE = Color.white
BLACK = Color.black

class ChessEngine:
    def __init__(self, game: object) -> None:
        self.game = game

    def choose_random_move(self) -> tuple:
        move = random.choice(self.game.find_all_legal_moves())
        print("Computer chose this move: {}".format(move))
        return move

    @staticmethod
    def evaluate(position: Position) -> float:
        # TODO: continue implementing
        evaluation = EVEN_EVALUATION
        for square in position:
            if square.is_empty(): continue
            reckon = __iadd__ if square.piece.color == WHITE else __isub__
            reckon(evaluation, square.piece.value)
            # TODO: implement positional evaluations
            # reckon(evaluation, evaluate_positionally(square))
        return evaluation

def evaluate_positionally(square: 'Square') -> float:
    evaluation = EVEN_EVALUATION
    if square.piece.__class__ == Pawn:
        # TODO: do the right weighting math here
        evaluation += square.piece.distance_from_promotion(square.index)
