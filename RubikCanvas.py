from tkinter import *

from numpy import matrix, tan, dot, add, pi, sign

from CONSTANTS import OUT_CLR, CANVAS_WIDTH, SIDE_WIDTH, CENT_POINT, DOT_RAD, DEBUG_CLRS, OCTANTS
from Transformations import ROTATIONS
from Forms import Cube, TriangularPrism
from Coordinate import Coordinate


class RubikCanvas(Canvas):
    def __init__(self, master=None, width=CANVAS_WIDTH):
        super().__init__(master=master, width=width, height=width)
        self.config(highlightthickness=1, highlightbackground=OUT_CLR)

        self._xtheta = 0
        self._ytheta = 0
        self.f = Cube(1, 1, 1)

        self.d_lines = []
        self.d_points = []
        self.last_pos = Coordinate(0, 0)

        self.bind("<Button-1>", self.set_xy)
        self.bind("<B1-Motion>", self.on_drag)

        self.initialize_cube()

    @property
    def xtheta(self):
        return self._xtheta

    @xtheta.setter
    def xtheta(self, v):
        self._xtheta = adjust_theta(v)

    @property
    def ytheta(self):
        return self._ytheta

    @ytheta.setter
    def ytheta(self, v):
        self._ytheta = adjust_theta(v)

    def set_xy(self, e):
        """
        This initializes or refreshes the last click.

        :param e: event
        """
        self.last_pos.x = e.x_root
        self.last_pos.y = e.y_root

    def on_drag(self, e):
        """
        This is the command that triggers when dragging on the canvas. This makes sure that
        the change in axis calls for transformation of the cube.
        """
        d_x, d_y = tan((self.last_pos.x - e.x_root) / SIDE_WIDTH), tan((self.last_pos.y - e.y_root) / SIDE_WIDTH)

        self.xtheta += d_x
        self.ytheta += d_y

        fp = self.projected_point(self.f.points[0], shift=False)
        print(fp)
        print(OCTANTS[(sign_p(fp[0]), sign_p(fp[1]), sign_p(fp[2]))])

        self.last_pos.x = e.x_root
        self.last_pos.y = e.y_root
        self.draw_cube()

    # TODO: Investigate a possible fix for the perspective skew.
    def draw_cube(self):
        """
        This adjust the cube model--a 'redraw' without the redrawing.
        This adjusts the individual coordinates to reduce CPU and RAM usage.
        """
        l_count = 0
        for i, point in enumerate(self.f.points):
            _p = self.projected_point(point)
            self.coords(self.d_points[i], as_dot(_p))

            # use a dictionary to determine how the lines should be connected
            # follow T -> M -> D to ensure that l_count is in sync to the order in which the lines where added
            if i in self.f.T_CON:
                _p2 = self.projected_point(self.f.points[self.f.T_CON[i]])
                self.coords(self.d_lines[l_count], int(_p[0]), int(_p[1]), int(_p2[0]), int(_p2[1]))
                l_count += 1

            if i in self.f.M_CON:
                _p2 = self.projected_point(self.f.points[self.f.M_CON[i]])
                self.coords(self.d_lines[l_count], int(_p[0]), int(_p[1]), int(_p2[0]), int(_p2[1]))
                l_count += 1

            if i in self.f.D_CON:
                _p2 = self.projected_point(self.f.points[self.f.D_CON[i]])
                self.coords(self.d_lines[l_count], int(_p[0]), int(_p[1]), int(_p2[0]), int(_p2[1]))
                l_count += 1

            # adjust for depth
            if is_behind(_p[2]):
                self.tag_lower(self.d_points[i])
            else:
                self.tag_raise(self.d_points[i])

    def initialize_cube(self):
        """
        This method initializes the Rubik's cube drawing--necessary to avoid null-referencing.
        """
        for i, point in enumerate(self.f.points):
            # determine projected point location
            _p = self.projected_point(point)

            # draw and store the dot
            self.d_points.append(self.create_oval(as_dot(_p), fill=DEBUG_CLRS[i]))

            # connect lines + adjust initial depth
            if i in self.f.T_CON:
                _p2 = self.projected_point(self.f.points[self.f.T_CON[i]])
                self.d_lines.append(self.create_line(int(_p[0]), int(_p[1]), int(_p2[0]), int(_p2[1]), fill='RED'))
                self.adj_line(_p, _p2)

            if i in self.f.M_CON:
                _p2 = self.projected_point(self.f.points[self.f.M_CON[i]])
                self.d_lines.append(self.create_line(int(_p[0]), int(_p[1]), int(_p2[0]), int(_p2[1]), fill='RED'))
                self.adj_line(_p, _p2)

            if i in self.f.D_CON:
                _p2 = self.projected_point(self.f.points[self.f.D_CON[i]])
                self.d_lines.append(self.create_line(int(_p[0]), int(_p[1]), int(_p2[0]), int(_p2[1]), fill='RED'))
                self.adj_line(_p, _p2)

            # adjust for depth
            if is_behind(_p[2]):
                self.tag_lower(self.d_points[i])
            else:
                self.tag_raise(self.d_points[i])

    def adj_line(self, p1, p2):
        """
        This method considers two points. If either of the points is in the background,
        the line is sent to the background.

        :param matrix p1: a point
        :param matrix p2: another point
        """
        if is_behind(p1[2], p2[2]):
            self.tag_lower(self.d_lines[-1])
        else:
            self.tag_raise(self.d_lines[-1])

    def projected_point(self, p, shift=True):
        """
        This method takes a point and applies the appropriate rotations.

        :param matrix p: point to transform
        :param bool shift: whether to perform shift for canvas

        :return: projected point
        :rtype: matrix
        """
        _p = rot_x(p, self.ytheta)
        _p = rot_y(_p, -self.xtheta)
        _p *= SIDE_WIDTH
        return add(_p, matrix([[int(CENT_POINT[0])], [int(CENT_POINT[1])], [0]])) if shift else _p


