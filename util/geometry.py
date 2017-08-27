from math import sin, cos, sqrt, atan, pi
from sympy.geometry import point


def get_iso_triangle_for_center(center, length, direction, tip_angle):
    tip = get_point_in_direction(center, direction, length / 2.0)
    point1 = get_point_in_direction(tip, direction + tip_angle, -length)
    point2 = get_point_in_direction(tip, direction - tip_angle, -length)

    return point.Point2D(tip), point.Point2D(point1), point.Point2D(point2)


def get_point_in_direction(start, angle, dist):
    return point.Point2D((dist * sin(angle) + start[0], dist * cos(angle) + start[1]))


def distance(a, b):
    return float(a.distance(b))


def normalize_position(position, max_vals):
    return (float(position.x) / max_vals[0], float(position.y / max_vals[1]))


def normalize_angle(angle):
    '''
    Normalizes an angle in radians
    '''
    return angle / (2.0 * pi)
