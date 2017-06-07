import abc
import logging
from enum import Enum
from typing import Tuple, Optional, Sequence

class Color(Enum):
    white = 1
    black = 2

# piece values, roughly
QUEEN_VALUE = 9
PAWN_VALUE = 1
BISHOP_VALUE = 3.1
KNIGHT_VALUE = 3
ROOK_VALUE = 5
KING_VALUE = QUEEN_VALUE + PAWN_VALUE * 8 + BISHOP_VALUE * 2 + KNIGHT_VALUE * 2 + ROOK_VALUE * 2 + 1

EMPTY_SQUARE = ' '

class Piece(metaclass = abc.ABCMeta):
    def __init__(self, color: Color) -> None:
        self.color = color
        self.moves = []
        self.pins = []

    def __str__(self) -> str:
        return self.short_name if self.color == Color.white else self.short_name.lower()

    @staticmethod
    def from_notation(piece_notation: str) -> Optional['Piece']:
        if piece_notation == EMPTY_SQUARE:
            return None

        piece_class = PIECE_MAPPING[piece_notation.upper()]
        color = Color.white if piece_notation.isupper() else Color.black
        return piece_class(color)

class Rook(Piece):
    name = 'Rook'
    short_name = 'R'
    value = ROOK_VALUE

class Knight(Piece):
    name = 'Knight'
    short_name = 'N'
    value = KNIGHT_VALUE

class Bishop(Piece):
    name = 'Bishop'
    short_name = 'B'
    value = BISHOP_VALUE

class Queen(Piece):
    name = 'Queen'
    short_name = 'Q'
    value = QUEEN_VALUE

class King(Piece):
    name = 'King'
    short_name = 'K'
    value = KING_VALUE

class Pawn(Piece):
    name = 'Pawn'
    short_name = 'P'
    value = PAWN_VALUE

    def distance_from_promotion(self, square_index: int) -> int:
        if self.color == Color.black:
            return 6 - (square_index // 8 - 6)
        elif self.color == Color.white:
            return 6 - (square_index // 8 - 2)

PIECE_MAPPING = {
    'R': Rook,
    'N': Knight,
    'B': Bishop,
    'Q': Queen,
    'K': King,
    'P': Pawn
    }

