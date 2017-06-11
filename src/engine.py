import random
import logging
from typing import Dict, Optional
from operator import __iadd__, __isub__, __lt__, __gt__
from collections import namedtuple

from src.piece import Piece
from src.piece import Pawn
from src.piece import King
from src.piece import Rook
from src.piece import Queen
from src.piece import Color
from src.piece import Knight
from src.piece import Bishop
from src.position import Position


EvaluatedPosition = namedtuple('EvaluatedPosition', ['position', 'evaluation'])
EvaluationTree = Optional[Dict[EvaluatedPosition, 'EvaluationTree']]
GET_EVAL = lambda x: x.evaluation

EVEN_EVALUATION = 0.0

DEFAULT_DEPTH = 3
WEIGH_PAWN_POSITION = lambda x: (6 - x) * 0.1
PASSED_PAWN_WEIGHT = 2.0

class ChessEngine:
    def __init__(self, game: object) -> None:
        self.game = game
        self.tree = {}

    def choose_random_move(self) -> 'Move':
        move = random.choice(self.game.position.find_all_legal_moves())
        print("Computer chose this move: {}".format(move))
        return move

    def evaluate(self, position: Position) -> float:
        evaluated_position = self.minimax(position)
        return evaluated_position.evaluation

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

    def get_successor_positons(self, tree: EvaluationTree):
        #TODO
        raise NotImplementedError()

    def minimax(self, position: Position,
            depth: int = DEFAULT_DEPTH, alpha: float = float('-inf'),
            beta: float = float('inf')) -> EvaluatedPosition:
        # terminating base case
        if depth == 0:
            return EvaluatedPosition(position, self._evaluate(position))

        # setting initial best as well as min|max function depending on black or white
        if position.active_player == Color.white:
            best = EvaluatedPosition(None, float('-inf'))
            optimize = max
        elif position.active_player == Color.black:
            best = EvaluatedPosition(None, float('inf'))
            optimize = min

        # meat of the recursion
        for next_position in position.successors():
            best = optimize(best, self.minimax(next_position, depth - 1, alpha, beta),
                    key = GET_EVAL)

            if position.active_player == Color.white:
                alpha = optimize(alpha, best.evaluation)
            elif position.active_player == Color.black:
                beta = optimize(beta, best.evaluation)

            if alpha >= beta:
                break

        return best

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
