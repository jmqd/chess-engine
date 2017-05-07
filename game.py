import copy
import string
import itertools
import logging

from piece import Piece
from piece import Color
from piece import EmptySquare


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
        self.move_history = []
        self.active_player = Color.WHITE
        self.captured_pieces = set()

    @property
    def legal_moves(self):
        legal_moves = []
        for square, piece in self.position.pieces:
            potential_moves = piece.enumerate_potential_moves(square)

    @legal_moves.setter
    def legal_moves(self, val):
        raise NotImplementedError("No.")


    def legal_moves_for_square(self, square):
        return self.position[square].legal_move_strategy(self, square).get_legal_moves()

    def show(self):
        print(self.position)

    def move(self, origin, destination):
        if self.position[origin].color != self.active_player:
            raise ValueError("That piece belongs to the inactive player!")

    def is_empty(self, square):
        logging.info("Checking if %s is empty...", square)
        result = self.position[square].__class__ == EmptySquare
        logging.info("%s is %s", square, 'empty' if result else 'not empty')
        return result

    def is_capturable(self, square):
        logging.info("Checking if %s is capturable...", square)
        result = not self.is_empty(square) and self.position[square].color != self.active_player
        logging.info("%s is %s", square, 'capturable' if result else 'not capturable')
        return result

    @staticmethod
    def is_on_board(square):
        return 0 <= square <= 63


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

    def __getitem__(self, index):
        return self.position[index]



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
    print(game.legal_moves_for_square(48))

if __name__ == '__main__':
    main()
