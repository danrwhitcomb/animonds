from math import sin, cos


def getPointInDirection(start, angle, dist):
    return (dist * sin(angle) + start[0],
            dist * cos(angle) + start[1])

def rotatePoint(angle, point, pivot=(0,0)):
    s = sin(angle)
    c = cos(angle)

    #Convert to origin reference frame
    point_o = (point[0] - pivot[0], point[1] - pivot[1])

    #Rotate
    new_p = (point_o[0] * c - point_o[1] * s, 
             point_o[0] * s + point_o[1] * c)

    return (new_p[0] + pivot[0], new_p[1] + pivot[1])