import abc
import logging
from enum import Enum

from util import humanize_square_name
from util import get_move_facts
from util import get_row_distance
from util import is_valid_move
from util import is_on_board

class Color(Enum):
    WHITE = 1
    BLACK = 2

EMPTY_SQUARE = ' '
DOWN = 8
RIGHT = 1
UP = DOWN * -1
LEFT = RIGHT * -1
DOWN_RIGHT = DOWN + RIGHT
DOWN_LEFT = DOWN + LEFT
UP_LEFT = UP + LEFT
UP_RIGHT = UP + RIGHT

class EmptySquare:
    def __init__(self):
        pass

    def __str__(self):
        return ' '

class LegalMoveStrategy(metaclass = abc.ABCMeta):
    def __init__(self, game, square):
        self.game = game
        self.square = square
        self.piece = self.game.position[square]

    def get_legal_moves(self):
        return set(self.square + move for move in self.piece.potentials() if self.is_legal(move))

    @abc.abstractmethod
    def is_legal(self, move):
        raise SyntaxError("Must implement in subclass.")

    @staticmethod
    def from_piece(piece):
        pass

class LegalKnightMoveStrategy(LegalMoveStrategy):
    def is_legal(self, move):
        square_if_moved, current_col, col_if_moved, col_dist_if_moved, row_dist = get_move_facts(self.square, move)
        expected_col_difference = 1 if row_dist == 2 else 2

        try:
            legal_knight_move_invariants = (
                    row_dist in (1, 2),
                    abs(col_if_moved - current_col) == expected_col_difference,
                    is_valid_move(self.square, move),
                    self.game.is_empty_or_capturable(square_if_moved)
                    )
        except IndexError as e:
            return False

        return all(legal_knight_move_invariants)

class LegalBishopMoveStrategy(LegalMoveStrategy):
    def get_legal_moves(self):
        return set(self.square + move for move in self.piece.potentials(self.square) if self.is_legal(move))

    def is_legal(self, move):
        square_if_moved, current_col, col_if_moved, col_dist_if_moved, row_dist = get_move_facts(self.square, move)
        legal_bishop_move_invariants = (
                is_valid_move(self.square, move),
                self.game.is_empty_or_capturable(square_if_moved),
                self.game.is_path_clear(self.square, move)
                )

        return all(legal_bishop_move_invariants)

class LegalPawnMoveStrategy(LegalMoveStrategy):
    def is_legal(self, move):
        square_if_moved, current_col, col_if_moved, col_dist_if_moved, row_dist = get_move_facts(self.square, move)
        if col_dist_if_moved == 0:
            pawn_move_invariants = (
                    is_valid_move(self.square, move),
                    self.game.is_empty(square_if_moved),
                    self.game.is_path_clear(self.square, move)
                    )
        else:
            pawn_move_invariants = (
                    is_valid_move(self.square, move),
                    col_dist_if_moved == 1,
                    self.game.is_capturable(square_if_moved)
                    )
        return all(pawn_move_invariants)


class Piece(metaclass = abc.ABCMeta):
    def __init__(self, color):
        self.color = color
        self.moves = []
        self.pins = []

    def __str__(self):
        return self.short_name if self.color == Color.WHITE else self.short_name.lower()

    @staticmethod
    def from_notation(piece_notation):
        if piece_notation == EMPTY_SQUARE:
            return EmptySquare()

        piece_class = PIECE_MAPPING[piece_notation.lower()]
        color = Color.WHITE if piece_notation.isupper() else Color.BLACK
        return piece_class(color)

class Rook(Piece):
    name = 'Rook'
    short_name = 'R'

    @staticmethod
    def enumerate_potential_moves(square):
        pass

    def potentials(self):
        return set()

class Knight(Piece):
    name = 'Knight'
    short_name = 'N'
    legal_move_strategy = LegalKnightMoveStrategy

    def potentials(self):
        return {UP_LEFT + LEFT, UP + UP_LEFT, UP_RIGHT + RIGHT,
                UP + UP_RIGHT, RIGHT + DOWN_RIGHT, DOWN_RIGHT + DOWN,
                DOWN + DOWN_LEFT, LEFT + DOWN_LEFT}

class Bishop(Piece):
    name = 'Bishop'
    short_name = 'B'
    legal_move_strategy = LegalBishopMoveStrategy

    def potentials(self, square):
        horizontal_index = square % 8
        vertical_index = square // 8
        left_threshold = horizontal_index
        right_threshold = 7 - horizontal_index
        up_threshold = vertical_index
        down_threshold = 7 - vertical_index

        # in the running for ugliest block of code I've ever written.
        # TODO: write Bishop movement elegantly
        possibles = []
        for i in range(1, min(up_threshold, left_threshold) + 1, 1):
            move = UP_LEFT * i
            possibles.append(move)

        for i in range(1, min(down_threshold, left_threshold) + 1, 1):
            move = DOWN_LEFT * i
            possibles.append(move)

        for i in range(1, min(up_threshold, right_threshold) + 1, 1):
            move = UP_RIGHT * i
            possibles.append(move)

        for i in range(1, min(down_threshold, right_threshold) + 1, 1):
            move = DOWN_LEFT * i
            possibles.append(move)

        return set(possibles)

class Queen(Piece):
    name = 'Queen'
    short_name = 'Q'

    def potentials(self):
        return set()

class King(Piece):
    name = 'King'
    short_name = 'K'

    def potentials(self):
        return {UP, DOWN, LEFT, RIGHT,
                UP_LEFT, UP_RIGHT,
                DOWN_LEFT, DOWN_RIGHT}


class Pawn(Piece):
    name = 'Pawn'
    short_name = 'P'
    legal_move_strategy = LegalPawnMoveStrategy

    def potentials(self):
        return self.potential_advances() | self.potential_captures()

    def potential_advances(self):
        if self.moves == []:
            return {UP, UP + UP} if self.color == Color.WHITE else {DOWN, DOWN + DOWN}

    def potential_captures(self):
        return {UP_LEFT, UP_RIGHT} if self.color == Color.WHITE else {DOWN_LEFT, DOWN_RIGHT}

PIECE_MAPPING = {
    'r': Rook,
    'n': Knight,
    'b': Bishop,
    'q': Queen,
    'k': King,
    'p': Pawn
    }

