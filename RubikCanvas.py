from tkinter import *

from numpy import matrix, tan, dot, add, sqrt, square

from CONSTANTS import OUT_CLR, RUBIKS_CANV_WIDTH, SIDE_WIDTH, CENT_POINT, DOT_RAD, ROTATIONS, DEBUG_CLRS
from CONSTANTS import T_CON, M_CON, D_CON, CUBE, OCTANTS
from Coordinate import Coordinate


class RubikCanvas(Canvas):
    def __init__(self, master=None, width=RUBIKS_CANV_WIDTH):
        super().__init__(master=master, width=width, height=width)
        self.config(highlightthickness=1, highlightbackground=OUT_CLR)

        self.xtheta = 0
        self.ytheta = 0
        self.ztheta = 0

        self.d_lines = []
        self.d_points = []
        self.last_pos = None

        self.bind("<Button-1>", self.set_xy)
        self.bind("<B1-Motion>", self.onDrag)

        self.initialize_cube()

    def set_xy(self, e):
        if self.last_pos is None:
            self.last_pos = Coordinate(x=e.x_root, y=e.y_root)
        else:
            self.last_pos.x = e.x_root
            self.last_pos.y = e.y_root

    def onDrag(self, e):
        foc_p = self.projected_point(CUBE[0], False)

        octant = OCTANTS[(sign_p(int(foc_p[0])), sign_p(int(foc_p[1])), sign_p(int(foc_p[2])))]

        d_x, d_y = -tan((self.last_pos.x - e.x_root) / SIDE_WIDTH), tan((self.last_pos.y - e.y_root) / SIDE_WIDTH)

        self.xtheta += d_x
        self.ytheta += d_y

        self.last_pos.x = e.x_root
        self.last_pos.y = e.y_root
        self.draw_cube()

    # TODO: Investigate a possible fix for the perspective skew.
    def draw_cube(self, rad=DOT_RAD):
        l_count = 0
        for i, point in enumerate(CUBE):
            # use a dictionary to determine how the lines should be connected
            # follow T -> M -> D to ensure that l_count is in sync to the order in which the lines where added
            if i in T_CON:
                _p1, _p2 = self.projected_point(CUBE[i]), self.projected_point(CUBE[T_CON[i]])
                self.coords(self.d_lines[l_count], int(_p1[0]), int(_p1[1]), int(_p2[0]), int(_p2[1]))
                l_count += 1

            if i in M_CON:
                _p1, _p2 = self.projected_point(CUBE[i]), self.projected_point(CUBE[M_CON[i]])
                self.coords(self.d_lines[l_count], int(_p1[0]), int(_p1[1]), int(_p2[0]), int(_p2[1]))
                l_count += 1

            if i in D_CON:
                _p1, _p2 = self.projected_point(CUBE[i]), self.projected_point(CUBE[D_CON[i]])
                self.coords(self.d_lines[l_count], int(_p1[0]), int(_p1[1]), int(_p2[0]), int(_p2[1]))
                l_count += 1

            _p = self.projected_point(point)

            # move instead of redraw to improve performance and memory usage
            self.coords(self.d_points[i], as_dot(_p))

            # adjust for depth
            if int(_p[2]) < 0:
                self.tag_lower(self.d_points[i])
            else:
                self.tag_raise(self.d_points[i])

    def initialize_cube(self, rad=DOT_RAD):
        """
        This method initializes the Rubik's cube drawing--necessary to avoid null-referencing.
        """
        for i, point in enumerate(CUBE):
            # connect lines
            if i in T_CON:
                _p1, _p2 = self.projected_point(CUBE[i]), self.projected_point(CUBE[T_CON[i]])
                self.d_lines.append(self.create_line(int(_p1[0]), int(_p1[1]), int(_p2[0]), int(_p2[1]), fill='RED'))

                if int(_p1[2]) > 0 or int(_p2[2]) > 0:
                    self.tag_raise(self.d_lines[-1])
                else:
                    self.tag_lower(self.d_lines[-1])

            if i in M_CON:
                _p1, _p2 = self.projected_point(CUBE[i]), self.projected_point(CUBE[M_CON[i]])
                self.d_lines.append(self.create_line(int(_p1[0]), int(_p1[1]), int(_p2[0]), int(_p2[1]), fill='RED'))

                if int(_p1[2]) > 0 or int(_p2[2]) > 0:
                    self.tag_raise(self.d_lines[-1])
                else:
                    self.tag_lower(self.d_lines[-1])

            if i in D_CON:
                _p1, _p2 = self.projected_point(CUBE[i]), self.projected_point(CUBE[D_CON[i]])
                self.d_lines.append(self.create_line(int(_p1[0]), int(_p1[1]), int(_p2[0]), int(_p2[1]), fill='RED'))

                if int(_p1[2]) > 0 or int(_p2[2]) > 0:
                    self.tag_raise(self.d_lines[-1])
                else:
                    self.tag_lower(self.d_lines[-1])

            _p = self.projected_point(point)

            # store drawing for deletion
            self.d_points.append(self.create_oval(as_dot(_p, rad=rad), fill=DEBUG_CLRS[i]))

            # account for depth
            if int(_p[2]) < 0:
                self.tag_lower(self.d_points[-1])
            else:
                self.tag_raise(self.d_points[-1])

    def projected_point(self, p, shift=True):
        _p = rot_x(p, self.ytheta)
        _p = rot_y(_p, self.xtheta)
        _p *= SIDE_WIDTH
        return add(_p, matrix([[int(CENT_POINT[0])], [int(CENT_POINT[1])], [0]])) if shift else _p


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


def sign_p(v):
    return -1 if v < 0 else 1



