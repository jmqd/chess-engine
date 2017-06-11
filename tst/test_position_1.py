from src.position import Position
from src.piece import Color

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

def test_pawn_distance_to_promotion() -> None:
    position = Position(TEST_POSITION_1, Color.white)
    assert position['D4'].piece.distance_from_promotion() == 4
    assert position['A2'].piece.distance_from_promotion() == 6
    assert position['A7'].piece.distance_from_promotion() == 6
    assert position['D5'].piece.distance_from_promotion() == 4
    assert position['C6'].piece.distance_from_promotion() == 5

