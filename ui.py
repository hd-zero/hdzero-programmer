from PIL import Image, ImageTk
import os
import tkinter as tk
from tkinter import HORIZONTAL, VERTICAL, ttk, StringVar
import Download
from ch341_wrapper import ch341

from icon32 import icon32
import base64
import io

version = "0.1"

class MyGUI:
    def __init__(self, master):
        self.master = master

        self.SelectedFirmwareString = ''
        self.target = 0
        self.targetNameString = tk.StringVar()

        self.ver_combobox = None
        self.target_combobox = None
        self.auto_btn = None
        self.prog_state = None
        self.vtx_state = None

        Download.LoadGithubFirmware()

        self.create_root_window()
        self.create_version_combobox()
        self.create_target_combobox()
        self.create_auto_detect_btn()
        self.create_prog_state()
        self.create_vtx_state()

        # self.CreateSeparator()
        # self.CreateLabel()
        # self.CreateLoadButton()
        # self.CreateDetectButton()
        # self.CreateDefineTargetButton()
        # self.CreateFlashButton()
        # self.CreateTargetPicture()
        # self.CreateTargetNameLabel()

    def create_root_window(self):
        titleString = "HDZero VTX Programmer"+" v"+version
        iconPath = 'Data/HDZero_16.ico'
        windowX = 640
        windowY = 320
        offsetX = (self.master.winfo_screenwidth() - windowX)/2
        offsetY = (self.master.winfo_screenheight() - windowY)/2
        self.master.geometry('%dx%d+%d+%d' %
                             (windowX, windowY, offsetX, offsetY))
        self.master.resizable(False, False)
        self.master.title(titleString)
        self.master.configure(bg="#303030")

        icon_base64 = base64.b64decode(icon32)
        icon_bytes = io.BytesIO(icon_base64)
        icon = tk.PhotoImage(data=icon_bytes.getvalue())

        self.master.iconphoto(True, icon)

    def create_version_combobox(self):
        self.ver_combobox = ttk.Combobox(self.master, state='readonly')
        self.ver_combobox.anchor = 'NW'
        self.ver_combobox.place(width=200, height=24, x=20, y=20)
        self.ver_combobox.config(state=tk.DISABLED)

    def create_target_combobox(self):
        self.target_combobox = ttk.Combobox(self.master, state='readonly')
        self.target_combobox.anchor = 'NW'
        self.target_combobox.place(width=200, height=24, x=20, y=50)
        self.target_combobox['value'] = Download.ParseTargetList()
        self.target_combobox.current(0)
        self.target_combobox.config(state=tk.DISABLED)

    def create_auto_detect_btn(self):
        self.auto_btn = ttk.Button(self.master, text='Auto detect')
        self.auto_btn.anchor = 'NW'
        self.auto_btn.place(width=80, height=24, x=240, y=50)
        self.auto_btn.config(state=tk.DISABLED)

    def create_prog_state(self):
        self.prog_state = ttk.Label(self.master, text="PROG", border=1, relief='ridge')
        self.prog_state.anchor = 'NW'
        self.prog_state.place(width=38, height=20, x=602, y=0)
        self.prog_state.config(background="red")

    def create_vtx_state(self):
        self.vtx_state = ttk.Label(self.master, text="VTX", border=1, relief='ridge')
        self.vtx_state.anchor = 'NW'
        self.vtx_state.place(width=28, height=20, x=574, y=0)
        self.vtx_state.config(background="red")

    def update_connection_state(self):
        if ch341.dev_connected == 0:
            self.prog_state.config(background="#a0a0a0")
        elif ch341.dev_connected == 1:
            self.prog_state.config(background="#42a459")

        if ch341.flash_connected == 0:
            self.vtx_state.config(background="#a0a0a0")
        elif ch341.dev_connected == 1:
            self.vtx_state.config(background="#42a459")

        if ch341.flash_connected == 1 and ch341.dev_connected == 1:
            self.auto_btn.config(state=tk.NORMAL)
            self.target_combobox.config(state=tk.NORMAL)
            self.ver_combobox.config(state=tk.NORMAL)
        else:
            self.auto_btn.config(state=tk.DISABLED)
            self.target_combobox.config(state=tk.DISABLED)
            self.ver_combobox.config(state=tk.DISABLED)

        self.master.after(100, self.update_connection_state)

    # def CreateSeparator(self):
    #     sep_hor1 = ttk.Separator(self, orient=HORIZONTAL)
    #     sep_hor1.anchor = 'NW'
    #     sep_hor1.place(width=800, height=1, x=0, y=400)
    #     sep_hor2 = ttk.Separator(self, orient=HORIZONTAL)
    #     sep_hor2.anchor = 'NW'
    #     sep_hor2.place(width=600, height=1, x=0, y=690)
    #     sep_ver1 = ttk.Separator(self, orient=VERTICAL)
    #     sep_ver1.anchor = 'NW'
    #     sep_ver1.place(width=1, height=400, x=300, y=0)

    # def LoadGithubButtonCommand(self):
    #     Download.LoadGithubFirmwareRequest()

    # def DetectTargetButtonCommand(self):
    #     # self.target = targetDetect()

    #     self.target = self.target + 1
    #     if self.target > Download.targetTypeNum:
    #         self.target = 0

    #     self.CreateTargetPicture()
    #     #self.CreateTargetNameLabel()

    # def CreateTargetPicture(self):
    #     global photo

    #     Witdh = 300
    #     Height = 400

    #     try:
    #         if self.targetPicture != None:
    #             self.targetPicture.destroy()
    #     except:
    #         a = 1

    #     if self.target == 0:
    #         img_path = './Data/Github/HDZero.png'
    #     else:
    #         img_path = './Data/Github/Target_Info/' + \
    #             Download.targetTypeList[self.target-1] + '/' + \
    #             Download.targetTypeList[self.target-1] + '.png'

    #     try:
    #         img = Image.open(img_path)
    #         photo = ImageTk.PhotoImage(img)
    #         offsetX = (Witdh - photo.width()) / 2
    #         offsetY = (Height - photo.height()) / 2
    #         self.targetPicture = tk.Label(self, image=photo)
    #         self.targetPicture.anchor = 'NW'
    #         self.targetPicture.place(x=offsetX, y=offsetY)
    #     except:
    #         print("DBG:Can't find img_path")

    # #def CreateTargetNameLabel(self):
    # #    try:
    # #        if self.targetLabel != None:
    # #            self.targetLabel.destroy()
    # #    except:
    # #        a = 1
    # #    self.UpdateTargetNameString()
    # #    self.targetLabel = tk.Label(self, text=self.targetNameString.get())
    # #    self.targetLabel.anchor = 'NW'
    # #    self.targetLabel.place(x=80, y=340)

    # def UpdateTargetNameString(self):
    #     if self.target == 0:
    #         self.targetNameString.set('disconnected')
    #     elif self.target == 255:
    #         self.targetNameString.set('unknow')
    #     elif self.target > Download.targetTypeNum:
    #         self.targetNameString.set('unknow')
    #     else:
    #         self.targetNameString.set(Download.targetTypeList[self.target-1])

    # def CreateLoadButton(self):
    #     buttonLoadGithubString = "Load Firmware[Github]"
    #     LoadGithubButton = ttk.Button(self, text=buttonLoadGithubString,
    #                                   command=self.LoadGithubButtonCommand)
    #     LoadGithubButton.anchor = 'NW'
    #     LoadGithubButton.place(x=310, y=370)

    #     buttonLoadLocalString = "Load Firmware[Local]"
    #     reloadButton = ttk.Button(self, text=buttonLoadLocalString,
    #                               command=self.LoadGithubButtonCommand)
    #     reloadButton.anchor = 'NW'
    #     reloadButton.place(x=460, y=370)

    # def CreateFlashButton(self):
    #     buttonFlashString = "Flash"
    #     FlashButton = ttk.Button(self, text=buttonFlashString,
    #                              command=self.LoadGithubButtonCommand)
    #     FlashButton.anchor = 'NW'
    #     FlashButton.place(x=610, y=370)

    # def CreateDetectButton(self):
    #     buttonDetectString = "Detect"
    #     DetectButton = ttk.Button(self, text=buttonDetectString,
    #                               command=self.DetectTargetButtonCommand)
    #     DetectButton.anchor = 'NW'
    #     DetectButton.place(x=110, y=370)

    # def CreateDefineTargetButton(self):
    #     buttonDefineTargetString = "Define Target"
    #     DefineTargetButton = ttk.Button(self, text=buttonDefineTargetString,
    #                                     command=self.LoadGithubButtonCommand)
    #     DefineTargetButton.anchor = 'NW'
    #     DefineTargetButton.place(x=630, y=692)

    # def CreateLabel(self):
    #     targetLabelString = "Target"
    #     targetLabel = tk.Label(self, text=targetLabelString, bg="dimgray",
    #                            fg="white", font=("Consolas", 15, "bold"))
    #     targetLabel.anchor = 'NW'
    #     targetLabel.place(x=110, y=10)

    #     firmwareLabelString = "Firmware"
    #     firmwareLabel = tk.Label(self, text=firmwareLabelString, bg="dimgray",
    #                              fg="white", font=("Consolas", 15, "bold"))
    #     firmwareLabel.anchor = 'NW'
    #     firmwareLabel.place(x=460, y=10)

    #     messageLabelString = "Message"
    #     messageLabel = tk.Label(self, text=messageLabelString, bg="dimgray",
    #                             fg="white", font=("Consolas", 15, "bold"))
    #     messageLabel.anchor = 'NW'
    #     messageLabel.place(x=10, y=410)

    #     statusLabelString = "Status"
    #     statusLabel = tk.Label(self, text=statusLabelString, bg="dimgray",
    #                            fg="white", font=("Consolas", 10, "bold"))
    #     statusLabel.anchor = 'NW'
    #     statusLabel.place(x=5, y=695)

    #     SelectedString = 'Selected'
    #     SelectedLabel = tk.Label(self, text=SelectedString, bg="dimgray",
    #                              fg="white", font=("Consolas", 10, "bold"))
    #     SelectedLabel.anchor = 'NW'
    #     SelectedLabel.place(x=320, y=340)

    #     SelectedFirmwareLabel = tk.Label(
    #         self, text=self.SelectedFirmwareString)
    #     SelectedFirmwareLabel.anchor = 'NW'
    #     SelectedFirmwareLabel.place(x=390, y=342)


def UI_mainloop():
    root = tk.Tk()
    my_gui = MyGUI(root)
    my_gui.update_connection_state()
    my_gui.master.mainloop()
