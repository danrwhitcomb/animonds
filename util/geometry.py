from math import sin, cos, sqrt, atan, pi


def get_point_in_direction(start, angle, dist):
    return (dist * sin(angle) + start[0],
            dist * cos(angle) + start[1])


def rotate_point(angle, point, pivot=(0, 0)):
    s = sin(angle)
    c = cos(angle)

    # Convert to origin reference frame
    point_o = (point[0] - pivot[0], point[1] - pivot[1])

    # Rotate
    new_p = (point_o[0] * c - point_o[1] * s,
             point_o[0] * s + point_o[1] * c)

    return (new_p[0] + pivot[0], new_p[1] + pivot[1])


def distance(a, b):
    return sqrt(((a[0] - b[0]) ** 2) + ((a[1] - b[1]) ** 2))


def angle_difference(angle, point_a, point_b):
    y_delta = float(point_b[1] - point_a[1])
    x_delta = float(point_b[0] - point_a[0])
    sigma = atan(x_delta / y_delta)

    theta1 = angle - sigma
    theta2 = (2 * pi) - theta1

    return (theta1, theta2)


def normalize_position(position, max_vals):
    return (float(position[0]) / max_vals[0], float(position[1] / max_vals[1]))


def normalize_angle(angle):
    '''
    Normalizes an angle in radians
    '''
    return angle / (2.0 * pi)
