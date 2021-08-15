from numpy import array, pi

# Main window
APP_BG = 'BLACK'
APP_WDT = 600
APP_HGT = 500
MIN_WDT = 1240
MIN_HGT = 680
RESIZE_WDT = True
RESIZE_HGT = True

# Label Font
LBL_FONT = 'TkDefaultFont 10 bold'

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

# Control Panel
CTRL_PNL_WDT = APP_WDT - CANVAS_WDT
CTRL_PNL_HGT = 200


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

# Control Panel
TICK_INT = 90
SHOW_FACES = False
SHOW_OUTLINE = False
SHOW_POINTS = False


# the x and y thetas are opposite signed since (0, 0)
# is the top left side of the canvas
X_THETA = 2 * pi / 180
Y_THETA = -2 * pi / 180
Z_THETA = 0 * pi / 180
