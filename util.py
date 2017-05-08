import logging

A_THRU_H = 'ABCDEFGH'
TOP_LEFT_SQUARE = 0
BOTTOM_RIGHT_SQUARE = 63

def humanize_square_name(index):
    string_index = str(index)
    distance_from_top = index // 8
    row = 8 - distance_from_top
    col = A_THRU_H[index % 8]
    return col + str(row)

def dehumanize_square_name(algebraic_notation):
    col, row = algebraic_notation[0], algebraic_notation[1]
    square = 8 * (8 - int(row)) + A_THRU_H.index(col)
    logging.info("%s is human format. Representing as %s", algebraic_notation, square)
    return square

def get_move_facts(origin, move):
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

def get_row_distance(src, move):
    src_row = src // 8
    row_if_moved = (src + move) // 8
    return abs(src_row - row_if_moved)

def is_on_board(square):
    return TOP_LEFT_SQUARE <= square <= BOTTOM_RIGHT_SQUARE

def is_valid_move(src_square, move):
    return is_on_board(src_square + move)

