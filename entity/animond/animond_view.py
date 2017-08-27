from pyglet.gl import glBegin, glColor3f, glVertex2f, glEnd, GL_TRIANGLES
from util import geometry


LENGTH = 50

WHITE = (1, 1, 1)
GREEN = (0, 1, 0)


class AnimondView:

    def __init__(self,
                 normal_color=WHITE,
                 food_color=GREEN):
        self.normal_color = normal_color
        self.food_color = food_color

    def render(self, triangle, has_food):
        color = self.food_color if has_food else self.normal_color

        glBegin(GL_TRIANGLES)

        glColor3f(color[0], color[1], color[2])
        for v in triangle.vertices:
            glVertex2f(*v)

        glEnd()
