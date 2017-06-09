import random
import logging
from operator import __iadd__, __isub__

from piece import Piece
from piece import Pawn
from piece import King
from piece import Rook
from piece import Queen
from piece import Color
from piece import Knight
from piece import Bishop

from position import Position

EVEN_EVALUATION = 0.0

DEFAULT_DEPTH = 2
WEIGH_PAWN_POSITION = lambda x: (6 - x) * 0.1
PASSED_PAWN_WEIGHT = 2.0

class ChessEngine:
    def __init__(self, game: object) -> None:
        self.game = game

    def choose_random_move(self) -> tuple:
        move = random.choice(self.game.position.find_all_legal_moves())
        print("Computer chose this move: {}".format(move))
        return move

    def evaluate(self, position: Position) -> float:
        result = self.minimax(position)
        print(result[1])
        return result[0]

    @staticmethod
    def _evaluate(position: Position) -> float:
        # TODO: continue implementing
        evaluation = EVEN_EVALUATION
        for square in position:
            if square.is_empty(): continue
            reckon = __iadd__ if square.piece.color == Color.white else __isub__
            evaluation = reckon(evaluation, square.piece.value)
            evaluation = reckon(evaluation, evaluate_positionally(square, position))
        return evaluation

    def minimax(self, position: Position, depth: int = DEFAULT_DEPTH):
        if depth == 0:
            return self._evaluate(position), position

        if self.game.active_player == Color.white:
            max_eval = float('-inf')
            for next_position in position.successors():
                max_local = self.minimax(next_position, depth - 1)
                max_eval = max(max_local[0], max_eval)
            return max_eval, position

        if self.game.active_player == Color.black:
            max_eval = float('inf')
            for next_position in position.successors():
                max_local = self.minimax(next_position, depth - 1)
                max_eval = min(max_local[0], max_eval)
            return max_eval, position

def evaluate_positionally(square: 'Square', position: Position) -> float:
    # TODO: implement positional evaluations
    evaluation = EVEN_EVALUATION
    if square.piece.__class__ == Pawn:
        evaluation += evaluate_pawn_positionally(square.piece, position)
    return evaluation

def evaluate_pawn_positionally(pawn: Piece, position: Position) -> float:
    evaluation = WEIGH_PAWN_POSITION(pawn.distance_from_promotion())

    # TODO
    is_passed_pawn = False

    if is_passed_pawn:
        # TODO
        evaluation *= PASSED_PAWN_WEIGHT

    return evaluation
