import logging
import pytest

from piece import Color
from game import Game, STANDARD_STARTING_POSITION
from game import Position

'''
TODO:
    import and use pytest
'''

TEST_POSITION_1 = [
    'r', ' ', ' ', 'q', 'k', 'b', 'n', 'r',
    'p', 'p', ' ', 'b', 'p', 'p', 'p', 'p',
    'n', ' ', 'p', ' ', ' ', ' ', ' ', ' ',
    ' ', ' ', ' ', 'p', ' ', 'R', ' ', ' ',
    ' ', ' ', ' ', 'P', 'B', ' ', ' ', ' ',
    ' ', ' ', 'N', 'Q', ' ', ' ', ' ', ' ',
    'P', 'P', 'P', ' ', 'P', 'P', 'P', 'P',
    ' ', ' ', ' ', ' ', 'K', 'B', 'N', 'R'
        ]

def main() -> None:
    logging.basicConfig(level = logging.WARN)
    Game.play()

def test_pawn_distance_to_promotion() -> None:
    position = Position(TEST_POSITION_1, Color.white)
    assert position['D4'].piece.distance_from_promotion() == 4
    assert position['A2'].piece.distance_from_promotion() == 6
    assert position['A7'].piece.distance_from_promotion() == 6
    assert position['D5'].piece.distance_from_promotion() == 4
    assert position['C6'].piece.distance_from_promotion() == 5
    print('test pawn passed')

def test_number_opening_moves() -> None:
    position = Position(STANDARD_STARTING_POSITION, Color.white)
    assert len(position.successors()) == 20

if __name__ == '__main__':
    main()
