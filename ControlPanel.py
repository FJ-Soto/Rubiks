from tkinter import *

from CONSTANTS import OUT_CLR, CTRL_PNL_HGT, CTRL_PNL_WDT


class ControlPanel(Frame):
    def __init__(self, master=None, width=CTRL_PNL_WDT, height=CTRL_PNL_HGT):
        super(ControlPanel, self).__init__(master=master, width=width, height=height)
        self.config(padx=10, pady=10)
        self.config(highlightthickness=1, highlightbackground=OUT_CLR)

        Label(self, text='Display Options').grid(row=0, column=0, columnspan=1, sticky=W)

        self.show_clrs = BooleanVar(value=True)
        self.ck_clrs = Checkbutton(self, text="Show colors", variable=self.show_clrs, selectcolor='BLACK',
                                   command=lambda *args: self.event_generate("<<Show Color Change>>")
                                   ).grid(row=1, column=0, padx=10, pady=10, sticky=W)

        self.show_outline = BooleanVar(value=False)
        self.ck_outline = Checkbutton(self, text="Show outline", variable=self.show_outline, selectcolor='BLACK',
                                      command=lambda *args: self.event_generate("<<Show Outline Change>>")
                                      ).grid(row=1, column=1, padx=10, pady=10, sticky=W)

        self.show_points = BooleanVar(value=False)
        self.ck_dots = Checkbutton(self, text="Show points", variable=self.show_points, selectcolor='BLACK',
                                   command=lambda *args: self.event_generate("<<Show Points Change>>")
                                   ).grid(row=1, column=2, padx=10, pady=10, sticky=W)
