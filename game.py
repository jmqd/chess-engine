import copy
import string
import logging
import operator
import itertools

from piece import Piece
from piece import Color
from piece import EmptySquare

from util import humanize_square_name
from util import dehumanize_square_name
from util import get_move_facts


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
VERTICAL_STEP = 8
HORIZONTAL_STEP = 1

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
        square = square if type(square) == int else dehumanize_square_name(square)
        return self.position[square].legal_move_strategy(self, square).get_legal_moves()

    def show(self):
        print(self.position)

    def move(self, origin, destination):
        if self.position[origin].color != self.active_player:
            raise ValueError("That piece belongs to the inactive player!")

    def is_empty_or_capturable(self, square):
        return self.is_empty(square) or self.is_capturable(square)

    def is_empty(self, square):
        logging.debug("Checking if %s is empty...", square)
        result = self.position[square].__class__ == EmptySquare
        logging.debug("%s is %s", square, 'empty' if result else 'not empty')
        return result

    def is_capturable(self, square):
        logging.debug("Checking if %s is capturable...", square)
        result = not self.is_empty(square) and self.position[square].color != self.active_player
        logging.debug("%s is %s", square, 'capturable' if result else 'not capturable')
        return result

    def is_path_clear(self, origin, move):
        square_if_moved, current_col, col_if_moved, col_dist_if_moved, row_dist = get_move_facts(origin, move)
        if row_dist == 0 and col_dist_if_moved > 0:
            step_magnitude = HORIZONTAL_STEP
        if row_dist > 0 and col_dist_if_moved == 0:
            step_magnitude = VERTICAL_STEP
        if row_dist > 0 and col_dist_if_moved > 0 and move % 9 == 0:
            step_magnitude = DIAGANOL_STEP

        step = operator.__add__ if move < 0 else operator.__sub__
        move = step(move, step_magnitude)
        while move != 0:
            if not self.is_empty(move + origin): return False
            move = step(move, step_magnitude)

        return True


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

def main():
    logging.basicConfig(level = logging.DEBUG)
    game = Game()
    game.show()
    print(set(humanize_square_name(x) for x in game.legal_moves_for_square('A2')))

if __name__ == '__main__':
    main()
