from numpy import matrix, array


class Form:
    def __init__(self, width, height, depth):
        self.width = width
        self.height = height
        self.depth = depth
        self.points = None
        self.T_CON = None
        self.M_CON = None
        self.D_CON = None
        self.faces = None


class Cube(Form):
    def __init__(self, width=1, height=1, depth=1):
        super(Cube, self).__init__(width=width, height=height, depth=depth)
        width /= 2
        height /= 2
        depth /= 2
        self.points = array([matrix([[-width], [-height], [depth]]), matrix([[width], [-height], [depth]]),
                             matrix([[-width], [height], [depth]]), matrix([[width], [height], [depth]]),
                             matrix([[-width], [height], [-depth]]), matrix([[width], [-height], [-depth]]),
                             matrix([[-width], [-height], [-depth]]), matrix([[width], [height], [-depth]]),
                             ])

        self.T_CON = {0: 1,
                      1: 5,
                      5: 6,
                      6: 0
                      }

        self.M_CON = {0: 2,
                      1: 3,
                      5: 7,
                      6: 4
                      }

        self.D_CON = {2: 3,
                      3: 7,
                      7: 4,
                      4: 2
                      }

        self.faces = [(0, 1, 3, 2),
                      (1, 5, 7, 3),
                      (5, 6, 4, 7),
                      (6, 0, 2, 4),
                      (0, 1, 5, 6),
                      (2, 3, 7, 4)]

        self.f_colors = ['WHITE', 'RED', 'YELLOW',
                         'ORANGE', 'BLUE', 'GREEN']


class TriangularPrism(Form):
    def __init__(self, width=1, height=1, depth=1):
        super(TriangularPrism, self).__init__(width=width, height=height, depth=depth)
        self.points = array([matrix([[0], [-height], [depth]]), matrix([[-width], [height], [depth]]),
                             matrix([[width], [height], [depth]]), matrix([[width], [height], [-depth]]),
                             matrix([[-width], [height], [-depth]]), matrix([[0], [-height], [-depth]]),
                             ])

        self.T_CON = {0: 5}

        self.M_CON = {0: 1,
                      2: 0,
                      5: 3,
                      4: 5
                      }

        self.D_CON = {1: 2,
                      2: 3,
                      3: 4,
                      4: 1
                      }
