import copy
import operator
import logging
from typing import Sequence, List, Dict, Tuple, Any, Optional

from src.move import LegalMoveStrategy
from src.piece import Piece
from src.piece import Color

from src.util import to_algebraic
from src.util import to_numeric
from src.util import get_move_facts

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
        return '{}: {}'.format(self.algebraic_index, self.piece)


class Position:
    def __init__(self, position_data: List[str], active_player: Color = Color.white) -> None:
        if position_data is not None:
            self.grid = self.serialize(position_data)

        self.active_player = active_player

        # state for iterator. probs should refactor this
        self.__it_checkpoint = -1
        self.evaluation = None
        self.depth = None
        self.move_history = []

    def find_all_legal_moves(self) -> Sequence[Tuple[int]]:
        legal_moves = []
        for square in self:
            if square.is_empty() or square.piece.color != self.active_player: continue
            legal_moves.extend(self.legal_moves_for_square(square))
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

    def is_path_clear(self, move: Move) -> bool:
        '''If our displacement is negative, we're moving to the left in the
        position array. And vice-a-versa.

        e.g.

        ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1']

        Say I have a rook on H1 and I move it to E1.
        My index goes from 7 to 4.

        Starting from the origin square and moving forward towards its target
        destination, while we are not yet at the target square, check if this
        square is empty.
        '''
        steps_taken = move.direction.value
        while abs(steps_taken) < abs(move.delta):
            square_to_check = move.origin + steps_taken
            logging.info("Checking %s...", to_algebraic(square_to_check))
            if not self[square_to_check].is_empty():
                logging.info("Something was in the way on %s", to_algebraic(square_to_check))
                return False
            steps_taken += move.direction.value
        logging.info("Path was clear for %s to %s", to_algebraic(move.origin), to_algebraic(move.origin + move.delta))
        return True

    def successors(self):
        positions = []
        positions.extend(self.get_transposition(x) for x in self.find_all_legal_moves())
        return positions

    def get_transposition(self, move: Move) -> object:
        new_active_player = Color.black if self.active_player == Color.white else Color.white
        transposition = Position(self.deserialize(), new_active_player)
        transposition.swap(move)
        return transposition

    def swap(self, move: Move) -> None:
        self[move.origin].piece, self[move.destination].piece = None, self[move.origin].piece
        self.move_history.append(move)

    @staticmethod
    def serialize(data: List[str]) -> List[Square]:
        internal_position = copy.deepcopy(EMPTY_BOARD)
        for index, notated_char in enumerate(data):
            internal_position[index] = Square(index, Piece.from_notation(notated_char))
        return internal_position

    def deserialize(self) -> List[str]:
        deserialized_position = [None] * 64
        for i, square in enumerate(self):
            deserialized_position[i] = str(square.piece) if square.piece else ' '
        return deserialized_position

    def __str__(self) -> str:
        list_repr = []
        for first_sq_in_row in range(0, 64, 8):
            list_repr.append(str([str(x.piece or ' ') for x in self.grid[first_sq_in_row:first_sq_in_row + 8]]))
        return "To move: {}\n{}".format(self.active_player, '\n'.join(list_repr))

    def __hash__(self):
        return hash(str(self))

    def get_pretty_text(self) -> str:
        list_repr = []
        for first_sq_in_row in range(0, 64, 8):
            list_repr.append(str([str(x.piece or ' ') for x in self.grid[first_sq_in_row:first_sq_in_row + 8]]))
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


