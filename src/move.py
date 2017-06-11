import abc
import logging
from typing import Sequence
from enum import Enum


from src.piece import Color

from src.util import get_move_facts
from src.util import is_valid_move
from src.util import to_algebraic

DOWN = 8
RIGHT = 1
UP = DOWN * -1
LEFT = RIGHT * -1
DOWN_RIGHT = DOWN + RIGHT
DOWN_LEFT = DOWN + LEFT
UP_LEFT = UP + LEFT
UP_RIGHT = UP + RIGHT

class Direction(Enum):
    UP = -8
    DOWN = 8
    LEFT = -1
    RIGHT = 1
    DOWN_RIGHT = 9
    DOWN_LEFT = 7
    UP_LEFT = -7
    UP_RIGHT = -9

class Move:
    def __init__(self, origin: int, delta: int) -> None:
        self.origin = origin
        self.delta = delta

        (self.destination,
        self.origin_col,
        self.destination_col,
        self.dx,
        self.dy) = get_move_facts(origin, delta)
        self.direction = self.decide_direction()

    def __str__(self):
        return '{}->{}'.format(self.origin, self.destination)

    def __hash__(self):
        return hash(str(self))

    def decide_direction(self):
        if self.dy == 0 and self.dx != 0:
            return Direction.LEFT if self.delta < 0 else Direction.RIGHT

        # moving vertically? (iff)
        if self.dy != 0 and self.dx == 0:
            return Direction.UP if self.delta < 0 else Direction.DOWN

        # moving diaganolly? (iff)
        if self.dy != 0 and self.dx != 0:
            if self.delta < 0:
                return Direction.UP_LEFT if self.delta % 9 == 0 else Direction.UP_RIGHT
            if self.delta > 0:
                return Direction.DOWN_LEFT if self.delta % 9 == 0 else Direction.DOWN_RIGHT

        if 'Code bug':
            raise Exception("Code logic error here... should have returned a direction.")

    def __str__(self):
        return '{} {}'.format(to_algebraic(self.origin), to_algebraic(self.destination))

class LegalMoveStrategy(metaclass = abc.ABCMeta):
    def __init__(self, position: 'Position', square: 'Square') -> None:
        self.position = position
        self.square = square
        self.piece = self.square.piece

    @staticmethod
    def of(piece: 'Piece') -> 'LegalMoveStrategy':
        return PIECE_STRATEGY_MAPPING[piece.name]

    def validate_can_move(self):
        if self.square.is_empty() or self.position.active_player != self.piece.color:
            return False
        return True

    def is_in_check(self) -> bool:
        move = self.move
        proposed_position = self.position.get_transposition(move)
        if proposed_position.is_in_check(self.position.active_player):
            return True
        return False

    def is_legal(self, move: Move) -> bool:
        '''A base implementation of is_legal. Can be overridden for exception pieces.'''
        default_legal_move_invariants = (
                is_valid_move(self.square.index, move.delta),
                self.position.is_empty_or_capturable(move.destination),
                self.position.is_path_clear(move)
                )

        return all(default_legal_move_invariants)

    def get_legal_moves(self) -> Sequence[int]:
        if not self.validate_can_move():
            return set()

        pos = self.square.index
        legal_moves = set()
        for delta in self.get_potential_moves():
            move = Move(pos, delta)
            if self.is_legal(move):
                legal_moves.add(move)
        return legal_moves

class RayPieceStrategyMixin:
    def get_legal_moves(self) -> Sequence[int]:
        if not self.validate_can_move():
            return set()

        pos = self.square.index
        legal_moves = set()
        for delta in self.get_potential_moves(pos):
            move = Move(pos, delta)
            if self.is_legal(move):
                legal_moves.add(move)
        return legal_moves

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
        dx_invariant = 1 if move.dy == 2 else 2

        try:
            legal_knight_move_invariants = (
                    move.dy in (1, 2),
                    move.dx == dx_invariant,
                    is_valid_move(move.origin, move.delta),
                    self.position.is_empty_or_capturable(move.destination)
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
        if move.dx == 0:
            pawn_move_invariants = (
                    is_valid_move(move.origin, move.delta),
                    self.position.is_empty(move.destination),
                    self.position.is_path_clear(move)
                    )
        else:
            pawn_move_invariants = (
                    is_valid_move(move.origin, move.delta),
                    move.dx == 1,
                    self.position.is_capturable(move.destination)
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
        logging.debug("checking legality of moving king from %s to %s",
                to_algebraic(move.origin),
                to_algebraic(move.destination))
        try:
            king_move_invariants = (
                    is_valid_move(move.origin, move.delta),
                    self.position.is_empty_or_capturable(move.destination)
                    )
        except IndexError:
            return False

        result = all(king_move_invariants)
        logging.debug("decided moving king at %s to %s is %s",
                to_algebraic(move.origin),
                to_algebraic(move.destination),
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

