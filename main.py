from tkinter import *

from CONSTANTS import APP_BG, APP_WDT, APP_HGT
from RubikCanvas import RubikCanvas
from ControlPanel import ControlPanel

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

    rubik_canvas.refresh()

    control_panel.bind("<<Show Color Change>>", onChangeColorChange)
    control_panel.bind("<<Show Outline Change>>", onChangeOutlineChange)
    control_panel.bind("<<Show Points Change>>", onChangePointsChange)

    root.title("Rubik's Cube Solver")
    root.minsize(APP_WDT, APP_HGT)
    root.tk_setPalette(background=APP_BG)

    root.mainloop()
