from tkinter import *

from CONSTANTS import APP_BG, CUBE_CLRS, RESIZE_WDT, RESIZE_HGT, MIN_WDT, MIN_HGT
from RubikCanvas import RubikCanvas
from ControlPanel import ControlPanel
from UtilityFunctions import to_rad, to_deg


from numpy import pi

if __name__ == '__main__':
    root = Tk()
    root.title("Rubik's Cube Solver")
    root.config(padx=20, pady=20)
    root.tk_setPalette(background=APP_BG)
    root.minsize(MIN_WDT, MIN_HGT)
    root.resizable(RESIZE_WDT, RESIZE_HGT)

    control_panel = ControlPanel(master=root)
    control_panel.grid(row=0, column=0, padx=20, pady=20, sticky=NE + W)

    rubik_canvas = RubikCanvas(master=root)
    rubik_canvas.grid(row=0, column=1, padx=20, pady=20, sticky=NSEW)

    control_panel.set_colors(CUBE_CLRS)

    def onChangeColorChange(e):
        """
        This method toggles the canvas cube color displaying.

        :param e: event

        :rtype: None
        """
        rubik_canvas.show_faces = control_panel.show_clrs.get()

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

    def adjColorScheme(e):
        rubik_canvas.color_scheme = control_panel.get_color_scheme()
        rubik_canvas.refresh()

    def reset_color_scheme(e):
        control_panel.set_colors(CUBE_CLRS)
        adjColorScheme(None)

    def rotate_u(e):
        rotate_cube('U')

    def rotate_cube(r):
        rubik_canvas.rotate(r)

    rubik_canvas.move_cube()

    control_panel.bind("<<showColorChange>>", onChangeColorChange)
    control_panel.bind("<<showOutlineChange>>", onChangeOutlineChange)
    control_panel.bind("<<showPointsChange>>", onChangePointsChange)
    control_panel.bind("<<colorSchemeChange>>", adjColorScheme)
    control_panel.bind("<<resetColorScheme>>", reset_color_scheme)
    control_panel.bind("<<rotate_u>>", rotate_u)

    root.mainloop()
