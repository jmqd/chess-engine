import copy
import operator

from piece import Piece
from util import to_algebraic
from util import to_numeric
from util import get_move_facts

EMPTY_BOARD = [' '] * 64
VERTICAL_STEP = 8
HORIZONTAL_STEP = 1

class Square:
    def __init__(self, numeric_index, piece=None):
        self.numeric_index = numeric_index
        self.algebraic_index = to_algebraic(numeric_index)
        self._piece = piece

    @property
    def piece(self):
        return self._piece

    @piece.setter
    def piece(self, val):
        self._piece = val

    def is_empty(self):
        return self.piece is None

    def is_occupied(self):
        return self.piece is not None

    def occupied_by(self):
        if self.piece is None:
            return None
        else:
            return self.piece.color

    def __str__(self):
        if self.piece is None:
            return ' '
        else:
            return str(self.piece)


class Position:
    def __init__(self, position_data):
        self.grid = self.serialize(position_data)

        # state for iterator. probs should refactor this
        self.__it_checkpoint = -1

    def find_piece_squares(self, piece_class, color):
        square_indices = []
        for sq_index, square in enumerate(self):
            if square.occupied_by() == color and isinstance(square.piece, piece_class):
                square_indices.append(sq_index)
        return square_indices

    def is_path_clear(self, origin, displacement):
        square_if_moved, current_col, col_if_moved, col_dist_if_moved, row_dist = get_move_facts(origin, displacement)
        if row_dist == 0 and col_dist_if_moved > 0:
            step_magnitude = HORIZONTAL_STEP
        if row_dist > 0 and col_dist_if_moved == 0:
            step_magnitude = VERTICAL_STEP
        if row_dist > 0 and col_dist_if_moved > 0:
            step_magnitude = 9 if displacement % 9 == 0 else 7

        step = operator.__add__ if displacement < 0 else operator.__sub__
        displacement = step(displacement, step_magnitude)
        if not self[origin + displacement].is_empty(): return False
        while displacement != 0:
            if not self[origin + displacement].is_empty():
                return False
            displacement = step(displacement, step_magnitude)
        return True

    @staticmethod
    def transposition_of(position, move):
        origin, destination = move
        new_position = copy.deepcopy(position)
        new_position[origin].piece, new_position[destination].piece = None, new_position[origin].piece
        return new_position


    @staticmethod
    def serialize(data):
        internal_position = copy.deepcopy(EMPTY_BOARD)
        for index, notated_char in enumerate(data):
            internal_position[index] = Square(index, Piece.from_notation(notated_char))
        return internal_position

    def __str__(self):
        list_repr = []
        for first_sq_in_row in range(0, 64, 8):
            list_repr.append(str([str(x) for x in self.grid[first_sq_in_row:first_sq_in_row + 8]]))
        return '\n'.join(list_repr)

    def __iter__(self):
        return self

    def __next__(self):
        self.__it_checkpoint += 1
        if self.__it_checkpoint > 63:
            self.__it_checkpoint = -1
            raise StopIteration
        return self.grid[self.__it_checkpoint]


    def __getitem__(self, square):
        if type(square) == int:
            index = square
        elif type(square) == str:
            index = to_numeric(square)
        elif type(square) == Square:
            index = square.numeric_index
        return self.grid[index]

    def __setitem__(self, square, value):
        index = square if type(square) == int else to_numeric(square)
        self.grid[index] = value

