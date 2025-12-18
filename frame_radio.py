import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class frame_radio:
    def __init__(self, parent):
        self._parent = parent
        self._frame = tk.Frame(parent)
        parent.add(self._frame, text="Radio")
        self.image_path = "resource/radio.png"
        self.show_image()

    def frame(self):
        return self._frame

    def show_image(self):
        image = Image.open(self.image_path)
        photo = ImageTk.PhotoImage(image)
        label = ttk.Label(self._frame, image=photo)
        label.image = photo
        label.pack()
