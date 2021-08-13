from numpy import array, matrix

# Main window
APP_BG = 'BLACK'
APP_WDT = 600
APP_HGT = 800

# Rubik
SIDE_WIDTH = (APP_WDT - 100) / 5
OUT_CLR = 'WHITE'
DOT_RAD = 5

# Canvas
CANVAS_WDT = (APP_WDT - 5)
CANVAS_HGT = CANVAS_WDT
CENTER = CANVAS_WDT / 2

# Computed Rubik
CENT_POINT = array([CANVAS_WDT / 2, CANVAS_WDT / 2, 0])
L1 = array([])

# Control Panel
CTRL_PNL_WDT = APP_WDT - CANVAS_WDT
CTRL_PNL_HGT = 200


# Cube
def CUBE(width, height, depth, x_offset: float = 0, y_offset: float = 0, z_offset: float = 0):
    width /= 2
    height /= 2
    depth /= 2
    return array([matrix([[-width + x_offset], [-height + y_offset], [depth + z_offset]]),
                  matrix([[width + x_offset], [-height + y_offset], [depth + z_offset]]),
                  matrix([[-width + x_offset], [height + y_offset], [depth + z_offset]]),
                  matrix([[width + x_offset], [height + y_offset], [depth + z_offset]]),
                  matrix([[-width + x_offset], [height + y_offset], [-depth + z_offset]]),
                  matrix([[width + x_offset], [-height + y_offset], [-depth + z_offset]]),
                  matrix([[-width + x_offset], [-height + y_offset], [-depth + z_offset]]),
                  matrix([[width + x_offset], [height + y_offset], [-depth + z_offset]])])


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

CUBE_FACES = {'FRONT': (0, 1, 3, 2),
              'RIGHT': (1, 5, 7, 3),
              'BACK': (5, 6, 4, 7),
              'LEFT': (6, 0, 2, 4),
              'TOP': (0, 1, 5, 6),
              'BOTTOM': (2, 3, 7, 4)}

CUBE_CLRS = {'FRONT': 'WHITE',
             'RIGHT': 'RED',
             'BACK': 'YELLOW',
             'LEFT': 'ORANGE',
             'TOP': 'BLUE',
             'BOTTOM': 'GREEN'}

OCTANTS = {(1, -1, 1): 1,
           (-1, -1, 1): 2,
           (-1, 1, 1): 3,
           (1, 1, 1): 4,
           (1, -1, -1): 5,
           (-1, -1, -1): 6,
           (-1, 1, -1): 7,
           (1, 1, -1): 8}
