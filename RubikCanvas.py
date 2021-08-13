from tkinter import *

from numpy import tan

from CONSTANTS import OUT_CLR, CANVAS_WDT, CANVAS_HGT, CENT_POINT, SIDE_WIDTH, CUBE_CLRS
from CONSTANTS import X_THETA, Y_THETA, Z_THETA
from Coordinate import Coordinate
from UtilityFunctions import adjust_theta

from RubiksLayer import RubikLayer


class RubikCanvas(Canvas):
    def __init__(self, master=None, height=CANVAS_HGT, width=CANVAS_WDT):
        super().__init__(master=master, width=width, height=height)
        self.config(highlightthickness=1, highlightbackground=OUT_CLR)
        self.color_scheme = CUBE_CLRS.copy()

        self.layers = [RubikLayer(self, -1, exclude_face={'BOTTOM'}),
                       RubikLayer(self, exclude_face={'TOP', 'BOTTOM'}),
                       RubikLayer(self, 1, exclude_face={'TOP'})]

        self.xtheta = X_THETA
        self.ytheta = Y_THETA
        self.ztheta = Z_THETA

        self.d_lines = []
        self.d_points = []
        self.d_faces = []
        self.last_pos = Coordinate()
        self.center = CENT_POINT

        self.bind("<Button-1>", self.set_xy)
        self.bind("<B1-Motion>", self.on_drag)

        self.show_clrs = True
        self.show_outline = False
        self.show_points = False

    @property
    def show_clrs(self):
        return self._show_clrs

    @show_clrs.setter
    def show_clrs(self, v):
        self._show_clrs = v
        for layer in self.layers:
            layer.show_clrs = v
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
        self._xtheta = adjust_theta(v)
        for layer in self.layers:
            layer.xtheta = self._xtheta

    def reset(self):
        self.xtheta = X_THETA
        self.ytheta = Y_THETA
        self.ztheta = Z_THETA
        self.refresh()

    @property
    def ytheta(self):
        return self._ytheta

    @ytheta.setter
    def ytheta(self, v):
        self._ytheta = adjust_theta(v)
        for layer in self.layers:
            layer.ytheta = self._ytheta

    @property
    def ztheta(self):
        return self._ztheta

    @ztheta.setter
    def ztheta(self, v):
        self._ztheta = adjust_theta(v)
        for layer in self.layers:
            layer.ztheta = self._ztheta

    def set_xy(self, e):
        """
        This initializes or refreshes the last click.

        :param e: event
        """
        self.last_pos.x = e.x_root
        self.last_pos.y = e.y_root

    def refresh(self):
        for layer in self.layers:
            layer.draw_cube()

    def on_drag(self, e):
        """
        This is the command that triggers when dragging on the canvas. This makes sure that
        the change in axis calls for transformation of the cube.
        """
        d_x = tan((self.last_pos.x - e.x_root) / (2 * SIDE_WIDTH))
        d_y = tan((self.last_pos.y - e.y_root) / (2 * SIDE_WIDTH))

        self.xtheta += -d_x
        self.ytheta += d_y

        self.last_pos.x = e.x_root
        self.last_pos.y = e.y_root

        for layer in self.layers:
            layer.set_thetas(self.xtheta, self.ytheta)

        self.event_generate('<<drag>>')
        self.refresh()
