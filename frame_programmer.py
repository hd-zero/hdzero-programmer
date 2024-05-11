import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os


class frame_programmer:
    def __init__(self, parent):
        self._parent = parent
        self._frame = tk.Frame(self._parent)

        self._frame.grid_rowconfigure(0, weight=1)
        self._frame.grid_rowconfigure(1, weight=1)
        self._frame.grid_rowconfigure(2, weight=1)
        self._frame.grid_columnconfigure(0, weight=1)
        self._frame.grid_columnconfigure(1, weight=1)
        self._frame.grid_columnconfigure(2, weight=1)

        self.online_list = []
        self.mode = 0  # 0/1 : url/local path
        self.local_file_path = ""
        self.local_file_path_shorten = ""
        self.url = ""

        self.is_cancel = 0

        self.is_load_online = tk.StringVar()

        self.version_combobox = ttk.Combobox(
            self._frame, values=self.online_list, state="readonly")
        self.version_combobox_set_default()
        self.version_combobox_disable()

        self.online_fw_button = ttk.Radiobutton(
            self._frame, text="Load Online Firmware", variable=self.is_load_online, value='1')
        self.online_fw_button_show()
        self.online_fw_button_disable()

        self.local_fw_button = ttk.Radiobutton(
            self._frame, text="Load Local Firmware", variable=self.is_load_online, value='0')
        self.local_fw_button.grid(row=1, column=1, padx=5, pady=5)
        self.local_fw_button_disable()

        self.update_button = tk.Button(self._frame)
        self.update_button.grid(row=1, column=2, padx=5, pady=5)

        self.update_button_set_text_update("VTX")
        self.update_button_disable()

    def frame(self):
        return self._frame

    def version_combobox_set_default(self):
        self.version_combobox.set("Load Online Fiwmare")

    def version_combobox_disable(self):
        self.version_combobox["state"] = "disabled"

    def version_combobox_enable(self):
        self.version_combobox["state"] = "readonly"

    def version_combobox_update_values(self, new_values):
        self.online_list = new_values
        self.version_combobox.configure(values=self.online_list)

    def online_fw_button_disable(self):
        self.online_fw_button.config(state="disabled")

    def online_fw_button_enable(self, network_error):
        if network_error:
            self.online_fw_button_disable()
        else:
            self.online_fw_button.config(state="normal")

    def online_fw_button_show(self):
        self.online_fw_button.grid(row=1, column=0, padx=5, pady=5)
        self.version_combobox.grid_remove()

    def online_fw_button_hidden(self):
        self.version_combobox.grid(
            row=1, column=0, padx=5, pady=5)
        self.version_combobox.event_generate('<Button-1>')
        self.online_fw_button.grid_remove()
        self.local_fw_button_set_str_default()

    def online_fw_button_set_str(self, str):
        self.online_fw_button['text'] = str

    def online_fw_button_set_str_default(self):
        self.online_fw_button['text'] = "Load Online Firmware"

    def local_fw_button_disable(self):
        self.local_fw_button.config(state="disabled")

    def local_fw_button_enable(self):
        self.local_fw_button.config(state="normal")

    def local_fw_button_set_str(self, str):
        self.local_fw_button["text"] = str

    def local_fw_button_set_str_default(self):
        self.local_fw_button["text"] = "Load Local Firmware"

    def deselect(self):
        self.is_load_online.set("")

    def select_local_file(self):
        self.version_combobox_set_default()
        self.online_fw_button_set_str_default()
        filetypes = (("Bin files", "*.bin"), ("All files", "*.*"))

        try:
            with open("resource/local_path", "r") as file:
                path = file.read()
                file.close()
        except:
            path = "."

        try:
            self.local_file_path = filedialog.askopenfilename(
                initialdir=path, title="select a firmware", filetypes=filetypes)
        except:
            print("please select a firmware file")

        if self.local_file_path:
            self.mode = 1
            self.local_file_path_shorten = self.shorten_path(
                self.local_file_path)
            self.local_fw_button_set_str(self.local_file_path_shorten)
            path = self.local_file_path[:self.local_file_path.rfind('/') + 1]
            with open("resource/local_path", "w") as file:
                file.write(path)
                file.close()

    def update_button_disable(self):
        self.update_button["state"] = "disabled"
        self.update_button["bg"] = "SystemButtonFace"

    def update_button_enable(self):
        self.update_button["state"] = "normal"
        if self.update_button["text"] == "Cancel":
            self.update_button["bg"] = "red"
        else:
            self.update_button["bg"] = "#06b025"

    def update_button_set_text_cancel(self):
        self.is_cancel = 1
        self.update_button["text"] = "Cancel"

    def update_button_set_text_update(self, string):
        self.is_cancel = 0
        self.update_button["text"] = "Flash " + string

    def shorten_path(self, path, max_length=40):
        if len(path) <= max_length:
            return path
        else:
            head, tail = os.path.split(path)
            while len(head) + len(tail) + 4 > max_length:
                head = os.path.split(head)[0]
            return os.path.join(head, "..." + tail)
