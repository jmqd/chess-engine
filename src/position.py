import copy
import operator
import logging
from typing import Sequence, List, Dict, Tuple, Any, Optional

from move import LegalMoveStrategy
from piece import Piece
from piece import Color

from util import to_algebraic
from util import to_numeric
from util import get_move_facts

Move = Tuple[int, int]
EMPTY_BOARD = [' '] * 64
VERTICAL_STEP = 8
HORIZONTAL_STEP = 1

class Square:
    def __init__(self, index: Any, piece: Optional[Piece] = None):
        self.index = index
        self.algebraic_index = to_algebraic(index)
        self.piece = piece

    @property
    def piece(self) -> Piece:
        return self._piece

    @piece.setter
    def piece(self, val: Piece) -> None:
        self._piece = val

        if self._piece:
            self._piece.square = self

    def is_empty(self) -> bool:
        return self.piece is None

    def is_occupied(self) -> bool:
        return self.piece is not None

    def occupied_by(self) -> Optional[Color]:
        if self.piece is None:
            return None
        else:
            return self.piece.color

    def __str__(self) -> str:
        if self.piece is None:
            return ' '
        else:
            return str(self.piece)


class Position:
    def __init__(self, position_data: List[str], active_player: Color = Color.white) -> None:
        self.grid = self.serialize(position_data)
        self.active_player = active_player

        # state for iterator. probs should refactor this
        self.__it_checkpoint = -1

    def find_all_legal_moves(self) -> Sequence[Tuple[int]]:
        legal_moves = []
        for i, square in enumerate(self):
            if square.is_empty() or square.piece.color != self.active_player: continue
            for legal_move in self.legal_moves_for_square(square):
                legal_moves.append((i, legal_move))
        return legal_moves

    def legal_moves_for_square(self, square: Square) -> Sequence[int]:
        return LegalMoveStrategy.of(square.piece)(self, square).get_legal_moves()

    def is_empty_or_capturable(self, square: Square) -> bool:
        return self.is_empty(square) or self.is_capturable(square)

    def is_empty(self, index: Any) -> bool:
        logging.debug("Checking if %s is empty...", index)
        result = self[index].is_empty()
        logging.debug("%s is %s", index, 'empty' if result else 'not empty')
        return result

    def is_capturable(self, index: Any) -> bool:
        logging.debug("Checking if %s is capturable...", index)
        result = not self.is_empty(index) and self[index].piece.color != self.active_player
        logging.debug("%s is %s", to_algebraic(index), 'capturable' if result else 'not capturable')
        return result

    def find_piece_squares(self, piece_class: Piece, color: Color) -> List[int]:
        square_indices = []
        for sq_index, square in enumerate(self):
            if square.occupied_by() == color and isinstance(square.piece, piece_class):
                square_indices.append(sq_index)
        return square_indices

    def is_path_clear(self, origin: int, displacement: int) -> bool:
        (square_if_moved, current_col,
         col_if_moved, col_dist_if_moved,
         row_dist) = get_move_facts(origin, displacement)

        # moving horizontally? (iff)
        if row_dist == 0 and col_dist_if_moved > 0:
            step_magnitude = HORIZONTAL_STEP

        # moving vertically? (iff)
        if row_dist > 0 and col_dist_if_moved == 0:
            step_magnitude = VERTICAL_STEP

        # moving diaganolly? (iff)
        if row_dist > 0 and col_dist_if_moved > 0:
            step_magnitude = 9 if displacement % 9 == 0 else 7

        '''If our displacement is negative, we're moving to the left in the
        position array. And vice-a-versa.

        e.g.

        ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1']

        Say I have a rook on H1 and I move it to E1.
        My index goes from 7 to 4.
        '''
        step = operator.__add__ if displacement < 0 else operator.__sub__

        '''Starting from the origin square and moving forward towards its target
        destination, while we are not yet at the target square, check if this
        square is empty.
        '''
        steps_taken = step_magnitude
        while steps_taken < displacement:
            if not self[origin + steps_taken].is_empty():
                return False
            steps_taken = step(steps_taken, step_magnitude)
        return True

    def successors(self):
        positions = []
        for move in self.find_all_legal_moves():
            positions.append(self.get_transposition(move))
        return positions

    def get_transposition(self, move: Move) -> object:
        origin, destination = move
        new_position = copy.deepcopy(self)
        new_position[origin].piece, new_position[destination].piece = None, new_position[origin].piece
        return new_position


    @staticmethod
    def serialize(data: List[str]) -> List[Square]:
        internal_position = copy.deepcopy(EMPTY_BOARD)
        for index, notated_char in enumerate(data):
            internal_position[index] = Square(index, Piece.from_notation(notated_char))
        return internal_position

    def __str__(self) -> str:
        list_repr = []
        for first_sq_in_row in range(0, 64, 8):
            list_repr.append(str([str(x) for x in self.grid[first_sq_in_row:first_sq_in_row + 8]]))
        return '\n'.join(list_repr)

    def __iter__(self):
        return self

    def __next__(self) -> Square:
        self.__it_checkpoint += 1
        if self.__it_checkpoint > 63:
            self.__it_checkpoint = -1
            raise StopIteration
        return self.grid[self.__it_checkpoint]


    def __getitem__(self, square: Any) -> Square:
        if type(square) == int:
            index = square
        elif type(square) == str:
            index = to_numeric(square)
        elif type(square) == Square:
            index = square.index
        return self.grid[index]

    def __setitem__(self, square: Any, value: Any) -> None:
        index = square if type(square) == int else to_numeric(square)
        self.grid[index] = value


