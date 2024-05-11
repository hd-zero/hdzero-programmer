import tkinter as tk
from tkinter import ttk


class frame_statusbar:
    def __init__(self, parent):
        self._parent = parent
        self._frame = tk.Frame(parent)

        self.init_progress_bar()
        self.progress_bar_set_value(0)
        self.init_label()
        self.label_hidden()

    def frame(self):
        return self._frame

    def label_hidden(self):
        self.label.place_forget()

    def label_show(self):
        self.label.place(relwidth=1, relheight=1)

    def init_label(self):
        self.label = tk.Label(self._frame, text="")
        self.status_label_set_bg("SystemButtonFace")

    def status_label_set_text(self, text, color):
        self.label["text"] = text
        self.status_label_set_bg(color)
        self.label_show()

    def status_label_set_bg(self, color):
        self.label["bg"] = color
        '''
        if color == 1: # system
            self.label["bg"] = "SystemButtonFace"
        elif color == 2: # red
            self.label["bg"] = "red"
        else: # green
            self.label["bg"] = "#06b025"
        '''

    def init_progress_bar(self):
        self.bar = ttk.Progressbar(
            self._frame, orient="horizontal", mode="determinate")
        self.bar.pack(fill="both", expand=True)

    def progress_bar_set_value(self, value):
        self.bar["value"] = value
