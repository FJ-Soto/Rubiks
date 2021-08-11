from numpy import array
from math import sqrt

APP_BG = 'BLACK'
APP_WDT = 600
APP_HGT = 800

# Rubik

SIDE_WIDTH = 70
OUT_CLR = 'WHITE'
CANVAS_WDT = sqrt((3 * SIDE_WIDTH) ** 2 * 2) + 50
CANVAS_HGT = CANVAS_WDT

CTRL_PNL_WDT = APP_WDT - sqrt((3 * SIDE_WIDTH) ** 2 * 2) + 50
CTRL_PNL_HGT = 200
DOT_RAD = 5

SCROLL_SENS = 0.03

# Computed Rubik
CENT_POINT = array([CANVAS_WDT / 2, CANVAS_WDT / 2, CANVAS_WDT / 2])

DEBUG_CLRS = {0: 'RED',
              1: 'ORANGE',
              2: 'YELLOW',
              3: 'GREEN',
              4: 'BLUE',
              5: 'PINK',
              6: 'PURPLE',
              7: 'BROWN'}

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
