import logging
from game import Game
from game import Position
from util import humanize_square_name

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

def main():
    logging.basicConfig(level = logging.DEBUG)
    test_position = Position(TEST_POSITION_1)
    game = Game(test_position)
    game.show()
    print(set(humanize_square_name(x) for x in game.legal_moves_for_square('F5')))
    print(set(humanize_square_name(x) for x in game.legal_moves_for_square('D3')))
    game.show()

if __name__ == '__main__':
    main()
