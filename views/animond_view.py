import pyglet
from pyglet.gl import *
from util import geometry

ANGLE = 0.2
LENGTH = 50

class AnimondView:

    def __init__(self, model):
        self.model = model

    def render(self): 
        while self.model.isLocked():
            print("Locked!")
            continue

        angle1 = self.model.angle + ANGLE
        angle2 = self.model.angle - ANGLE

        tip = geometry.getPointInDirection(self.model.loc, self.model.angle, LENGTH / 2.0)
        point1 = geometry.getPointInDirection(tip, angle1, -LENGTH)
        point2 = geometry.getPointInDirection(tip, angle2, -LENGTH)

        glBegin(GL_TRIANGLES)

        glColor3f(1.0, 1.0, 1.0)
        glVertex2f(tip[0], tip[1])
        glVertex2f(point1[0], point1[1])
        glVertex2f(point2[0], point2[1])

        glEnd()