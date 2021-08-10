from numpy import matrix, sin, cos


ROTATIONS = {'x': lambda t: matrix([[1, 0, 0], [0, cos(t), -sin(t)], [0, sin(t), cos(t)]]),
             'y': lambda t: matrix([[cos(t), 0, sin(t)], [0, 1, 0], [-sin(t), 0, cos(t)]]),
             'z': lambda t: matrix([[cos(t), -sin(t), 0], [sin(t), cos(t), 0], [0, 0, 1]])}