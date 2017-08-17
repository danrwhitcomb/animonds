from pyglet.gl import glColor3f

from util import shapes

R = 0
G = 1.0
B = 0

RADIUS = 15


class FoodView:

    def __init__(self,
                 color=(R, G, B),
                 size=RADIUS):
        self.color = color
        self.size = size

    def render(self, position):
        glColor3f(self.color[0], self.color[1], self.color[2])
        shapes.draw_circle(position, self.size)
