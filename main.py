from tkinter import *

from CONSTANTS import APP_BG, APP_WDT, APP_HGT
from RubikCanvas import RubikCanvas
from ControlPanel import ControlPanel
from UtilityFunctions import to_rad, to_deg


from numpy import pi

if __name__ == '__main__':
    root = Tk()
    root.config(padx=20, pady=20)
    root.resizable(False, False)

    control_panel = ControlPanel(master=root)
    control_panel.grid(row=0, column=0, padx=20, pady=20, sticky=NE + W)

    rubik_canvas = RubikCanvas(master=root)
    rubik_canvas.grid(row=0, column=1, padx=20, pady=20, sticky=NSEW)

    def onChangeColorChange(e):
        """
        This method toggles the canvas cube color displaying.

        :param e: event

        :rtype: None
        """
        rubik_canvas.show_clrs = control_panel.show_clrs.get()

    def onChangeOutlineChange(e):
        """
        This method toggles the canvas cube outline displaying.

        :param e: event

        :rtype: None
        """
        rubik_canvas.show_outline = control_panel.show_outline.get()

    def onChangePointsChange(e):
        """
        This method toggles the canvas cube points displaying.

        :param e: event

        :rtype: None
        """
        rubik_canvas.show_points = control_panel.show_points.get()

    def xchange(e):
        """
        This method sets the cube x-theta when slider is changed

        :param e: event

        :rtype: None
        """
        rubik_canvas.ytheta = (control_panel.sc_xchange.get() / 180) * pi
        rubik_canvas.refresh()

    def ychange(e):
        """
        This method sets the cube y-theta when slider is changed

        :param e: event

        :rtype: None
        """
        rubik_canvas.xtheta = to_rad(control_panel.sc_ychange.get())
        rubik_canvas.refresh()

    def zchange(e):
        """
        This method sets the cube z-theta when slider is changed

        :param e: event

        :rtype: None
        """
        rubik_canvas.ztheta = to_rad(control_panel.sc_zchange.get())
        rubik_canvas.refresh()

    def rubiksDrag(e):
        """
        This method sets the control panels theta values when Rubik canvas is dragged.

        :param e: event

        :rtype: None
        """
        control_panel.ychange.set(to_deg(rubik_canvas.ytheta))
        control_panel.xchange.set(to_deg(rubik_canvas.xtheta))
        control_panel.zchange.set(to_deg(rubik_canvas.ztheta))

    def refresh(e):
        """
        This method resets the perspective of the cube to the default.

        :param e: event

        :rtype: None
        """
        rubik_canvas.reset()
        control_panel.ychange.set(to_deg(rubik_canvas.ytheta))
        control_panel.xchange.set(to_deg(rubik_canvas.xtheta))
        control_panel.zchange.set(to_deg(rubik_canvas.ztheta))

    rubik_canvas.refresh()

    rubik_canvas.bind("<<drag>>", rubiksDrag)

    control_panel.bind("<<Show Color Change>>", onChangeColorChange)
    control_panel.bind("<<Show Outline Change>>", onChangeOutlineChange)
    control_panel.bind("<<Show Points Change>>", onChangePointsChange)
    control_panel.bind("<<x-change>>", xchange)
    control_panel.bind("<<y-change>>", ychange)
    control_panel.bind("<<z-change>>", zchange)
    control_panel.bind("<<reset canvas>>", refresh)

    root.title("Rubik's Cube Solver")
    root.minsize(APP_WDT, APP_HGT)
    root.tk_setPalette(background=APP_BG)

    root.mainloop()
