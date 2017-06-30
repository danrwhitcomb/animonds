import pyglet
from pyglet.gl import *

from shapes import draw_circle

R = 0
G = 1.0
B = 0

RADIUS = 30

class FoodView:
    def __init__(self, model):
        self.model = model

    def render(self):
        glColor3f(R, G, B)
        draw_circle(self.model.loc, 15)
