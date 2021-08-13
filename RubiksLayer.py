from tkinter import *
from itertools import chain

from Coordinate import Coordinate
from CONSTANTS import SIDE_WIDTH, T_CON, M_CON, D_CON
from CONSTANTS import CUBE, CUBE_FACES, CUBE_CLRS, DEBUG_CLRS, OCTANTS, CENT_POINT

from UtilityFunctions import adjust_theta, sign_p, as_dot, rot_x, rot_y, rot_z
from numpy import tan, reshape, add, matrix


class RubikLayer:
    def __init__(self, master: Canvas, y_offset: float = 0):
        self.master = master
        self._xtheta = 0
        self._ytheta = 0
        self._ztheta = 0
        self.CUBE = CUBE(3, 1, 3, y_offset=y_offset)

        self.show_clrs = True
        self.show_outline = False
        self.show_points = False

        self.d_lines = []
        self.d_points = []
        self.d_faces = []
        self.last_pos = Coordinate(0, 0)
        self.center = CENT_POINT

        # self.d_c = self.master.create_oval(as_dot(self.center), fill='CYAN')
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

    @property
    def ztheta(self):
        return self._ztheta

    @ztheta.setter
    def ztheta(self, v):
        self._ztheta = adjust_theta(v)

    def set_xy(self, e):
        """
        This initializes or refreshes the last click.

        :param e: event
        """
        self.last_pos.x = e.x_root
        self.last_pos.y = e.y_root

    def set_thetas(self, x, y):
        self.xtheta = x
        self.ytheta = y

    def on_drag(self, e):
        """
        This is the command that triggers when dragging on the canvas. This makes sure that
        the change in axis calls for transformation of the cube.
        """
        d_x, d_y = tan((self.last_pos.x - e.x_root) / SIDE_WIDTH), tan((self.last_pos.y - e.y_root) / SIDE_WIDTH)

        self.xtheta += d_x
        self.ytheta += d_y

        self.last_pos.x = e.x_root
        self.last_pos.y = e.y_root
        self.draw_cube()

    def get_octant(self, p):
        fp = self.projected_point(p, shift=False)
        return OCTANTS[sign_p(fp[0]), sign_p(fp[1]), sign_p(fp[2])]

    # TODO: Investigate a possible fix for the perspective skew.
    def draw_cube(self):
        """
        This adjust the cube model--a 'redraw' without the redrawing.
        This adjusts the individual coordinates to reduce CPU and RAM usage.
        """
        l_count = 0
        for i, point in enumerate(self.CUBE):
            _p = self.projected_point(point)
            if self.show_points:
                self.master.itemconfigure(self.d_points[i], state=NORMAL)
                self.master.coords(self.d_points[i], as_dot(_p))
                # adjust for depth
                if self.is_behind(_p[2]):
                    self.master.tag_lower(self.d_points[i])
                else:
                    self.master.tag_raise(self.d_points[i])
            else:
                self.master.itemconfigure(self.d_points[i], state=HIDDEN)

            # use a dictionary to determine how the lines should be connected
            # follow T -> M -> D to ensure that l_count is in sync to the order in which the lines where added
            if i in T_CON:
                if self.show_outline:
                    self.master.itemconfigure(self.d_lines[l_count], state=NORMAL)
                    _p2 = self.projected_point(self.CUBE[T_CON[i]])
                    self.master.coords(self.d_lines[l_count], int(_p[0]), int(_p[1]), int(_p2[0]), int(_p2[1]))
                else:
                    self.master.itemconfigure(self.d_lines[l_count], state=HIDDEN)
                l_count += 1

            if i in M_CON:
                if self.show_outline:
                    self.master.itemconfigure(self.d_lines[l_count], state=NORMAL)
                    _p2 = self.projected_point(self.CUBE[M_CON[i]])
                    self.master.coords(self.d_lines[l_count], int(_p[0]), int(_p[1]), int(_p2[0]), int(_p2[1]))
                else:
                    self.master.itemconfigure(self.d_lines[l_count], state=HIDDEN)
                l_count += 1

            if i in D_CON:
                if self.show_outline:
                    self.master.itemconfigure(self.d_lines[l_count], state=NORMAL)
                    _p2 = self.projected_point(self.CUBE[D_CON[i]])
                    self.master.coords(self.d_lines[l_count], int(_p[0]), int(_p[1]), int(_p2[0]), int(_p2[1]))
                else:
                    self.master.itemconfigure(self.d_lines[l_count], state=HIDDEN)
                l_count += 1

        if self.show_clrs:
            # determine the peak point
            peak = max(map(lambda x: self.projected_point(x), self.CUBE), key=lambda x: x[2])

            for i, face in enumerate(CUBE_FACES):
                # compute projected face points
                ps = list(map(lambda x: self.projected_point(x), list(self.CUBE[z] for z in face)))

                # determine if any of the projected points connect with the peak and show or hide
                if any((peak == p).all() for p in ps):
                    self.master.coords(self.d_faces[i],
                                       tuple(chain.from_iterable(map(lambda x: (int(x[0]), int(x[1])), ps))))
                    self.master.itemconfigure(self.d_faces[i], state=NORMAL)
                else:
                    self.master.itemconfigure(self.d_faces[i], state=HIDDEN)
        else:
            for face in self.d_faces:
                self.master.itemconfigure(face, state=HIDDEN)

    def initialize_cube(self):
        """
        This method initializes the Rubik's cube drawing--necessary to avoid null-referencing.
        """
        for i, point in enumerate(self.CUBE):
            # determine projected point location
            _p = self.projected_point(point)

            # draw and store the dot
            self.d_points.append(self.master.create_oval(as_dot(_p), fill=DEBUG_CLRS[i]))

            # connect lines + adjust initial depth
            if i in T_CON:
                _p2 = self.projected_point(self.CUBE[T_CON[i]])
                self.d_lines.append(self.master.create_line(int(_p[0]), int(_p[1]), int(_p2[0]), int(_p2[1]), fill='RED'))
                self.adj_line(_p, _p2)

            if i in M_CON:
                _p2 = self.projected_point(self.CUBE[M_CON[i]])
                self.d_lines.append(self.master.create_line(int(_p[0]), int(_p[1]), int(_p2[0]), int(_p2[1]), fill='RED'))
                self.adj_line(_p, _p2)

            if i in D_CON:
                _p2 = self.projected_point(self.CUBE[D_CON[i]])
                self.d_lines.append(self.master.create_line(int(_p[0]), int(_p[1]), int(_p2[0]), int(_p2[1]), fill='RED'))
                self.adj_line(_p, _p2)

            # adjust for depth
            if self.is_behind(_p[2]):
                self.master.tag_lower(self.d_points[i])
            else:
                self.master.tag_raise(self.d_points[i])

        peak = max(map(lambda x: self.projected_point(x), self.CUBE), key=lambda x: x[2])

        for i, face in enumerate(CUBE_FACES):
            ps = list(map(lambda x: self.projected_point(x), list(self.CUBE[z] for z in face)))
            coords = tuple(chain.from_iterable(map(lambda x: (int(x[0]), int(x[1])), ps)))
            pol = self.master.create_polygon(coords, fill=CUBE_CLRS[i])
            self.d_faces.append(pol)

            if any((peak == p).all() for p in ps):
                self.master.itemconfigure(self.d_faces[-1], state=NORMAL)
            else:
                self.master.itemconfigure(self.d_faces[-1], state=HIDDEN)

    def adj_line(self, p1, p2):
        """
        This method considers two points. If either of the points is in the background,
        the line is sent to the background.

        :param matrix p1: a point
        :param matrix p2: another point
        """
        if self.is_behind(p1[2], p2[2]):
            self.master.tag_lower(self.d_lines[-1])
        else:
            self.master.tag_raise(self.d_lines[-1])

    def projected_point(self, p, shift=True):
        """
        This method takes a point and applies the appropriate rotations.

        :param matrix p: point to transform
        :param bool shift: whether to perform shift for canvas

        :return: projected point
        :rtype: matrix
        """
        _p = self.project(p)
        _p *= SIDE_WIDTH

        # print(self.project(reshape((1 / CANVAS_WDT) * self.center, (3, 1))))
        return add(_p, reshape(self.center, (3, 1))) if shift else _p

    def project(self, p):
        _p = rot_x(p, self.ytheta)
        _p = rot_y(_p, -self.xtheta)
        _p = rot_z(_p, self.ztheta)
        return _p

    def is_behind(self, *args):
        """
        This returns true if any of the value sent over is negative.

        :param args: list of numbers

        :returns: boolean indicating whether any value is negative
        :rtype: bool
        """
        return any(x < self.center[2] for x in args)
