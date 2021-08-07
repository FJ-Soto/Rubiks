from tkinter import *

from numpy import matrix, cos, sin, tan, dot, add, abs, sign

from CONSTANTS import OUT_CLR, RUBIKS_CANV_WIDTH, SIDE_WIDTH, CENT_POINT, DOT_RAD, ROTATIONS, DEBUG_CLRS
from Coordinate import Coordinate


class RubikCanvas(Canvas):
    def __init__(self, master=None, width=RUBIKS_CANV_WIDTH):
        super().__init__(master=master, width=width, height=width)
        self.config(highlightthickness=1, highlightbackground=OUT_CLR)

        self.edge_points = [matrix([[-1], [-1], [1]]), matrix([[1], [-1], [1]]),
                            matrix([[1], [1], [1]]), matrix([[-1], [1], [1]]),
                            matrix([[-1], [1], [-1]]), matrix([[1], [1], [-1]]),
                            matrix([[1], [-1], [-1]]), matrix([[-1], [-1], [-1]])]

        self.d_lines = []
        self.d_points = []

        self.bind("<Button-1>", self.set_xy)
        self.bind("<B1-Motion>", self.onDrag)
        self.xtheta = 0
        self.ytheta = 0
        self.ztheta = 0
        self.curLastPos = None

        self.initialize_cube()
        # self.draw_point(CENT_POINT)

    def set_xy(self, e):
        if self.curLastPos is None:
            self.curLastPos = Coordinate(x=e.x_root, y=e.y_root)
        else:
            self.curLastPos.x = e.x_root
            self.curLastPos.y = e.y_root

    def onDrag(self, e):
        self.ytheta += tan((self.curLastPos.y - e.y_root) / SIDE_WIDTH)
        self.xtheta += tan((self.curLastPos.x - e.x_root) / SIDE_WIDTH)
        self.curLastPos.x = e.x_root
        self.curLastPos.y = e.y_root

        self.draw_cube()
        print(self.edge_points[0], e.x_root, e.y_root)

    # TODO: Investigate a possible fix for the perspective skew.
    def draw_cube(self, rad=DOT_RAD):
        for i, point in enumerate(self.edge_points):
            _p = self.projected_point(point)

            # move instead of redraw to improve performance and memory usage
            self.coords(self.d_points[i], as_dot(_p))

            _prev_point = self.projected_point(self.edge_points[i - 1])

            self.coords(self.d_lines[i], int(_p[0]), int(_p[1]), int(_prev_point[0]), int(_prev_point[1]))

            # adjust for depth
            if int(_p[2]) < 0:
                self.tag_lower(self.d_points[i])
            else:
                self.tag_raise(self.d_points[i])

    def initialize_cube(self, rad=DOT_RAD):
        """
        This method initializes the Rubik's cube drawing--necessary to avoid null-referencing.
        """
        for i, point in enumerate(self.edge_points):
            _p = self.projected_point(point)

            # store drawing for deletion
            self.d_points.append(self.create_oval(as_dot(_p, rad=rad), fill=DEBUG_CLRS[i]))

            # account for depth
            if int(_p[2]) < 0:
                self.tag_lower(self.d_points[-1])
            else:
                self.tag_raise(self.d_points[-1])

            _p2 = self.projected_point(self.edge_points[i - 1])
            self.d_lines.append(self.create_line(int(_p[0]), int(_p[1]), int(_p2[0]), int(_p2[1]), fill=OUT_CLR))

    def projected_point(self, p):
        _p = rot_x(p, self.ytheta)
        _p = rot_y(_p, -self.xtheta)
        _p *= SIDE_WIDTH
        _p = add(_p, matrix([[int(CENT_POINT[0])], [int(CENT_POINT[1])], [0]]))
        return _p


def as_dot(p, rad=DOT_RAD):
    return int(p[0]) - rad, int(p[1]) - rad, int(p[0]) + rad, int(p[1]) + rad


def rot(p, theta, r):
    return dot(ROTATIONS[r](theta), p)


def rot_x(p, theta=90):
    return rot(p, theta, 'x')


def rot_y(p, theta=90):
    return rot(p, theta, 'y')


def rot_z(p, theta=90):
    return rot(p, theta, 'z')



