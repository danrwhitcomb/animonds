from math import pi
from random import randint

from util import geometry
from util.moves import FORWARD, LEFT_ROTATE, RIGHT_ROTATE, MOVES

MOVE_DIST = 10
ROTATE_DIST = pi / 8.0


class Animond:

    def __init__(self, id, loc):
        self.id = id
        self.loc = loc
        self.angle = 0
        self.lock = False

    def isLocked(self):
        return self.lock

    def getRandomMove(self):
        return MOVES[randint(0, len(MOVES)-1)]

    def applyMove(self, move):
        self.lock = True

        if move == FORWARD:
            self.loc = geometry.getPointInDirection(self.loc, self.angle, MOVE_DIST)
        elif move == LEFT_ROTATE:
            self.angle += ROTATE_DIST
        elif move == RIGHT_ROTATE:
            self.angle -= ROTATE_DIST
        else:
            print("Move not found")

        self.lock = False
