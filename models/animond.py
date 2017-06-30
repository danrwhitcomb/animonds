from math import pi
from random import randint

from util import geometry
from util.moves import FORWARD, LEFT_ROTATE, RIGHT_ROTATE, MOVES

MOVE_DIST = 10
ROTATE_DIST = pi / 8.0


class Animond:

    def __init__(self, id, loc, max_dim, has_food=False):
        self.id = id
        self.loc = loc
        self.max_dim = max_dim
        self.angle = 0
        self.lock = False
        self.has_food = False

    def is_locked(self):
        return self.lock

    def set_state(self, location, angle, has_food):
        self.loc = location
        self.angle = angle
        self.has_food = has_food

    def apply_move(self, move):
        self.lock = True

        if move == FORWARD:
            new_location = geometry.getPointInDirection(self.loc, self.angle, MOVE_DIST)
            self.loc = (min(new_location[0], self.max_dim[0]), min(new_location[1], self.max_dim[1]))
            self.loc = (max(0, self.loc[0]), max(0, self.loc[1]))

        elif move == LEFT_ROTATE:
            self.angle += ROTATE_DIST
        elif move == RIGHT_ROTATE:
            self.angle -= ROTATE_DIST
        else:
            print("Move not found")

        self.lock = False
