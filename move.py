import abc
import logging
from typing import Sequence

from piece import Color

from util import get_move_facts
from util import is_valid_move
from util import to_algebraic

DOWN = 8
RIGHT = 1
UP = DOWN * -1
LEFT = RIGHT * -1
DOWN_RIGHT = DOWN + RIGHT
DOWN_LEFT = DOWN + LEFT
UP_LEFT = UP + LEFT
UP_RIGHT = UP + RIGHT

class Move:
    def __init__(self, origin: int, delta: int) -> None:
        self.origin = origin
        self.delta = delta

        (self.destination,
        self.origin_col,
        self.destination_col,
        self.dx,
        self.dy) = get_move_facts(origin, delta)

    def __str__(self):
        return '{} {}'.format(to_algebraic(self.origin), to_algebraic(self.destination))

class LegalMoveStrategy(metaclass = abc.ABCMeta):
    def __init__(self, game, square):
        self.game = game
        self.square = square
        self.piece = self.square.piece

    @staticmethod
    def of(piece: 'Piece') -> 'LegalMoveStrategy':
        return PIECE_STRATEGY_MAPPING[piece.name]

    def is_in_check(self) -> bool:
        move = self.move
        proposed_position = self.game.position.get_transposition(move)
        if proposed_position.is_in_check(self.game.active_player):
            return True
        return False

    def is_legal(self, move: Move) -> bool:
        '''A base implementation of is_legal. Can be overridden for exception pieces.'''
        square_if_moved, current_col, col_if_moved, col_dist_if_moved, row_dist = get_move_facts(self.square.index, move)
        default_legal_move_invariants = (
                is_valid_move(self.square.index, move),
                self.game.is_empty_or_capturable(square_if_moved),
                self.game.position.is_path_clear(self.square.index, move)
                )

        return all(default_legal_move_invariants)

    def get_legal_moves(self) -> Sequence[int]:
        pos = self.square.index
        return set(pos + move for move in self.get_potential_moves() if self.is_legal(move))

class RayPieceStrategyMixin:
    def get_legal_moves(self) -> Sequence[int]:
        pos = self.square.index
        return set(pos + move for move in self.get_potential_moves(pos) if self.is_legal(move))


#TODO: lots of repetition here. Use mixins. Clean it up.

class BishopLegalMoveStrategy(RayPieceStrategyMixin, LegalMoveStrategy):
    @staticmethod
    def get_potential_moves(square_index: int) -> Sequence[int]:
        return get_diagonal_moves(square_index)

class RookLegalMoveStrategy(RayPieceStrategyMixin, LegalMoveStrategy):
    @staticmethod
    def get_potential_moves(square_index: int) -> Sequence[int]:
        return get_horizontal_moves(square_index) | get_vertical_moves(square_index)

class QueenLegalMoveStrategy(RayPieceStrategyMixin, LegalMoveStrategy):
    @staticmethod
    def get_potential_moves(square_index: int) -> Sequence[int]:
        return (get_diagonal_moves(square_index)
                | get_horizontal_moves(square_index)
                | get_vertical_moves(square_index))


class KnightLegalMoveStrategy(LegalMoveStrategy):
    def is_legal(self, move: Move) -> bool:
        square_if_moved, current_col, col_if_moved, col_dist_if_moved, row_dist = get_move_facts(self.square.index, move)
        expected_col_difference = 1 if row_dist == 2 else 2

        try:
            legal_knight_move_invariants = (
                    row_dist in (1, 2),
                    abs(col_if_moved - current_col) == expected_col_difference,
                    is_valid_move(self.square.index, move),
                    self.game.is_empty_or_capturable(square_if_moved)
                    )
        except IndexError as e:
            return False

        return all(legal_knight_move_invariants)

    def get_potential_moves(self) -> Sequence[int]:
        return {UP_LEFT + LEFT, UP + UP_LEFT, UP_RIGHT + RIGHT,
                UP + UP_RIGHT, RIGHT + DOWN_RIGHT, DOWN_RIGHT + DOWN,
                DOWN + DOWN_LEFT, LEFT + DOWN_LEFT}


