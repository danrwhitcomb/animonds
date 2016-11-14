from random import randint
from util.moves import MOVES


class RandomPredictor:

    def getMove(self, animond):
        return MOVES[randint(0, len(MOVES)-1)]
