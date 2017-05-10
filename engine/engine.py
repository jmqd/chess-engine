import random

class ChessEngine:
    def __init__(self, game):
        self.game = game

    def make_move(self):
        pass

    def choose_random_move(self):
        move = random.choice(self.game.find_all_legal_moves())
        print("Computer chose this move: {}".format(move))
        return move

