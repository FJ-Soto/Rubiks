from tkinter import *

from CONSTANTS import APP_BG, SIDE_WIDTH
from RubikCanvas import RubikCanvas

if __name__ == '__main__':
    root = Tk()
    root.config(padx=20, pady=20)
    root.resizable(False, False)

    rubik_canvas = RubikCanvas(master=root)
    rubik_canvas.grid(row=0, column=0, padx=20, pady=20)

    root.title("Rubik's Cube Solver")
    root.minsize(800, 600)
    root.tk_setPalette(background=APP_BG)
    root.mainloop()
