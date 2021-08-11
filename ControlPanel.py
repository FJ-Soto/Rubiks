from tkinter import *
from CONSTANTS import OUT_CLR, CTRL_PNL_HGT, CTRL_PNL_WDT


class ControlPanel(Frame):
    def __init__(self, master=None, width=CTRL_PNL_WDT, height=CTRL_PNL_HGT):
        super(ControlPanel, self).__init__(master=master, width=width, height=height)
        self.config(highlightthickness=1, highlightbackground=OUT_CLR)
