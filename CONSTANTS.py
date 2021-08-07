from numpy import matrix, sin, cos


APP_BG = 'BLACK'

# Rubik
SIDE_WIDTH = 70
OUT_CLR = 'WHITE'
RUBIKS_CANV_WIDTH = 400
DOT_RAD = 3

SCROLL_SENS = 0.03


# Computed Rubik
CENT_POINT = matrix([[RUBIKS_CANV_WIDTH // 2], [RUBIKS_CANV_WIDTH // 2], [RUBIKS_CANV_WIDTH // 2]])


ROTATIONS = {'x': lambda t: matrix([[1, 0, 0], [0, cos(t), -sin(t)], [0, sin(t), cos(t)]]),
             'y': lambda t: matrix([[cos(t), 0, sin(t)], [0, 1, 0], [-sin(t), 0, cos(t)]]),
             'z': lambda t: matrix([[cos(t), -sin(t), 0], [sin(t), cos(t), 0], [0, 0, 1]])}

DEBUG_CLRS = {0: 'RED', 1: 'ORANGE', 2: 'YELLOW', 3: 'GREEN',
              4: 'BLUE', 5: 'PINK', 6: 'PURPLE', 7: 'BROWN'}