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
    Game.play()

if __name__ == '__main__':
    main()
