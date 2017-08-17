from pyglet.gl import glBegin, glColor3f, glVertex2f, glEnd, GL_TRIANGLES
from util import geometry

ANGLE = 0.2
LENGTH = 50

WHITE = (1, 1, 1)
GREEN = (0, 1, 0)


class AnimondView:

    def __init__(self,
                 normal_color=WHITE,
                 food_color=GREEN,
                 angle=ANGLE,
                 length=LENGTH):
        self.normal_color = normal_color
        self.food_color = food_color
        self.angle = angle
        self.length = length

    def render(self, position, current_angle, has_food) -> None:
        angle1 = current_angle + self.angle
        angle2 = current_angle - self.angle

        tip = geometry.get_point_in_direction(position, current_angle, self.length / 2.0)
        point1 = geometry.get_point_in_direction(tip, angle1, -self.length)
        point2 = geometry.get_point_in_direction(tip, angle2, -self.length)
        color = self.food_color if has_food else self.normal_color

        glBegin(GL_TRIANGLES)

        glColor3f(color[0], color[1], color[2])
        glVertex2f(tip[0], tip[1])
        glVertex2f(point1[0], point1[1])
        glVertex2f(point2[0], point2[1])

        glEnd()
