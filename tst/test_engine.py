import logging
import pytest

from src.piece import Color
from src.game import Game
from src.position import Position, Square
from src.util import to_algebraic, to_numeric
from tst.util import InvalidMoveException
from tst.util import DidNotFindAllLegalMovesException

from tst.position_data import KNIGHT_FORK_POSITION

def check_computer_makes_right_move(position: Position, expected_move: str) -> None:
    game = Game(position)
    game.start_engine()

    evaluated_position = game.computer.evaluate(game.position)
    next_possible_positions_evaluated = game.computer.tree[evaluated_position]
    next_possible_positions_evaluated.sort(key = lambda x: x.evaluation)

    if expected_move is not None:
        assert next_possible_positions_evaluated.move_history[-1] == expected_move

def test():
    position = Position(KNIGHT_FORK_POSITION, Color.white)
    check_computer_makes_right_move(position, expected_move = None)

if __name__ == '__main__':
    test()
