from PIL import Image, ImageTk
import os
import tkinter as tk
from tkinter import HORIZONTAL, VERTICAL, ttk, StringVar
from tkinter import filedialog
import Download
from ch341_wrapper import *

from icon32 import icon32
import base64
import io

import zipfile

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
        self.fw_state = None
        self.update_btn = None
        self.load_fw_online_btn = None
        self.load_fw_local_btn = None
        self.init_done = 0
        self.downloadCommand = 0
        self.ch341Command = 0

        self.updateCnt = 0

        self.ver_index_select = 0
        self.vtx_index_select = 0
        self.vtx_name_select = ""

        self.create_root_window()
        self.create_version_combobox()
        self.switch_version_action()
        self.create_target_combobox()
        self.switch_target_action()
        self.create_auto_detect_btn()
        self.create_load_firmnware_online_btn()
        self.create_load_firmnware_local_btn()
        self.create_update_button()
        self.create_fw_state()
        self.create_prog_state()
        self.create_vtx_state()

    def create_root_window(self):
        titleString = "HDZero VTX Programmer"+" v"+version
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

        self.ver_combobox['value'] = Download.version_list
        self.ver_combobox.current(0)
        # self.ver_combobox.config(state=tk.DISABLED)

    def create_target_combobox(self):
        self.target_combobox = ttk.Combobox(self.master, state='readonly')
        self.target_combobox.anchor = 'NW'
        self.target_combobox.place(width=200, height=24, x=20, y=50)
        self.target_combobox['value'] = Download.vtx_name_list[0]
        self.target_combobox.current(0)
        # self.target_combobox.config(state=tk.DISABLED)

    def auto_detect_btn_callback(event):
        global my_gui
        ch341.command = 1
        my_gui.ch341Command = 1

    def create_auto_detect_btn(self):
        self.auto_btn = ttk.Button(
            self.master, text='Auto detect', command=self.auto_detect_btn_callback)
        self.auto_btn.anchor = 'NW'
        self.auto_btn.place(width=80, height=24, x=240, y=50)
        # self.auto_btn.config(state=tk.DISABLED)

    def create_fw_state(self):
        self.fw_state = ttk.Label(
            self.master, text="FW:", border=1, relief='ridge')
        self.fw_state.anchor = 'NW'
        self.fw_state.place(width=74, height=20, x=500, y=300)
        self.fw_state.config(background="#a0a0a0")

    def create_vtx_state(self):
        self.vtx_state = ttk.Label(
            self.master, text="VTX", border=1, relief='ridge')
        self.vtx_state.anchor = 'NW'
        self.vtx_state.place(width=28, height=20, x=574, y=300)
        self.vtx_state.config(background="#a0a0a0")

    def create_prog_state(self):
        self.prog_state = ttk.Label(
            self.master, text="PROG", border=1, relief='ridge')
        self.prog_state.anchor = 'NW'
        self.prog_state.place(width=38, height=20, x=602, y=300)
        self.prog_state.config(background="#a0a0a0")

    def switch_version_callback(self, event):
        self.ver_index_select = self.ver_combobox.current()
        self.target_combobox['value'] = Download.vtx_name_list[self.ver_index_select]
        self.target_combobox.current(0)

    def switch_version_action(self):
        self.ver_combobox.bind("<<ComboboxSelected>>",
                               self.switch_version_callback)

    def switch_vtx_callback(self, event):
        self.vtx_index_select = self.target_combobox.current()
        self.vtx_name_select = self.target_combobox['value'][self.vtx_index_select]

    def switch_target_action(self):
        self.target_combobox.bind(
            "<<ComboboxSelected>>", self.switch_vtx_callback)

    def load_firmware_online_callback(event):
        global my_gui
        if my_gui.vtx_index_select != 0 and my_gui.ver_index_select != 0:
            Download.downloadLink = firmware_link_list[my_gui.vtx_name_select]
            Download.localTemp = "./Data/Temp/fw.zip"
            Download.downloadCommand = 2
            my_gui.downloadCommand = 2
            my_gui.fw_state.config(text="FW:")
            my_gui.fw_state.config(background="#a0a0a0")
        else:
            print()
            print("Version and VTX must be specified.")

    def create_load_firmnware_online_btn(self):
        self.load_fw_online_btn = ttk.Button(
            self.master, text='Load Firmawre(Online)', command=self.load_firmware_online_callback)
        self.load_fw_online_btn.anchor = 'NW'
        self.load_fw_online_btn.place(width=150, height=24, x=20, y=100)

    def load_firmware_local_callback(event):
        global my_gui
        selected_file_path = filedialog.askopenfilename()
        if os.path.getsize(selected_file_path) <= 65536:
            ch341.fw_path = selected_file_path
            my_gui.fw_state.config(text="FW:Local")
            my_gui.fw_state.config(background="#42a459")
        else:
            print()
            print("local firmware error")
            my_gui.fw_state.config(text="FW:")
            my_gui.fw_state.config(background="#a0a0a0")

    def create_load_firmnware_local_btn(self):
        self.load_fw_local_btn = ttk.Button(
            self.master, text='Load Firmawre(Local)', command=self.load_firmware_local_callback)
        self.load_fw_local_btn.anchor = 'NW'
        self.load_fw_local_btn.place(width=150, height=24, x=180, y=100)

    def update_callback(event):
        global my_gui
        ch341.command = 2
        my_gui.ch341Command = 2
        my_gui.load_fw_online_btn.config(state=tk.DISABLED)
        my_gui.load_fw_local_btn.config(state=tk.DISABLED)
        my_gui.ver_combobox.config(state=tk.DISABLED)
        my_gui.target_combobox.config(state=tk.DISABLED)
        my_gui.update_btn.config(state=tk.DISABLED)
        my_gui.auto_btn.config(state=tk.DISABLED)


    def create_update_button(self):
        self.update_btn = ttk.Button(
            self.master, text='Update', command=self.update_callback)
        self.update_btn.anchor = 'NW'
        self.update_btn.place(width=70, height=24, x=340, y=100)


    def update_connection_state(self):
        # init download online info
        if self.updateCnt == 1:
            Download.downloadCommand = 1
        if self.updateCnt > 1 and Download.downloadCommand == 0 and self.init_done == 0:

            self.ver_combobox['value'] = Download.version_list
            self.ver_combobox.current(0)

            self.target_combobox['value'] = Download.vtx_name_list[0]
            self.target_combobox.current(0)

            self.init_done = 1

        if ch341.dev_connected == 0:
            self.prog_state.config(background="#a0a0a0")
        elif ch341.dev_connected == 1:
            self.prog_state.config(background="#42a459")

        if ch341.flash_connected == 0:
            self.vtx_state.config(background="#a0a0a0")
        elif ch341.dev_connected == 1:
            self.vtx_state.config(background="#42a459")

        if self.ch341Command != 2:
            if ch341.flash_connected == 1 and ch341.dev_connected == 1:
                self.auto_btn.config(state=tk.NORMAL)
                self.target_combobox.config(state="readonly")
                self.ver_combobox.config(state="readonly")
                self.load_fw_online_btn.config(state=tk.NORMAL)
                self.load_fw_local_btn.config(state=tk.NORMAL)
            else:
                self.auto_btn.config(state=tk.DISABLED)
                self.target_combobox.config(state=tk.DISABLED)
                self.target_combobox.current(0)
                self.ver_combobox.config(state=tk.DISABLED)
                self.ver_combobox.current(0)
                self.load_fw_online_btn.config(state=tk.DISABLED)
                self.load_fw_local_btn.config(state=tk.DISABLED)

        # check vtx id done
        if self.ch341Command == 1 and ch341.command == 0:
            j = 0
            for i in Download.vtx_id_list:
                if vtx_id_list[i] == ch341.vtx_id:
                    print()
                    print("Current vtx is", i)
                    if self.target_combobox['value'][j] == i:
                        self.target_combobox.current(j)
                        self.vtx_name_select = i
                        self.vtx_index_select = j
                j += 1
            self.ch341Command = 0

        # download online firmware done
        if self.downloadCommand == 2 and Download.downloadCommand == 0:
            print()
            print("download done, unziping...")
            zfile = zipfile.ZipFile(Download.localTemp, 'r')
            for filename in zfile.namelist():
                data = zfile.read(filename)
                file = open("./Data/Temp/"+filename, 'w+b')
                file.write(data)
                file.close()
            print("unzip done")
            self.downloadCommand = 0
            ch341.fw_path = "./Data/Temp/"+filename
            self.fw_state.config(text="FW:Online")
            self.fw_state.config(background="#42a459")
        
        if self.ch341Command != 2:
            if self.fw_state.cget('text') =="FW:":
                self.update_btn.config(state=tk.DISABLED)
            else:
                self.update_btn.config(state=tk.NORMAL)

        self.updateCnt += 1
        self.master.after(100, self.update_connection_state)


def UI_mainloop():
    global my_gui
    root = tk.Tk()
    my_gui = MyGUI(root)
    my_gui.update_connection_state()
    my_gui.master.mainloop()
