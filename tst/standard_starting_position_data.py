from src.game import STANDARD_STARTING_POSITION
from src.piece import Color
from src.position import Position

position = {
        'white_playing': Position(STANDARD_STARTING_POSITION, Color.white),
        'black_playing': Position(STANDARD_STARTING_POSITION, Color.black)
        }

legal_moves= {
        'white_playing': {
            'A2': {'A3', 'A4'},
            'B2': {'B3', 'B4'},
            'C2': {'C3', 'C4'},
            'D2': {'D3', 'D4'},
            'E2': {'E3', 'E4'},
            'F2': {'F3', 'F4'},
            'G2': {'G3', 'G4'},
            'H2': {'H3', 'H4'},
            'A1': set(),
            'B1': {'A3', 'C3'},
            'C1': set(),
            'D1': set(),
            'E1': set(),
            'F1': set(),
            'G1': {'F3', 'H3'},
            'H1': set(),
            'C7': set(),
            'A1': set()
            },
        'black_playing': {
            'A7': {'A6', 'A5'},
            'B7': {'B6', 'B5'},
            'C7': {'C6', 'C5'},
            'D7': {'D6', 'D5'},
            'E7': {'E6', 'E5'},
            'F7': {'F6', 'F5'},
            'G7': {'G6', 'G5'},
            'H7': {'H6', 'H5'},
            'A8': set(),
            'B8': {'A6', 'C6'},
            'C8': set(),
            'D8': set(),
            'E8': set(),
            'F8': set(),
            'G8': {'F6', 'H6'},
            'H8': set(),
            }
        }
