from pyglet.gl import glColor3f
from util import shapes


class FoodView:

    def render(self, position, size, color):
        glColor3f(color[0], color[1], color[2])
        shapes.draw_circle(position, size)
