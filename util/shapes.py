from math import cos, sin, pi
from pyglet.gl import glVertex2f, glBegin, glEnd, GL_POLYGON, GL_QUADS


def draw_circle(center, radius):
    sides = 64

    glBegin(GL_POLYGON)
    for i in range(100):
        cosine = radius * cos(i * 2 * pi / sides) + center[0]
        sine = radius * sin(i * 2 * pi / sides) + center[1]
        glVertex2f(cosine, sine)
    glEnd()


def draw_square(x, y, size):
    glBegin(GL_QUADS)  # start drawing a rectangle

    glVertex2f(x, y)                # bottom left point
    glVertex2f(x + size, y)         # bottom right point
    glVertex2f(x + size, y + size)  # top right point
    glVertex2f(x, y + size)         # top left point

    glEnd()
