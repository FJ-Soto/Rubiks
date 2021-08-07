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
        # angle =
        # print(angle)
        # sign(self.curLastPos.y - e.y_root) *
        # sign(self.curLastPos.x - e.x_root) *
        self.ytheta += tan((self.curLastPos.y - e.y_root) / SIDE_WIDTH)
        self.xtheta += tan((self.curLastPos.x - e.x_root) / SIDE_WIDTH)
        self.curLastPos.x = e.x_root
        self.curLastPos.y = e.y_root

        self.draw_cube()
        print(self.edge_points[0], e.x_root, e.y_root)

    # TODO: Investigate a possible fix for the perspective skew.
    def draw_cube(self):
        for i, point in enumerate(self.edge_points):
            _p = self.projected_point(point)

            # move instead of redraw to improve performance and memory usage
            self.moveto(self.d_points[i], int(_p[0]), int(_p[1]))

    def initialize_cube(self):
        for i, point in enumerate(self.edge_points):
            _p = self.projected_point(point)
            # store drawing for deletion
            self.d_points.append(self.draw_point(_p, color=DEBUG_CLRS[i], rad=5))

            # account for depth
            if int(_p[2]) < 0:
                self.tag_lower(self.d_points[-1])
            else:
                self.tag_raise(self.d_points[-1])

            self.d_lines.append(self.draw_line(self.projected_point(self.edge_points[i - 1]), _p))

    def projected_point(self, p):
        _p = rot_x(p, self.ytheta)
        _p = rot_y(_p, -self.xtheta)
        _p *= SIDE_WIDTH
        _p = add(_p, matrix([[int(CENT_POINT[0])], [int(CENT_POINT[1])], [0]]))
        return _p

    def draw_segment(self, p1, p2, rad=DOT_RAD):
        """
        This method draws a line segment from one point to the other.

        :param p1: point one
        :param p2: point two
        :param rad: radius for the segment
        """
        return self.draw_point(p1, rad=rad), self.draw_point(p2, rad=rad), self.draw_line(p1, p2)

    def draw_point(self, p, rad=DOT_RAD, color=OUT_CLR):
        """
        This method draws a point.

        :param p: point to draw
        :param rad: radius of the circle
        :param color: color of the dot

        :return: reference to the drawn point
        """
        return self.create_oval(as_dot(p, rad=rad), fill=color)

    def draw_line(self, p1, p2):
        """
        This method draws a line.

        :param p1: point one to start line
        :param p2: point two to end line

        :return: reference to the drawn line
        """
        return self.create_line(int(p1[0]), int(p1[1]), int(p2[0]), int(p2[1]), fill=OUT_CLR)


def as_dot(p, rad=3):
    return int(p[0]) - rad, int(p[1]) - rad, int(p[0]) + rad, int(p[1]) + rad


def rot(p, theta, r):
    return dot(ROTATIONS[r](theta), p)


def rot_x(p, theta=90):
    return rot(p, theta, 'x')


def rot_y(p, theta=90):
    return rot(p, theta, 'y')


def rot_z(p, theta=90):
    return rot(p, theta, 'z')



