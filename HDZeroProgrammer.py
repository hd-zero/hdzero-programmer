import sys
import tkinter as tk
from tkinter import ttk


def RootCreateWindow():
    titleString = "HDZero Programmer"
    windowX = 640
    windowY = 480
    offsetX = (root.winfo_screenwidth() - windowX)/2
    offsetY = (root.winfo_screenheight() - windowY)/2
    root.geometry('%dx%d+%d+%d' % (windowX, windowY, offsetX, offsetY))
    root.resizable(False, False)
    root.title(titleString)

root = tk.Tk()
RootCreateWindow();

root.mainloop()