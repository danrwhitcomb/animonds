from pyglet.gl import glColor3f

from util import shapes

R = 0
G = 0.1
B = 0.9

LENGTH = 30


class HomeView:

    def __init__(self,
                 color=(R, G, B),
                 size=LENGTH):
        self.color = color
        self.size = size

    def render(self, position):
        glColor3f(self.color[0], self.color[1], self.color[2])
        shapes.draw_square(position[0], position[1], self.size)
