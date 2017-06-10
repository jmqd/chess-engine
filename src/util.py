import logging
from typing import Tuple

MoveFacts = Tuple[int, int, int, int, int]
A_THRU_H = 'ABCDEFGH'

# pre-compute an array mapping to algebraic notation
NUMERICAL_TO_ALGEBRAIC = ["{}{}".format(l, n) for n in range(8, 0, -1) for l in A_THRU_H]

# pre-compute a dict mapping to the index
ALGEBRAIC_TO_NUMERICAL = {a:n for n, a in enumerate(NUMERICAL_TO_ALGEBRAIC)}

TOP_LEFT_SQUARE = 0
BOTTOM_RIGHT_SQUARE = 63

def to_algebraic(index: int) -> str:
    try:
        return NUMERICAL_TO_ALGEBRAIC[index]
    except IndexError:
        return index

def to_numeric(algebraic_notation: str) -> int:
    try:
        return ALGEBRAIC_TO_NUMERICAL[algebraic_notation.upper()]
    except IndexError:
        return algebraic_notation

def get_move_facts(origin: int, move: int) -> MoveFacts:
    square_if_moved = origin + move
    current_col = origin % 8
    col_if_moved = (origin + move) % 8
    col_dist_if_moved = abs(current_col - col_if_moved)
    row_dist = get_row_distance(origin, move)
    return (square_if_moved,
            current_col,
            col_if_moved,
            col_dist_if_moved,
            row_dist)

def get_row_distance(src: int, move: int) -> int:
    src_row = src // 8
    row_if_moved = (src + move) // 8
    return abs(src_row - row_if_moved)

def is_on_board(square: int) -> bool:
    return TOP_LEFT_SQUARE <= square <= BOTTOM_RIGHT_SQUARE

def is_valid_move(src_square: int, move: int) -> bool:
    return is_on_board(src_square + move)

