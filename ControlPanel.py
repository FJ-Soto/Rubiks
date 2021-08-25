from tkinter import *
from tkinter import colorchooser

from CONSTANTS import OUT_CLR, CTRL_PNL_HGT, CTRL_PNL_WDT, LBL_FONT


class ControlPanel(Frame):
    def __init__(self, master=None, width=CTRL_PNL_WDT, height=CTRL_PNL_HGT):
        super(ControlPanel, self).__init__(master=master, width=width, height=height)
        self.config(padx=20, pady=15)
        self.config(highlightthickness=1, highlightbackground=OUT_CLR)

        self.add_label(text='Cube Display Controls', row=0, pady=0)

        self.show_clrs = BooleanVar(value=True)
        self.ck_clrs = Checkbutton(self, text="Show colors", variable=self.show_clrs, selectcolor='BLACK',
                                   command=lambda *args: self.event_generate("<<showColorChange>>")
                                   ).grid(row=1, column=0, padx=(0, 10), sticky=W)

        self.show_outline = BooleanVar(value=False)
        self.ck_outline = Checkbutton(self, text="Show outline", variable=self.show_outline, selectcolor='BLACK',
                                      command=lambda *args: self.event_generate("<<showOutlineChange>>")
                                      ).grid(row=1, column=1, padx=(0, 10), sticky=W)

        self.show_points = BooleanVar(value=False)
        self.ck_dots = Checkbutton(self, text="Show points", variable=self.show_points, selectcolor='BLACK',
                                   command=lambda *args: self.event_generate("<<showPointsChange>>")
                                   ).grid(row=1, column=2, padx=(0, 10), pady=10, sticky=W)

        self.add_label(text="Color Scheme", row=2, pady=10)
        self.color_dict = {'FRONT': Label(self, text="", width=7, height=2),
                           'LEFT': Label(self, text="", width=7, height=2),
                           'TOP': Label(self, text="", width=7, height=2),
                           'BACK': Label(self, text="", width=7, height=2),
                           'RIGHT': Label(self, text="", width=7, height=2),
                           'BOTTOM': Label(self, text="", width=7, height=2)}
        for i, lbl in enumerate(self.color_dict.values()):
            lbl.grid(row=3 + (i // 3), column=i % 3, sticky=NSEW, padx=(0, 10), pady=(0, 10))
            lbl.bind('<Button-1>', self.change_color)

        Button(self, text="Reset Color Scheme",
               command=lambda *args: self.event_generate("<<resetColorScheme>>")
               ).grid(row=3, column=3, padx=10, sticky=N+EW)

        self.add_label(text="Rubik Rotations", row=9)

        self.cube_notation = {'U': Button(self)}
        for i, rot in enumerate(self.cube_notation):
            self.cube_notation[rot].config(text=rot)
            self.cube_notation[rot].bind('<Button-1>', self.cube_rotate)
            self.cube_notation[rot].grid(row=10, column=0, sticky=NSEW)

    def cube_rotate(self, e):
        self.event_generate(f'<<rotate_{e.widget.cget("text").lower()}>>')

    def change_color(self, e):
        col = colorchooser.askcolor(color=e.widget.cget("bg"), title="Select new color")
        e.widget.config(bg=col[1])
        self.event_generate("<<colorSchemeChange>>")

    def add_label(self, text, row, pady=(10, 0)):
        Label(self, text=text, font=LBL_FONT).grid(row=row, column=0, columnspan=3, pady=pady, sticky=W)

    def set_colors(self, color_dict):
        for color in color_dict:
            self.color_dict[color].config(bg=color_dict[color])

    def get_color_scheme(self):
        return {k: v.cget("bg") for k, v in self.color_dict.items()}
