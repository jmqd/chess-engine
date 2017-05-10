import copy
import string
import random
import logging
import operator
import itertools

from piece import Piece
from piece import King
from piece import Queen
from piece import Rook
from piece import Bishop
from piece import Knight
from piece import Pawn

from piece import Color
from piece import EmptySquare

from util import humanize_square_name
from util import dehumanize_square_name
from util import get_move_facts
from util import A_THRU_H


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
PIECE_TYPES = [King, Queen, Pawn, Rook, Knight, Bishop]
COLORS = [Color.black, Color.white]

class Game:
    def __init__(self, position=None):
        self.position = position or Position(STANDARD_STARTING_POSITION)
        self.move_history = []
        self.active_player = Color.white
        self.captured_pieces = []
        self.is_playing = True

    def next_player(self):
        self.active_player = Color.white if self.active_player == Color.black else Color.black

    @property
    def inactive_player(self):
        return Color.white if self.active_player == Color.black else Color.white

    def legal_moves_for_square(self, square):
        square = square if type(square) == int else dehumanize_square_name(square)
        return self.position[square].legal_move_strategy(self, square).get_legal_moves()

    def find_all_legal_moves(self):
        legal_moves = set()
        for i, piece in enumerate(self.position):
            if piece.__class__ == EmptySquare or piece.color != self.active_player: continue
            legal_moves |= set(humanize_square_name(i) + '->' + humanize_square_name(x) for x in self.legal_moves_for_square(i))
        return legal_moves


    def show(self):
        screen = []
        for index, line in enumerate(str(self.position).split('\n')):
            print(8 - index, line)
        print(" " * 4 + '    '.join(x for x in A_THRU_H))


    def move(self, origin, destination):
        piece = self.position[origin]
        new_square = destination if type(destination) == int else dehumanize_square_name(destination)

        if not isinstance(piece, Piece):
            raise ValueError("That square is empty!")

        if piece.color != self.active_player:
            raise ValueError("That piece belongs to {}!".format(self.active_player.name))

        legal_moves = self.legal_moves_for_square(origin)

        if new_square not in legal_moves:
            raise ValueError("You can't move that there!")

        if self.is_occupied(new_square):
            self.captured_pieces.append(self.position[new_square])

        self.position[origin], self.position[new_square] = EmptySquare(), piece
        print("Moved the {} at {} to {}.".format(piece.name, origin, destination))
        self.move_history.append((origin, destination))
        self.next_player()

    @staticmethod
    def play():
        game = Game()
        while game.is_playing:
            tmp_function_print_squares_for_pieces(game)
            game.show()
            move = input("{} to move: ".format(game.active_player.name))
            if move == 'listAll':
                print(game.find_all_legal_moves())
            else:
                origin, destination = move.split('->')
                try:
                    game.move(origin, destination)
                except Exception as e:
                    print("Sorry, ", e)

    def is_empty_or_capturable(self, square):
        return self.is_empty(square) or self.is_capturable(square)

    def is_occupied(self, square):
        return not self.is_empty(square)

    def is_attacked_by_active_player(square):
        return square in self.attacked_squares

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
        if row_dist > 0 and col_dist_if_moved > 0:
            step_magnitude = 9 if move % 9 == 0 else 7

        step = operator.__add__ if move < 0 else operator.__sub__
        move = step(move, step_magnitude)
        while move != 0:
            if not self.is_empty(move + origin): return False
            move = step(move, step_magnitude)
        return True

def tmp_function_print_squares_for_pieces(game):
    piece_to_check = random.choice(PIECE_TYPES)
    color_to_check = random.choice(COLORS)
    squares = game.position.find_piece_squares(piece_to_check, color_to_check)
    print("Randomly decided to show all positions of {} {}s".format(color_to_check.name,
                                                                    piece_to_check.name),
          end = ': ')
    print([humanize_square_name(x) for x in squares])

class Position:
    def __init__(self, position_data):
        self.position = self.serialize(position_data)
        self.__it_checkpoint = -1

    @property
    def pieces(self):
        for letter, col in self.position:
            for num, piece in enumerate(col):
                square = letter + num
                yield square, piece

    def find_piece_squares(self, piece_class, color):
        squares = []
        for sq_index, piece in enumerate(self):
            if piece.color == color and isinstance(piece, piece_class):
                squares.append(sq_index)
        return squares

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

    def __iter__(self):
        return self

    def __next__(self):
        self.__it_checkpoint += 1

        if self.__it_checkpoint > 63:
            self.__it_checkpoint = -1
            raise StopIteration

        return self.position[self.__it_checkpoint]


    def __getitem__(self, square):
        index = square if type(square) == int else dehumanize_square_name(square)
        return self.position[index]

    def __setitem__(self, square, value):
        index = square if type(square) == int else dehumanize_square_name(square)
        self.position[index] = value

