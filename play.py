import logging
import click

from src.game import Game
from src.position import Position
from src.game import STANDARD_STARTING_POSITION
from src.piece import Color
from tst.position_data import KNIGHT_FORK_POSITION

STARTING_POSITIONS = {
        'standard': STANDARD_STARTING_POSITION,
        'knight_fork': KNIGHT_FORK_POSITION
        }

@click.group('cli')
def cli() -> None: pass

@cli.command('play')
@click.option('--starting-position', type = str, required = False, default = 'standard')
@click.option('--color', type = str, required = False, default = 'white')
def play(starting_position: str, color: str) -> None:
    if color not in ('black', 'white'):
        raise ValueError("Color must be black or white.")

    starting_color = Color.white if color == 'white' else Color.black
    position = STARTING_POSITIONS[starting_position]
    Game.play(position, starting_color)

@cli.command('show-legal-moves')
@click.option('--starting-position', type = str, required = False, default = 'standard')
@click.option('--color', type = str, required = False, default = 'white')
def show_legal_moves(starting_position: str, color: str) -> None:
    if color not in ('black', 'white'):
        raise ValueError("Color must be black or white.")

    starting_color = Color.white if color == 'white' else Color.black
    position = Position(STARTING_POSITIONS[starting_position], starting_color)

    print(position)
    print([str(x) for x in position.find_all_legal_moves()])
    print(position.deserialize())

if __name__ == '__main__':
    cli()
