import logging
import pytest

from src.piece import Color
from src.game import Game
from src.position import Position, Square
from src.util import to_algebraic, to_numeric
from tst.util import InvalidMoveException
from tst.util import DidNotFindAllLegalMovesException

from tst.standard_starting_position_data import position as position
from tst.standard_starting_position_data import legal_moves

def check_number_opening_moves(pos, expected) -> None:
    pos = Position(STANDARD_STARTING_POSITION, Color.white)
    assert len(pos.successors()) == expected

def check_legal_moves(pos, square, expected):
    moves = pos.legal_moves_for_square(square)
    for move in moves:
        algebraic_move = to_algebraic(move.destination)
        try:
            expected.remove(algebraic_move)
        except KeyError:
            raise InvalidMoveException('{} is an invalid move for square {} in position\n{}'.format(
                algebraic_move, square, pos))
    try:
        assert len(expected) == 0
    except Exception as e:
        raise DidNotFindAllLegalMovesException("Didn't find all the moves... moves: {}, expected: {}".format(
            moves, expected))

def test_white() -> None:
    for square, expected in legal_moves['white_playing'].items():
        square = position['white_playing'][square]
        check_legal_moves(position['white_playing'], square, expected)

def test_black() -> None:
    for square, expected in legal_moves['black_playing'].items():
        square = position['black_playing'][square]
        check_legal_moves(position['black_playing'], square, expected)

