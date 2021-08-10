from numpy import matrix, array

APP_BG = 'BLACK'

# Rubik
SIDE_WIDTH = 70
OUT_CLR = 'WHITE'
CANVAS_WIDTH = 600
DOT_RAD = 5

SCROLL_SENS = 0.03

# Computed Rubik
CENT_POINT = matrix([[CANVAS_WIDTH // 2], [CANVAS_WIDTH // 2], [CANVAS_WIDTH // 2]])

DEBUG_CLRS = {0: 'RED', 1: 'ORANGE', 2: 'YELLOW', 3: 'GREEN',
              4: 'BLUE', 5: 'PINK', 6: 'PURPLE', 7: 'BROWN'}

T_CON = {0: 1,
         1: 5,
         5: 6,
         6: 0}

M_CON = {0: 2,
         1: 3,
         5: 7,
         6: 4}

D_CON = {2: 3,
         3: 7,
         7: 4,
         4: 2}

OCTANTS = {(1, -1, 1): 1,
           (-1, -1, 1): 2,
           (-1, 1, 1): 3,
           (1, 1, 1): 4,
           (1, -1, -1): 5,
           (-1, -1, -1): 6,
           (-1, 1, -1): 7,
           (1, 1, -1): 8}
