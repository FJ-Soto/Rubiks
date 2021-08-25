from tkinter import *

from numpy import tan, pi

from CONSTANTS import OUT_CLR, CANVAS_WDT, CANVAS_HGT, SIDE_WIDTH, CUBE_CLRS
from CONSTANTS import X_THETA, Y_THETA, Z_THETA
from CONSTANTS import SHOW_FACES, SHOW_OUTLINE, SHOW_POINTS
from Coordinate import Coordinate
from UtilityFunctions import adjust_theta

from RubiksLayer import RubikLayer


class RubikCanvas(Canvas):
    def __init__(self, master=None, height=CANVAS_HGT, width=CANVAS_WDT):
        super().__init__(master=master, width=width, height=height)
        self.config(highlightthickness=1, highlightbackground=OUT_CLR)
        self.color_scheme = CUBE_CLRS.copy()

        self._xtheta = X_THETA
        self._ytheta = Y_THETA
        self._ztheta = Z_THETA

        self.layers = [RubikLayer(self, x_rad=X_THETA, y_rad=Y_THETA, z_rad=Z_THETA,
                                  show_faces=SHOW_FACES, show_outline=SHOW_OUTLINE, show_points=SHOW_POINTS,
                                  y_offset=-1, exclude_face={'BOTTOM'}),
                       RubikLayer(self, x_rad=X_THETA, y_rad=Y_THETA, z_rad=Z_THETA,
                                  show_faces=SHOW_FACES, show_outline=SHOW_OUTLINE, show_points=SHOW_POINTS,
                                  exclude_face={'TOP', 'BOTTOM'}),
                       RubikLayer(self, x_rad=X_THETA, y_rad=Y_THETA, z_rad=Z_THETA,
                                  show_faces=SHOW_FACES, show_outline=SHOW_OUTLINE, show_points=SHOW_POINTS,
                                  y_offset=1, exclude_face={'TOP'})]

        self.last_pos = Coordinate()

        self.bind("<Button-1>", self.set_xy)
        self.bind("<B1-Motion>", self.on_drag)

        self.show_faces = True
        self.show_outline = False
        self.show_points = False

    @property
    def show_faces(self):
        return self._show_clrs

    @show_faces.setter
    def show_faces(self, v):
        self._show_clrs = v
        for layer in self.layers:
            layer.show_faces = v
        self.refresh()

    @property
    def show_outline(self):
        return self._show_outline

    @show_outline.setter
    def show_outline(self, v):
        self._show_outline = v
        for layer in self.layers:
            layer.show_outline = v
        self.refresh()

    @property
    def show_points(self):
        return self._show_points

    @show_points.setter
    def show_points(self, v):
        self._show_points = v
        for layer in self.layers:
            layer.show_points = v
        self.refresh()

    @property
    def xtheta(self):
        return self._xtheta

    @xtheta.setter
    def xtheta(self, v):
        self._xtheta = v

    @property
    def ytheta(self):
        return self._ytheta

    @ytheta.setter
    def ytheta(self, v):
        self._ytheta = v

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

    def reset(self):
        self.xtheta = X_THETA
        self.ytheta = Y_THETA
        self.ztheta = Z_THETA
        for layer in self.layers:
            layer.reset()
        self.move_cube()

    def move_cube(self):
        for layer in self.layers:
            layer.move(self.xtheta, self.ytheta, self.ztheta)

    def refresh(self):
        for layer in self.layers:
            layer.redraw()

    def rotate(self, r):
        if r == 'U':
            self.layers[0].move(self.xtheta + 1 / 2 * pi, self.ytheta, self.ztheta)
        self.refresh()

    def on_drag(self, e):
        """
        This is the command that triggers when dragging on the canvas. This makes sure that
        the change in axis calls for transformation of the cube.
        """
        if self.show_faces or self.show_outline or self.show_points:
            d_x = -tan((self.last_pos.x - e.x_root) / (2 * SIDE_WIDTH))
            d_y = tan((self.last_pos.y - e.y_root) / (2 * SIDE_WIDTH))

            self.xtheta = d_x / 2.5
            self.ytheta = d_y / 2.5

            self.last_pos.x = e.x_root
            self.last_pos.y = e.y_root

            self.move_cube()
