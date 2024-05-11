import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class frame_vtx():
    def __init__(self, parent):
        self._parent = parent
        self._frame = tk.Frame(parent)
        parent.add(self._frame, text="VTX")

        self.target_num = 0
        self.radio_button = []
        self.image = []
        self.tk_image = []
        self.vtx_target = tk.StringVar()

        for i in range(0, 4):
            self._frame.grid_rowconfigure(i, weight=1)
            self._frame.grid_columnconfigure(i, weight=1)

    def frame(self):
        return self._frame

    def create_radio_button_list(self, targets, callback, vtx_image):
        self.target_num = len(targets)
        for i in range(0, self.target_num):
            # self.image.append(Image.open(f"{i}.png"))
            self.tk_image.append(ImageTk.PhotoImage(vtx_image[i]))
            self.radio_button.append(ttk.Radiobutton(self._frame, image=self.tk_image[i],
                                                     variable=self.vtx_target, value=targets[i], compound="left", command=callback))
            self.radio_button[i].grid(
                row=(int)(i % 4), column=(int)(i/4), padx=5, pady=5)
        self.radio_button_reset()

    def radio_button_disable(self):
        for i in range(0, self.target_num):
            self.radio_button[i].config(state="disabled")

    def radio_button_enable(self):
        for i in range(0, self.target_num):
            self.radio_button[i].config(state="normal")

    def radio_button_reset(self):
        try:
            self.radio_button[0].invoke()
        except:
            pass
