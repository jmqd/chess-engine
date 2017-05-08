import logging
from game import Game
from game import Position
from util import humanize_square_name

TEST_POSITION_1 = [
    'r', 'n', 'b', 'q', 'k', 'b', 'n', 'r',
    'p', 'p', 'p', ' ', 'p', 'p', 'p', 'p',
    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
    ' ', ' ', ' ', 'p', ' ', ' ', ' ', ' ',
    ' ', ' ', ' ', 'P', 'B', ' ', ' ', ' ',
    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
    'P', 'P', 'P', ' ', 'P', 'P', 'P', 'P',
    'R', 'N', ' ', 'Q', 'K', 'B', 'N', 'R'
        ]

def main():
    logging.basicConfig(level = logging.DEBUG)
    test_position = Position(TEST_POSITION_1)
    game = Game(test_position)
    game.show()
    print(set(humanize_square_name(x) for x in game.legal_moves_for_square('E4')))

if __name__ == '__main__':
    main()
