import random
import logging
from typing import Dict, Optional, List, Any
from operator import __iadd__, __isub__, __lt__, __gt__
from collections import namedtuple, defaultdict

from src.piece import Piece
from src.piece import Pawn
from src.piece import King
from src.piece import Rook
from src.piece import Queen
from src.piece import Color
from src.piece import Knight
from src.piece import Bishop
from src.position import Position


GET_EVAL = lambda x: x['evaluation']

EVEN_EVALUATION = 0.0

DEFAULT_DEPTH = 5
WEIGH_PAWN_POSITION = lambda x: (6 - x) * 0.1
PASSED_PAWN_WEIGHT = 2.0

class ChessEngine:
    def __init__(self, game: object) -> None:
        self.game = game
        self.tree = defaultdict(list)

    def choose_random_move(self) -> 'Move':
        move = random.choice(self.game.position.find_all_legal_moves())
        print("Computer chose this move: {}".format(move))
        return move

    def evaluate(self, position: Position) -> float:
        if position not in self.tree:
            pruned_tree = None

            for prev_pos, prev_move_tree in self.tree.items():
                if position in prev_move_tree:
                    pruned_tree = prev_move_tree[position]

            if pruned_tree is not None:
                self.tree = pruned_tree

        evaluated_position = self.minimax(position)
        return evaluated_position

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

    def minimax(self, position: 'Position',
            depth: int = DEFAULT_DEPTH, alpha: float = float('-inf'),
            beta: float = float('inf')) -> Position:

        if position in self.tree:
            return position

        # terminating base case
        if depth == 0:
            position.evaluation = self._evaluate(position)
            position.depth = depth
            return position

        # setting initial best as well as min|max function depending on black or white
        if position.active_player == Color.white:
            best = float('-inf')
            optimize = max

        elif position.active_player == Color.black:
            best = float('inf')
            optimize = min

        # meat of the recursion
        if position not in self.tree:
            self.tree[position] = position.successors()

        for next_position in self.tree[position]:
            if next_position in self.tree:
                continue

            best_leaf = self.minimax(
                    next_position,
                    depth = depth - 1,
                    alpha = alpha,
                    beta = beta)
            best = optimize(best, best_leaf.evaluation)

            if position.active_player == Color.white:
                alpha = optimize(alpha, best)

            elif position.active_player == Color.black:
                beta = optimize(beta, best)

            if alpha >= beta:
                break

        position.evaluation = best
        position.depth = max(position.depth, depth) if position.depth is not None else depth
        return position

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

