from itertools import chain
from tkinter import *

from numpy import reshape, add, matrix

from CONSTANTS import CUBE_FACES, DEBUG_CLRS, CENT_POINT
from CONSTANTS import SIDE_WIDTH, T_CON, M_CON, D_CON
from Coordinate import Coordinate
from UtilityFunctions import as_dot, gen_cube, project


class RubikLayer:
    def __init__(self, master, x_rad, y_rad, z_rad, show_faces, show_outline, show_points,
                 y_offset=0, x_offset=0, exclude_face=None):
        """
        This initializes an instance of a drawable Rubik layer.

        :param master: the canvas for which to draw cube on.
        :param float y_offset: shift center point by y-offset
        :param float x_offset: shift center point by x-offset
        :param set exclude_face: list of faces not to color
        """
        self.master = master
        self.CUBE = gen_cube(3, 1, 3, y_offset=y_offset, x_offset=x_offset)
        self._CUBE = gen_cube(3, 1, 3, y_offset=y_offset, x_offset=x_offset)
        self.x_offset = x_offset
        self.y_offset = y_offset

        self.show_faces = show_faces
        self.show_outline = show_outline
        self.show_points = show_points
        self._faces_showing = not self.show_faces
        self._outline_showing = not self.show_outline
        self._points_showing = not self.show_points

        self.d_lines = []
        self.d_points = []
        self.d_faces = []
        self.last_pos = Coordinate(0, 0)
        self.center = CENT_POINT

        self._faces = set(CUBE_FACES.keys()) - exclude_face

        self.initialize_cube(x_rad, y_rad, z_rad)

    def redraw(self):
        """
            This adjust the cube model--a 'redraw' without the redrawing.
            This adjusts the individual coordinates to reduce CPU and RAM usage.

            Note: in effort to reduce time complexity, multiple parts of the cube
            are draw/adjusted within a single for-loop. Ideally, this could be
            written in segments.
            """
        l_count = 0
        for i, point in enumerate(self.CUBE):
            _p = self.shift_to_center(point * SIDE_WIDTH)

            if self.show_points:
                self.master.itemconfigure(self.d_points[i], state=NORMAL)
                self.master.coords(self.d_points[i], as_dot(_p))
                # adjust for depth
                if self.is_behind(int(_p[2])):
                    self.master.tag_lower(self.d_points[i])
                else:
                    self.master.tag_raise(self.d_points[i])
                self._points_showing = True
            elif self._points_showing:
                self._points_showing = False
                for p in self.d_points:
                    self.master.itemconfigure(p, state=HIDDEN)

            # use a dictionary to determine how the lines should be connected
            # follow T -> M -> D to ensure that l_count is in sync to the order in which the lines where added
            if self.show_outline:
                if i in T_CON:
                    self.master.itemconfigure(self.d_lines[l_count], state=NORMAL)
                    _p2 = self.shift_to_center(self.CUBE[T_CON[i]] * SIDE_WIDTH)
                    self.master.coords(self.d_lines[l_count], int(_p[0]), int(_p[1]), int(_p2[0]), int(_p2[1]))
                    l_count += 1

                if i in M_CON:
                    self.master.itemconfigure(self.d_lines[l_count], state=NORMAL)
                    _p2 = self.shift_to_center(self.CUBE[M_CON[i]] * SIDE_WIDTH)
                    self.master.coords(self.d_lines[l_count], int(_p[0]), int(_p[1]), int(_p2[0]), int(_p2[1]))
                    l_count += 1

                if i in D_CON:
                    self.master.itemconfigure(self.d_lines[l_count], state=NORMAL)
                    _p2 = self.shift_to_center(self.CUBE[D_CON[i]] * SIDE_WIDTH)
                    self.master.coords(self.d_lines[l_count], int(_p[0]), int(_p[1]), int(_p2[0]), int(_p2[1]))
                    l_count += 1
                    self._outline_showing = True
            elif self._outline_showing:
                self._outline_showing = False
                for line in self.d_lines:
                    self.master.itemconfigure(line, state=HIDDEN)

        if self.show_faces:
            # determine the peak point
            proj_ps = list(map(lambda x: self.shift_to_center(x * SIDE_WIDTH), self.CUBE))
            peak = max(proj_ps, key=lambda x: x[2])

            for i, face in enumerate(self._faces):
                ps = list(proj_ps[p] for p in CUBE_FACES[face])
                if any((peak == p).all() for p in ps):
                    self.master.coords(self.d_faces[i],
                                       tuple(chain.from_iterable(map(lambda x: (int(x[0]), int(x[1])), ps))))
                    self.master.itemconfigure(self.d_faces[i], state=NORMAL, fill=self.master.color_scheme[face])
                else:
                    self.master.itemconfigure(self.d_faces[i], state=HIDDEN)
                self._faces_showing = True
        elif self._faces_showing:
            self._faces_showing = False
            for face in self.d_faces:
                self.master.itemconfigure(face, state=HIDDEN)

    # TODO: Investigate a possible fix for the perspective skew.
    def move(self, x_rad, y_rad, z_rad):
        """
        This adjust the cube model--a 'redraw' without the redrawing.
        This adjusts the individual coordinates to reduce CPU and RAM usage.

        Note: in effort to reduce time complexity, multiple parts of the cube
        are draw/adjusted within a single for-loop. Ideally, this could be
        written in segments.
        """
        l_count = 0
        for i, point in enumerate(self.CUBE):
            _p = self.projected_point(point, x_rad, y_rad, z_rad)

            if self.show_points:
                self.master.itemconfigure(self.d_points[i], state=NORMAL)
                self.master.coords(self.d_points[i], as_dot(_p))
                # adjust for depth
                if self.is_behind(int(_p[2])):
                    self.master.tag_lower(self.d_points[i])
                else:
                    self.master.tag_raise(self.d_points[i])
                self._points_showing = True
            elif self._points_showing:
                self._points_showing = False
                for p in self.d_points:
                    self.master.itemconfigure(p, state=HIDDEN)

            # use a dictionary to determine how the lines should be connected
            # follow T -> M -> D to ensure that l_count is in sync to the order in which the lines where added
            if self.show_outline:
                if i in T_CON:
                    self.master.itemconfigure(self.d_lines[l_count], state=NORMAL)
                    _p2 = self.projected_point(self.CUBE[T_CON[i]], x_rad, y_rad, z_rad)
                    self.master.coords(self.d_lines[l_count], int(_p[0]), int(_p[1]), int(_p2[0]), int(_p2[1]))
                    l_count += 1

                if i in M_CON:
                    self.master.itemconfigure(self.d_lines[l_count], state=NORMAL)
                    _p2 = self.projected_point(self.CUBE[M_CON[i]], x_rad, y_rad, z_rad)
                    self.master.coords(self.d_lines[l_count], int(_p[0]), int(_p[1]), int(_p2[0]), int(_p2[1]))
                    l_count += 1

                if i in D_CON:
                    self.master.itemconfigure(self.d_lines[l_count], state=NORMAL)
                    _p2 = self.projected_point(self.CUBE[D_CON[i]], x_rad, y_rad, z_rad)
                    self.master.coords(self.d_lines[l_count], int(_p[0]), int(_p[1]), int(_p2[0]), int(_p2[1]))
                    l_count += 1
                    self._outline_showing = True
            elif self._outline_showing:
                self._outline_showing = False
                for line in self.d_lines:
                    self.master.itemconfigure(line, state=HIDDEN)

        if self.show_faces:
            # determine the peak point
            proj_ps = list(map(lambda x: self.projected_point(x, x_rad, y_rad, z_rad), self.CUBE))
            peak = max(proj_ps, key=lambda x: x[2])

            for i, face in enumerate(self._faces):
                ps = list(proj_ps[p] for p in CUBE_FACES[face])
                if any((peak == p).all() for p in ps):
                    self.master.coords(self.d_faces[i],
                                       tuple(chain.from_iterable(map(lambda x: (int(x[0]), int(x[1])), ps))))
                    self.master.itemconfigure(self.d_faces[i], state=NORMAL, fill=self.master.color_scheme[face])
                else:
                    self.master.itemconfigure(self.d_faces[i], state=HIDDEN)
                self._faces_showing = True
        elif self._faces_showing:
            self._faces_showing = False
            for face in self.d_faces:
                self.master.itemconfigure(face, state=HIDDEN)

        self.CUBE = list(map(lambda point: project(point, x_rad, y_rad, z_rad), self.CUBE))

    def initialize_cube(self, x_rad, y_rad, z_rad):
        """
        This method initializes the Rubik's cube drawing--necessary to avoid null-referencing.
        """
        for i, point in enumerate(self.CUBE):
            # determine projected point location

            _p = self.projected_point(point, x_rad, y_rad, z_rad)

            # draw and store the dot
            self.d_points.append(self.master.create_oval(as_dot(_p), fill=DEBUG_CLRS[i]))

            # connect lines + adjust initial depth
            if i in T_CON:
                _p2 = self.projected_point(self.CUBE[T_CON[i]], x_rad, y_rad, z_rad)
                self.d_lines.append(self.master.create_line(int(_p[0]), int(_p[1]), int(_p2[0]), int(_p2[1]),
                                                            fill='RED'))
                self.adj_line(_p, _p2)

            if i in M_CON:
                _p2 = self.projected_point(self.CUBE[M_CON[i]], x_rad, y_rad, z_rad)
                self.d_lines.append(self.master.create_line(int(_p[0]), int(_p[1]), int(_p2[0]), int(_p2[1]),
                                                            fill='RED'))
                self.adj_line(_p, _p2)

            if i in D_CON:
                _p2 = self.projected_point(self.CUBE[D_CON[i]], x_rad, y_rad, z_rad)
                self.d_lines.append(self.master.create_line(int(_p[0]), int(_p[1]), int(_p2[0]), int(_p2[1]),
                                                            fill='RED'))
                self.adj_line(_p, _p2)

            # adjust for depth
            if self.is_behind(int(_p[2])):
                self.master.tag_lower(self.d_points[i])
            else:
                self.master.tag_raise(self.d_points[i])

        peak = max(map(lambda x: self.projected_point(x, x_rad, y_rad, z_rad), self.CUBE), key=lambda x: x[2])

        for face in self._faces:
            ps = list(map(lambda x: self.projected_point(x, x_rad, y_rad, z_rad),
                          list(self.CUBE[z] for z in CUBE_FACES[face])))
            coords = tuple(chain.from_iterable(map(lambda x: (int(x[0]), int(x[1])), ps)))
            pol = self.master.create_polygon(coords, fill=self.master.color_scheme[face])
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
        if self.is_behind(int(p1[2]), int(p2[2])):
            self.master.tag_lower(self.d_lines[-1])
        else:
            self.master.tag_raise(self.d_lines[-1])

    def projected_point(self, p, x_rad, y_rad, z_rad, shift=True):
        """
        This method takes a point and applies the appropriate rotations.

        :param matrix p: point to transform
        :param float x_rad: radian for x-axis
        :param float y_rad: radian for y-axis
        :param float z_rad: radian for z-axis
        :param bool shift: whether to perform shift for canvas

        :return: projected point
        :rtype: matrix
        """
        _p = project(p, x_rad, y_rad, z_rad)
        _p *= SIDE_WIDTH

        return self.shift_to_center(_p) if shift else _p

    def shift_to_center(self, p):
        return add(p, reshape(self.center, (3, 1)))

    def is_behind(self, *args):
        """
        This returns true if any of the value sent over is negative.

        :param args: list of numbers

        :returns: boolean indicating whether any value is negative
        :rtype: bool
        """
        return any(x < self.center[2] for x in args)

    def reset(self):
        self.CUBE = self._CUBE.copy()
