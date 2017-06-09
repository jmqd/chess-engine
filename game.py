import sys
import random
import logging
from typing import Tuple, Sequence, Any, Optional

from position import Position
from position import Square

from piece import Piece
from piece import Color
from piece import King
from piece import Queen
from piece import Rook
from piece import Bishop
from piece import Knight
from piece import Pawn

from move import LegalMoveStrategy
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
    def __init__(self, position: Optional[Position] = None) -> None:
        self.position = position or Position(STANDARD_STARTING_POSITION, Color.white)
        self.move_history = []
        self._active_player = Color.white
        self.captured_pieces = []
        self.is_playing = True

        # TODO: break this out into a Computer class
        self.computer = None
        self.is_computer_playing = None
        self.computer_color = None

    @property
    def active_player(self):
        return self._active_player

    @active_player.setter
    def active_player(self, new_player):
        self._active_player = new_player
        self.position.active_player = new_player

    def next_player(self) -> Color:
        return Color.white if self.active_player == Color.black else Color.black

    @property
    def inactive_player(self) -> Color:
        return Color.white if self.active_player == Color.black else Color.white

    def show(self) -> None:
        screen = []
        evaluation = round(self.computer.evaluate(self.position), 3)
        print("Evaluation: {}".format(evaluation))
        for index, line in enumerate(str(self.position).split('\n')):
            print(8 - index, line)
        print(" " * 4 + '    '.join(x for x in A_THRU_H))


    def move(self, origin: Any, destination: Any) -> None:
        square = self.position[origin]
        new_square = self.position[destination]

        if square.is_empty():
            raise ValueError("That square is empty!")

        if square.piece.color != self.active_player:
            raise IllegalMoveException("That piece belongs to {}!".format(self.active_player.name))

        legal_moves = self.position.legal_moves_for_square(square)

        logging.info("Legal moves for %s: %s", square, legal_moves)

        if new_square.index not in legal_moves:
            raise IllegalMoveException("You can't move that there!")

        captured_piece = None

        if new_square.is_occupied():
            captured_piece = self.position[new_square].piece
            self.captured_pieces.append(captured_piece)

        square.piece, new_square.piece = None, square.piece

        logging.info("Moved the {} at {} to {}.".format(new_square.piece.name, origin, destination))

        self.move_history.append((origin, destination, captured_piece))
        self.active_player = self.next_player()

    def start_engine(self) -> None:
        self.computer = ChessEngine(self)

    def rewind(self) -> None:
        origin, destination, captured_piece = self.move_history.pop()

        original_square = self.position[origin].sqaure
        current_square = self.position[destination].square

        original_square.piece, current_square.piece = current_square.piece, captured_piece or None

        logging.info("Rewinded move {} to {}.".format(to_algebraic(origin), to_algebraic(destination)))

        self.active_player = self.next_player()

    def prompt_for_mode(self) -> None:
        self.is_computer_playing = True if input("Play against the computer? y/n > ") == "y" else False
        self.computer_color = Color.white if input("Choose black or white b/w > ") == 'b' else Color.black
        self.start_engine()

    @staticmethod
    def play() -> None:
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

    def is_occupied(self, square: Square) -> bool:
        return not self.is_empty(square)


def tmp_function_print_squares_for_pieces(game: Game) -> None:
    piece_to_check = random.choice(PIECE_TYPES)
    color_to_check = random.choice(COLORS)
    squares = game.position.find_piece_squares(piece_to_check, color_to_check)
    print("Randomly decided to show all positions of {} {}s".format(color_to_check.name,
                                                                    piece_to_check.name),
          end = ': ')
    print([to_algebraic(x) for x in squares])

class ChessException(Exception): pass
class IllegalMoveException(ChessException, ValueError): pass