def is_behind(*args):
    """
    This returns true if any of the value sent over is negative.

    :param args: list of numbers

    :returns: boolean indicating whether any value is negative
    :rtype: bool
    """
    return any(x < 0 for x in args)


def as_dot(p, rad=DOT_RAD):
    """
    This returns the diagonal coordinates necessary
    to compose the circle of a given radius.

    :param matrix p: point to convert
    :param int rad: radius for the circle

    :return: a list of edges
    :rtype: tuple
    """
    return int(p[0]) - rad, int(p[1]) - rad, int(p[0]) + rad, int(p[1]) + rad


def rot(p, theta, rotation):
    """
    This method rotates a given point by the given angle and
    in the direction specified.

    :param matrix p: point to rotate
    :param int theta: angle to rotate by
    :param str rotation: x, y, or z

    :return: a matrix representing the points new position
    :rtype: matrix
    """
    return dot(ROTATIONS[rotation](theta), p)


def rot_x(p, theta=90):
    """
    This rotates a point in the x-axis by theta.

    :param matrix p: point to rotate
    :param int theta: angle to rotate by

    :return: a matrix representing the points new position
    :rtype: matrix
    """
    return rot(p, theta, 'x')


def rot_y(p: matrix, theta=90):
    """
    This rotates a point in the y-axis by theta.

    :param matrix p: point to rotate
    :param int theta: angle to rotate by

    :return: a matrix representing the points new position
    :rtype: matrix
    """
    return rot(p, theta, 'y')


def rot_z(p, theta=90):
    """
    This rotates a point in the z-axis by theta.

    :param matrix p: point to rotate
    :param int theta: angle to rotate by

    :return: a matrix representing the points new position
    :rtype: matrix
    """
    return rot(p, theta, 'z')


def sign_p(v):
    """
    This is a positive-biased version of a sign function.
    This returns -1 if v < 0 else 1.

    :param int v: number to compare on
    :rtype: int
    """
    return -1 if v < 0 else 1


def adjust_theta(v):
    if -2 * pi <= v <= 2 * pi:
        return v
    elif 2 * pi < v:
        return -2 * pi
    else:
        return 2 * pi
