from tkinter import *

from CONSTANTS import APP_BG, APP_WDT, APP_HGT
from RubikCanvas import RubikCanvas
from ControlPanel import ControlPanel

from numpy import pi

if __name__ == '__main__':
    root = Tk()
    root.config(padx=20, pady=20)
    root.resizable(False, False)

    control_panel = ControlPanel(master=root)
    control_panel.grid(row=0, column=0, padx=20, pady=20, sticky=NE + W)

    rubik_canvas = RubikCanvas(master=root)
    rubik_canvas.grid(row=1, column=0, padx=20, pady=20, sticky=NSEW)

    def onChangeColorChange(e):
        rubik_canvas.show_clrs = control_panel.show_clrs.get()

    def onChangeOutlineChange(e):
        rubik_canvas.show_outline = control_panel.show_outline.get()

    def onChangePointsChange(e):
        rubik_canvas.show_points = control_panel.show_points.get()

    def xchange(e):
        rubik_canvas.ytheta = (control_panel.sc_xchange.get() / 180) * pi
        rubik_canvas.refresh()

    def ychange(e):
        rubik_canvas.xtheta = -(control_panel.sc_ychange.get() / 180) * pi
        rubik_canvas.refresh()

    def zchange(e):
        rubik_canvas.ztheta = (control_panel.sc_zchange.get() / 180) * pi
        rubik_canvas.refresh()

    def rubiksDrag(e):
        control_panel.ychange.set(rubik_canvas.ytheta * 180 / pi)
        control_panel.xchange.set(-rubik_canvas.xtheta * 180 / pi)
        control_panel.zchange.set(rubik_canvas.ztheta * 180 / pi)

    def refresh(e):
        rubik_canvas.reset()
        control_panel.ychange.set(rubik_canvas.ytheta * 180 / pi)
        control_panel.xchange.set(-rubik_canvas.xtheta * 180 / pi)
        control_panel.zchange.set(rubik_canvas.ztheta * 180 / pi)

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
