import abc
import logging
from enum import Enum

from util import get_move_facts
from util import get_row_distance
from util import is_valid_move
from util import is_on_board

class Color(Enum):
    white = 1
    black = 2

# piece values, roughly
QUEEN_VALUE = 9
PAWN_VALUE = 1
BISHOP_VALUE = 3.1
KNIGHT_VALUE = 3
ROOK_VALUE = 5

# movement consts
EMPTY_SQUARE = ' '
DOWN = 8
RIGHT = 1
UP = DOWN * -1
LEFT = RIGHT * -1
DOWN_RIGHT = DOWN + RIGHT
DOWN_LEFT = DOWN + LEFT
UP_LEFT = UP + LEFT
UP_RIGHT = UP + RIGHT

class LegalMoveStrategy(metaclass = abc.ABCMeta):
    def __init__(self, game, square):
        self.game = game
        self.square = square
        self.piece = self.square.piece

    def is_legal(self, move):
        '''A common implementation of is_legal. Can be overridden for exception pieces.'''
        square_if_moved, current_col, col_if_moved, col_dist_if_moved, row_dist = get_move_facts(self.square.numeric_index, move)
        default_legal_move_invariants = (
                is_valid_move(self.square.numeric_index, move),
                self.game.is_empty_or_capturable(square_if_moved),
                self.game.position.is_path_clear(self.square.numeric_index, move)
                )

        return all(default_legal_move_invariants)

    def get_legal_moves(self):
        return set(self.square.numeric_index + move for move in self.piece.potentials() if self.is_legal(move))


class KnightLegalMoveStrategy(LegalMoveStrategy):
    def is_legal(self, move):
        square_if_moved, current_col, col_if_moved, col_dist_if_moved, row_dist = get_move_facts(self.square.numeric_index, move)
        expected_col_difference = 1 if row_dist == 2 else 2

        try:
            legal_knight_move_invariants = (
                    row_dist in (1, 2),
                    abs(col_if_moved - current_col) == expected_col_difference,
                    is_valid_move(self.square.numeric_index, move),
                    self.game.is_empty_or_capturable(square_if_moved)
                    )
        except IndexError as e:
            return False

        return all(legal_knight_move_invariants)

#TODO: lots of repetition here. Use mixins. Clean it up.

class BishopLegalMoveStrategy(LegalMoveStrategy):
    def get_legal_moves(self):
        return set(self.square.numeric_index + move for move in self.piece.potentials(self.square.numeric_index) if self.is_legal(move))


class RookLegalMoveStrategy(LegalMoveStrategy):
    def get_legal_moves(self):
        return set(self.square.numeric_index + move for move in self.piece.potentials(self.square.numeric_index) if self.is_legal(move))


class QueenLegalMoveStrategy(LegalMoveStrategy):
    def get_legal_moves(self):
        return set(self.square.numeric_index + move for move in self.piece.potentials(self.square.numeric_index) if self.is_legal(move))


class PawnLegalMoveStrategy(LegalMoveStrategy):
    def is_legal(self, move):
        square_if_moved, current_col, col_if_moved, col_dist_if_moved, row_dist = get_move_facts(self.square.numeric_index, move)
        if col_dist_if_moved == 0:
            pawn_move_invariants = (
                    is_valid_move(self.square.numeric_index, move),
                    self.game.is_empty(square_if_moved),
                    self.game.position.is_path_clear(self.square.numeric_index, move)
                    )
        else:
            pawn_move_invariants = (
                    is_valid_move(self.square.numeric_index, move),
                    col_dist_if_moved == 1,
                    self.game.is_capturable(square_if_moved)
                    )
        return all(pawn_move_invariants)


class KingLegalMoveStrategy(LegalMoveStrategy):
    def is_legal(self, move):
        square_if_moved, current_col, col_if_moved, col_dist_if_moved, row_dist = get_move_facts(self.square.numeric_index, move)
        try:
            king_move_invariants = (
                    is_valid_move(self.square.numeric_index, move),
                    self.game.is_empty_or_capturable(square_if_moved)
                    )
        except IndexError:
            return False
        return all(king_move_invariants)


class Piece(metaclass = abc.ABCMeta):
    def __init__(self, color):
        self.color = color
        self.moves = []
        self.pins = []

    def __str__(self):
        return self.short_name if self.color == Color.white else self.short_name.lower()

    @staticmethod
    def from_notation(piece_notation):
        if piece_notation == EMPTY_SQUARE:
            return None

        piece_class = PIECE_MAPPING[piece_notation.lower()]
        color = Color.white if piece_notation.isupper() else Color.black
        return piece_class(color)


class Rook(Piece):
    name = 'Rook'
    short_name = 'R'
    value = ROOK_VALUE
    legal_move_strategy = RookLegalMoveStrategy

    def potentials(self, square_index):
        return get_horizontal_moves(square_index) | get_vertical_moves(square_index)


class Knight(Piece):
    name = 'Knight'
    short_name = 'N'
    value = KNIGHT_VALUE
    legal_move_strategy = KnightLegalMoveStrategy

    def potentials(self):
        return {UP_LEFT + LEFT, UP + UP_LEFT, UP_RIGHT + RIGHT,
                UP + UP_RIGHT, RIGHT + DOWN_RIGHT, DOWN_RIGHT + DOWN,
                DOWN + DOWN_LEFT, LEFT + DOWN_LEFT}

class Bishop(Piece):
    name = 'Bishop'
    short_name = 'B'
    value = BISHOP_VALUE
    legal_move_strategy = BishopLegalMoveStrategy

    def potentials(self, square_index):
        return get_diagonal_moves(square_index)


class Queen(Piece):
    name = 'Queen'
    short_name = 'Q'
    value = QUEEN_VALUE
    legal_move_strategy = QueenLegalMoveStrategy

    def potentials(self, square_index):
        return get_diagonal_moves(square_index) | get_horizontal_moves(square_index) | get_vertical_moves(square_index)

def get_horizontal_moves(square_index):
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

def get_vertical_moves(square_index):
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


def get_diagonal_moves(square_index):
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


class King(Piece):
    name = 'King'
    short_name = 'K'
    legal_move_strategy = KingLegalMoveStrategy

    def potentials(self):
        return {UP, DOWN, LEFT, RIGHT,
                UP_LEFT, UP_RIGHT,
                DOWN_LEFT, DOWN_RIGHT}


class Pawn(Piece):
    name = 'Pawn'
    short_name = 'P'
    value = PAWN_VALUE
    legal_move_strategy = PawnLegalMoveStrategy

    def potentials(self):
        return self.potential_advances() | self.potential_captures()

    def potential_advances(self):
        if self.moves == []:
            return {UP, UP + UP} if self.color == Color.white else {DOWN, DOWN + DOWN}

    def potential_captures(self):
        return {UP_LEFT, UP_RIGHT} if self.color == Color.white else {DOWN_LEFT, DOWN_RIGHT}

PIECE_MAPPING = {
    'r': Rook,
    'n': Knight,
    'b': Bishop,
    'q': Queen,
    'k': King,
    'p': Pawn
    }

