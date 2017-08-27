from pyglet.gl import glColor3f

from util import shapes

class HomeView:

    def render(self, position, size, color):
        glColor3f(color[0], color[1], color[2])
        shapes.draw_square(position[0], position[1], size)
