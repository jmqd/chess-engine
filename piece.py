import abc
import logging
from enum import Enum

class Color(Enum):
    WHITE = 1
    BLACK = 2

EMPTY_SQUARE = ' '
UP = -8
DOWN = 8
LEFT = -1
RIGHT = 1

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

    @abc.abstractmethod
    def get_legal_moves(self):
        raise SyntaxError("Implemented in subclass.")

    @staticmethod
    def from_piece(piece):
        pass


class LegalPawnMoveStrategy(LegalMoveStrategy):
    def get_legal_moves(self):
        moves = set()
        moves |= set(x + self.square for x in self.piece.potential_advances() if self.game.is_empty(x + self.square))
        logging.info("Potential advances: %s", moves)
        moves |= set(x + self.square for x in self.piece.potential_captures() if self.game.is_capturable(x + self.square))
        logging.info("With captures: %s", moves)
        return moves


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

class Knight(Piece):
    name = 'Knight'
    short_name = 'N'

class Bishop(Piece):
    name = 'Bishop'
    short_name = 'B'

class Queen(Piece):
    name = 'Queen'
    short_name = 'Q'

class King(Piece):
    name = 'King'
    short_name = 'K'
    move_matrix = (UP, DOWN, LEFT, RIGHT,
                   UP + LEFT, UP + RIGHT,
                   DOWN + LEFT, DOWN + RIGHT)

class Pawn(Piece):
    name = 'Pawn'
    short_name = 'P'
    legal_move_strategy = LegalPawnMoveStrategy

    def potential_advances(self):
        if self.moves == []:
            return {UP, UP + UP} if self.color == Color.WHITE else {DOWN, DOWN + DOWN}

    def potential_captures(self):
        return {UP + LEFT, UP + RIGHT} if self.color == Color.WHITE else {DOWN + LEFT, DOWN + RIGHT}

PIECE_MAPPING = {
    'r': Rook,
    'n': Knight,
    'b': Bishop,
    'q': Queen,
    'k': King,
    'p': Pawn
    }