class PawnLegalMoveStrategy(LegalMoveStrategy):
    def is_legal(self, move: Move) -> bool:
        square_if_moved, current_col, col_if_moved, col_dist_if_moved, row_dist = get_move_facts(self.square.index, move)
        if col_dist_if_moved == 0:
            pawn_move_invariants = (
                    is_valid_move(self.square.index, move),
                    self.game.is_empty(square_if_moved),
                    self.game.position.is_path_clear(self.square.index, move)
                    )
        else:
            pawn_move_invariants = (
                    is_valid_move(self.square.index, move),
                    col_dist_if_moved == 1,
                    self.game.is_capturable(square_if_moved)
                    )
        return all(pawn_move_invariants)

    def get_potential_moves(self) -> Sequence[int]:
        return self.potential_advances() | self.potential_captures()

    def potential_advances(self) -> Sequence[int]:
        if self.piece.moves == []:
            return {UP, UP + UP} if self.piece.color == Color.white else {DOWN, DOWN + DOWN}

    def potential_captures(self) -> Sequence[int]:
        return {UP_LEFT, UP_RIGHT} if self.piece.color == Color.white else {DOWN_LEFT, DOWN_RIGHT}


class KingLegalMoveStrategy(LegalMoveStrategy):
    def is_legal(self, move: Move) -> bool:
        square_if_moved, current_col, col_if_moved, col_dist_if_moved, row_dist = get_move_facts(self.square.index, move)
        logging.debug("checking legality of moving king from %s to %s",
                to_algebraic(self.square.index),
                to_algebraic(square_if_moved))
        try:
            king_move_invariants = (
                    is_valid_move(self.square.index, move),
                    self.game.is_empty_or_capturable(square_if_moved)
                    )
        except IndexError:
            return False
        result = all(king_move_invariants)
        logging.debug("decided moving king at %s to %s is %s",
                to_algebraic(self.square.index),
                to_algebraic(square_if_moved),
                "legal" if result else "not legal")
        return result

    def get_potential_moves(self) -> Sequence[int]:
        return {UP, DOWN, LEFT, RIGHT,
                UP_LEFT, UP_RIGHT,
                DOWN_LEFT, DOWN_RIGHT}


PIECE_STRATEGY_MAPPING = {
        'Knight': KnightLegalMoveStrategy,
        'Pawn': PawnLegalMoveStrategy,
        'Bishop': BishopLegalMoveStrategy,
        'King': KingLegalMoveStrategy,
        'Rook': RookLegalMoveStrategy,
        'Queen': QueenLegalMoveStrategy
        }


def get_horizontal_moves(square_index: int) -> Sequence[int]:
    horizontal_index = square_index % 8
    left_threshold = horizontal_index
    right_threshold = 7 - horizontal_index

    possibles = []
    for i in range(1, left_threshold + 1):
        move = LEFT * i
        possibles.append(move)

    for i in range(1, right_threshold + 1):
        move = RIGHT * i
        possibles.append(move)

    return set(possibles)

def get_vertical_moves(square_index: int) -> Sequence[int]:
    vertical_index = square_index // 8
    up_threshold = vertical_index
    down_threshold = 7 - vertical_index

    possibles = []
    for i in range(1, up_threshold + 1):
        move = UP * i
        possibles.append(move)

    for i in range(1, down_threshold + 1):
        move = DOWN * i
        possibles.append(move)

    return set(possibles)


def get_diagonal_moves(square_index: int) -> Sequence[int]:
    horizontal_index = square_index % 8
    vertical_index = square_index // 8
    left_threshold = horizontal_index
    right_threshold = 7 - horizontal_index
    up_threshold = vertical_index
    down_threshold = 7 - vertical_index

    possibles = []
    for i in range(1, min(up_threshold, left_threshold) + 1):
        move = UP_LEFT * i
        possibles.append(move)

    for i in range(1, min(down_threshold, left_threshold) + 1):
        move = DOWN_LEFT * i
        possibles.append(move)

    for i in range(1, min(up_threshold, right_threshold) + 1):
        move = UP_RIGHT * i
        possibles.append(move)

    for i in range(1, min(down_threshold, right_threshold) + 1):
        move = DOWN_LEFT * i
        possibles.append(move)

    return set(possibles)

