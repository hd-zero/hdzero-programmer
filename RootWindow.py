#from msilib.schema import Font
import os
import tkinter as tk
from tkinter import HORIZONTAL, VERTICAL, ttk
from Download import LoadGithubFirmwareRequest

version = "0.1"
root = tk.Tk()


def CreateRootWindow():
    titleString = "HDZero Programmer"+" v"+version
    iconPath = 'Data/HDZero_16.ico'
    windowX = 720
    windowY = 720
    offsetX = (root.winfo_screenwidth() - windowX)/2
    offsetY = (root.winfo_screenheight() - windowY)/2
    root.geometry('%dx%d+%d+%d' % (windowX, windowY, offsetX, offsetY))
    root.resizable(False, False)
    root.title(titleString)
    if os.path.exists(iconPath):
        root.iconbitmap(iconPath)


def CreateSeparator():
    sep_hor1 = ttk.Separator(root, orient=HORIZONTAL)
    sep_hor1.anchor = 'NW'
    sep_hor1.place(width=720, height=1, x=0, y=400)
    sep_hor2 = ttk.Separator(root, orient=HORIZONTAL)
    sep_hor2.anchor = 'NW'
    sep_hor2.place(width=720, height=1, x=0, y=690)
    sep_ver1 = ttk.Separator(root, orient=VERTICAL)
    sep_ver1.anchor = 'NW'
    sep_ver1.place(width=1, height=400, x=300, y=0)


def LoadGithubButtonCommand():
    LoadGithubFirmwareRequest()


def CreateLoadButton():
    buttonLoadGithubString = "Load Firmware[Github]"
    LoadGithubButton = ttk.Button(root, text=buttonLoadGithubString,
                                  command=LoadGithubButtonCommand)
    LoadGithubButton.anchor = 'NW'
    LoadGithubButton.place(x=310, y=360)

    buttonLoadLocalString = "Load Firmware[Local]"
    reloadButton = ttk.Button(root, text=buttonLoadLocalString,
                              command=LoadGithubButtonCommand)
    reloadButton.anchor = 'NW'
    reloadButton.place(x=460, y=360)

def CreateFlashButton():
    buttonFlashString = "Flash"
    FlashButton = ttk.Button(root, text=buttonFlashString,
                                  command=LoadGithubButtonCommand)
    FlashButton.anchor = 'NW'
    FlashButton.place(x=610, y=360)


def CreateLabel():
    vtxLabelString = "VTX Type"
    vtxLabel = tk.Label(root, text=vtxLabelString, bg="dimgray",
                        fg="white", font=("Consolas", 15, "bold"))
    vtxLabel.anchor = 'NW'
    vtxLabel.place(x=95, y=10)

    firmwareLabelString = "Firmware"
    firmwareLabel = tk.Label(root, text=firmwareLabelString, bg="dimgray",
                        fg="white", font=("Consolas", 15, "bold"))
    firmwareLabel.anchor = 'NW'
    firmwareLabel.place(x=460, y=10)

    messageLabelString = "Message"
    messageLabel = tk.Label(root, text=messageLabelString, bg="dimgray",
                        fg="white", font=("Consolas", 15, "bold"))
    messageLabel.anchor = 'NW'
    messageLabel.place(x=10, y=410)

    statusLabelString = "Status"
    statusLabel = tk.Label(root, text=statusLabelString, bg="dimgray",
                        fg="white", font=("Consolas", 10, "bold"))
    statusLabel.anchor = 'NW'
    statusLabel.place(x=5, y=695)


def RootThreadProc():
    CreateRootWindow()
    CreateSeparator()
    CreateLabel()
    CreateLoadButton()
    CreateFlashButton()
