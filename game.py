import copy
import string
import itertools
import logging

from piece import Piece
from collections import OrderedDict


STANDARD_STARTING_POSITION = OrderedDict([
    ('A', ['R', 'P', None, None, None, None, 'p', 'r']),
    ('B', ['N', 'P', None, None, None, None, 'p', 'n']),
    ('C', ['B', 'P', None, None, None, None, 'p', 'b']),
    ('D', ['Q', 'P', None, None, None, None, 'p', 'q']),
    ('E', ['K', 'P', None, None, None, None, 'p', 'k']),
    ('F', ['B', 'P', None, None, None, None, 'p', 'b']),
    ('G', ['N', 'P', None, None, None, None, 'p', 'n']),
    ('H', ['R', 'P', None, None, None, None, 'p', 'r'])
    ])

EMPTY_BOARD = OrderedDict([(char, [None] * 8) for char in string.ascii_uppercase[:8]])
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
        for piece in self.board.pieces:
            legal_moves.extend(self.legal_moves_for_piece(piece))

        return legal_moves


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

    @staticmethod
    def serialize(data):
        internal_position = copy.deepcopy(EMPTY_BOARD)
        logging.info(internal_position)
        for letter, col in data.items():
            for num, piece_notation in enumerate(col):
                logging.info("putting piece %s to [%s][%s]", piece_notation, letter, num)
                internal_position[letter][num] = Piece.from_notation(piece_notation)
        return internal_position

    def __str__(self):
        list_repr = []
        for i in range(7, -1, -1):
            list_repr.extend([[str(self.position[letter][i]) for letter in A_THRU_H]])
        return str('\n'.join(str(x) for x in list_repr))


def main():
    logging.basicConfig(level = logging.INFO)
    game = Game()
    game.show()

if __name__ == '__main__':
    main()
