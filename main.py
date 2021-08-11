from tkinter import *

from CONSTANTS import APP_BG, APP_WDT, APP_HGT
from RubikCanvas import RubikCanvas
from ControlPanel import ControlPanel

if __name__ == '__main__':
    root = Tk()
    root.config(padx=20, pady=20)
    root.resizable(False, False)

    rubik_canvas = RubikCanvas(master=root)
    rubik_canvas.grid(row=0, column=0, padx=20, pady=20, sticky=EW)

    control_panel = ControlPanel(master=root)
    control_panel.grid(row=0, column=1, padx=20, pady=20, sticky=N+EW)

    root.title("Rubik's Cube Solver")
    root.minsize(APP_HGT, APP_WDT)
    root.tk_setPalette(background=APP_BG)
    root.mainloop()
