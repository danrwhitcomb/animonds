import pyglet
from pyglet.gl import *

from shapes import draw_square

R = 0
G = 0.1
B = 0.9

LENGTH = 30

class HomeView:

    def __init__(self, model):
        self.model = model

    def render(self):
        glColor3f(R, G, B)
        draw_square(self.model.loc[0], self.model.loc[1], 20)
