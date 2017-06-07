import sys
import random
import logging

from position import Position

from piece import Piece
from piece import Color
from piece import King
from piece import Queen
from piece import Rook
from piece import Bishop
from piece import Knight
from piece import Pawn

from engine import ChessEngine

from util import to_algebraic
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

PIECE_TYPES = [King, Queen, Pawn, Rook, Knight, Bishop]
COLORS = [Color.black, Color.white]

class Game:
    def __init__(self, position=None):
        self.position = position or Position(STANDARD_STARTING_POSITION)
        self.move_history = []
        self.active_player = Color.white
        self.captured_pieces = []
        self.is_playing = True

        # TODO: break this out into a Computer class
        self.computer = None
        self.is_computer_playing = None
        self.computer_color = None

    def next_player(self):
        return Color.white if self.active_player == Color.black else Color.black

    @property
    def inactive_player(self):
        return Color.white if self.active_player == Color.black else Color.white

    def legal_moves_for_square(self, square):
        return square.piece.legal_move_strategy(self, square).get_legal_moves()

    def find_all_legal_moves(self):
        legal_moves = []
        for i, square in enumerate(self.position):
            if square.is_empty() or square.piece.color != self.active_player: continue
            for legal_move in self.legal_moves_for_square(square):
                legal_moves.append((i, legal_move))
        return legal_moves


    def show(self):
        screen = []
        for index, line in enumerate(str(self.position).split('\n')):
            print(8 - index, line)
        print(" " * 4 + '    '.join(x for x in A_THRU_H))


    def move(self, origin, destination):
        square = self.position[origin]
        new_square = self.position[destination]

        if square.is_empty():
            raise ValueError("That square is empty!")

        if square.piece.color != self.active_player:
            raise IllegalMoveException("That piece belongs to {}!".format(self.active_player.name))

        legal_moves = self.legal_moves_for_square(square)

        logging.info("Legal moves for %s: %s", square, legal_moves)

        if new_square.numeric_index not in legal_moves:
            raise IllegalMoveException("You can't move that there!")

        captured_piece = None

        if new_square.is_occupied():
            captured_piece = self.position[new_square].piece
            self.captured_pieces.append(captured_piece)

        square.piece, new_square.piece = None, square.piece

        logging.info("Moved the {} at {} to {}.".format(new_square.piece.name, origin, destination))

        self.move_history.append((origin, destination, captured_piece))
        self.active_player = self.next_player()

    def start_engine(self):
        self.computer = ChessEngine(self)

    def rewind(self):
        origin, destination, captured_piece = self.move_history.pop()

        original_square = self.position[origin].sqaure
        current_square = self.position[destination].square

        original_square.piece, current_square.piece = current_square.piece, captured_piece or None

        logging.info("Rewinded move {} to {}.".format(to_algebraic(origin), to_algebraic(destination)))

        self.active_player = self.next_player()

    def prompt_for_mode(self):
        self.is_computer_playing = True if input("Play against the computer? y/n > ") == "y" else False
        self.computer_color = Color.white if input("Choose black or white b/w > ") == 'b' else Color.black
        self.start_engine()

    @staticmethod
    def play():
        game = Game()
        game.prompt_for_mode()

        while game.is_playing:
            tmp_function_print_squares_for_pieces(game)
            if game.is_computer_playing and game.computer_color == game.active_player:
                origin, destination = game.computer.choose_random_move()
                game.move(origin, destination)

            game.show()
            move = input("{} to move: ".format(game.active_player.name))

            if move == 'listAll':
                print(game.find_all_legal_moves())
            elif move == 'rewind':
                game.rewind()
            elif move in ('quit', 'q'):
                print("Quitting...")
                sys.exit(0)
            else:
                origin, destination = move.split()
                try:
                    game.move(origin, destination)
                except ChessException as chess_exception:
                    print("Sorry: ", chess_exception)
                except Exception as e:
                    raise

    def is_empty_or_capturable(self, square):
        return self.is_empty(square) or self.is_capturable(square)

    def is_occupied(self, square):
        return not self.is_empty(square)

    def is_empty(self, square_index):
        logging.debug("Checking if %s is empty...", square_index)
        result = self.position[square_index].is_empty()
        logging.debug("%s is %s", square_index, 'empty' if result else 'not empty')
        return result

    def is_capturable(self, square_index):
        logging.debug("Checking if %s is capturable...", square_index)
        result = not self.is_empty(square_index) and self.position[square_index].piece.color != self.active_player
        logging.debug("%s is %s", to_algebraic(square_index), 'capturable' if result else 'not capturable')
        return result


def tmp_function_print_squares_for_pieces(game):
    piece_to_check = random.choice(PIECE_TYPES)
    color_to_check = random.choice(COLORS)
    squares = game.position.find_piece_squares(piece_to_check, color_to_check)
    print("Randomly decided to show all positions of {} {}s".format(color_to_check.name,
                                                                    piece_to_check.name),
          end = ': ')
    print([to_algebraic(x) for x in squares])

class ChessException(Exception): pass
class IllegalMoveException(ChessException, ValueError): pass
