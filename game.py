import copy
import string
import itertools
import logging

from piece import Piece
from collections import OrderedDict


STANDARD_STARTING_POSITION = [
    'r', 'n', 'b', 'q', 'k', 'b', 'n', 'r',
    'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p',
    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
    'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P',
    'R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'
        ]
EMPTY_BOARD = [' '] * 64

A_THRU_H = 'ABCDEFGH'

class Game:
    def __init__(self):
        self.position = Position(STANDARD_STARTING_POSITION)
        self.black = None
        self.white = None
        self.move_history = []
        self.active_player = self.white
        self.captured_pieces = set()

    @property
    def legal_moves(self):
        legal_moves = []
        for square, piece in self.position.pieces:
            potential_moves = piece.enumerate_potential_moves(square)

    @legal_moves.setter
    def legal_moves(self, val):
        raise NotImplementedError("No.")


    def legal_moves_for_piece(self, piece):
        pass

    def show(self):
        print(self.position)


class Position:
    def __init__(self, position_data):
        self.position = self.serialize(position_data)

    @property
    def pieces(self):
        for letter, col in self.position:
            for num, piece in enumerate(col):
                square = letter + num
                yield square, piece

    @staticmethod
    def serialize(data):
        internal_position = copy.deepcopy(EMPTY_BOARD)
        for index, notated_char in enumerate(data):
            internal_position[index] = Piece.from_notation(notated_char)
        return internal_position

    def __str__(self):
        list_repr = []
        for first_sq_in_row in range(0, 64, 8):
            list_repr.append(str([str(x) for x in self.position[first_sq_in_row:first_sq_in_row + 8]]))
        return '\n'.join(list_repr)


def humanize_square_name(index):
    string_index = str(index)
    distance_from_top = index // 8
    row = 8 - distance_from_top
    col = A_THRU_H[index - distance_from_top]
    return col + row


def main():
    logging.basicConfig(level = logging.INFO)
    game = Game()
    game.show()

if __name__ == '__main__':
    main()
