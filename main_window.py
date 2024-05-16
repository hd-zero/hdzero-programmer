import sys
import os

import tkinter as tk
from tkinter import ttk

from frame_vtx import frame_vtx
from frame_monitor import frame_monitor
from frame_event_vrx import frame_event_vrx
from frame_programmer import frame_programmer
from frame_statusbar import frame_statusbar

from downloader import *
from parse_file import *
import global_var
from global_var import *
from ch341 import my_ch341
import base64
from icon32 import icon32
import io


class MyGUI:

    def __init__(self, init_window_name):
        self.winWidth = 800
        self.winHeight = 600
        self.title = "HDZero Programmer " + "V2.0.0"

        self._programmer_frame = None
        self._main_window = init_window_name
        self._main_window.grid_rowconfigure(0, weight=18)
        self._main_window.grid_rowconfigure(1, weight=0)
        self._main_window.grid_rowconfigure(2, weight=0)
        self._main_window.grid_columnconfigure(0, weight=1)

        self.init_tab()
        self.init_programmer()
        self._programmer_frame.frame().grid(row=1, column=0, sticky="nsew")

        self.init_statusbar()
        self._statusbar_frame.frame().grid(row=2, column=0, sticky="nsew")

        self.is_update_monitor = 0
        self.monitor_is_alive = 0

        self.downloading_window_status = 0
        self.network_error = 0

    def init_main_window(self):
        screenWidth = self._main_window.winfo_screenwidth()
        screenHeight = self._main_window.winfo_screenheight()
        x = int((screenWidth - self.winWidth) / 2)
        y = int((screenHeight - self.winHeight) / 2)

        self._main_window.title(self.title)
        self._main_window.geometry("%sx%s+%s+%s" %
                                   (self.winWidth, self.winHeight, x, y))
        self._main_window.resizable(False, False)

        icon_base64 = base64.b64decode(icon32)
        icon_bytes = io.BytesIO(icon_base64)
        icon = tk.PhotoImage(data=icon_bytes.getvalue())

        self._main_window.iconphoto(True, icon)

    def init_tab(self):
        self._tabCtrl = ttk.Notebook(self._main_window)
        self.init_main_window()
        self.init_vtx_frame()
        self.init_monitor_frame()
        self.init_event_vrx_frame()
        self._tabCtrl.select(self._vtx_frame.frame())
        self._tabCtrl.grid(row=0, column=0, sticky="nsew")
        self._tabCtrl.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        self.notebook_disable()

    def notebook_disable(self):
        self._tabCtrl.state(['disabled'])

    def notebook_enable(self):
        self._tabCtrl.state(['!disabled'])

    def init_programmer(self):
        self._programmer_frame = frame_programmer(self._main_window)
        self._programmer_frame.version_combobox.bind(
            "<<ComboboxSelected>>",  self.on_select_version)
        self._programmer_frame.online_fw_button["command"] = self._programmer_frame.online_fw_button_hidden
        self._programmer_frame.local_fw_button["command"] = self.on_load_local_firmware
        self._programmer_frame.update_button["command"] = self.on_update

    def init_vtx_frame(self):
        self._vtx_frame = frame_vtx(self._tabCtrl)
        for i in range(0, len(list(my_parse.vtx_info.keys()))):
            self._vtx_frame.radio_button[i].bind(
                "<Button-1>", self.on_select_vtx_target)

    def init_monitor_frame(self):
        self._monitor_frame = frame_monitor(self._tabCtrl)

    def init_event_vrx_frame(self):
        self._event_vrx_frame = frame_event_vrx(self._tabCtrl)

    def init_statusbar(self):
        self._statusbar_frame = frame_statusbar(self._main_window)

    def on_select_vtx_target(self):
        selected_target = self._vtx_frame.vtx_target.get()
        print("Selected target:", selected_target)
        try:
            version_list = list(my_parse.vtx_info[selected_target].keys())[1:]
            self._programmer_frame.version_combobox_update_values(version_list)
        except:
            pass
        self._programmer_frame.version_combobox_set_default()
        self._programmer_frame.version_combobox_enable()

        self._programmer_frame.online_fw_button_enable(self.network_error)
        self._programmer_frame.online_fw_button_set_str_default()

        self._programmer_frame.local_fw_button_enable()
        self._programmer_frame.local_fw_button_set_str_default()

    def on_select_version(self, event):
        selected_version = self._programmer_frame.version_combobox.get()
        print("Selected:", selected_version)
        self._programmer_frame.mode = 0
        self._programmer_frame.online_fw_button_show()

        if self.current_selected_tab() == 0:
            self._programmer_frame.update_button_enable()
            self._programmer_frame.url = my_parse.vtx_info[self._vtx_frame.vtx_target.get(
            )][self._programmer_frame.version_combobox.get()]
            self._programmer_frame.online_fw_button_set_str(
                self._programmer_frame.version_combobox.get())
        elif self.current_selected_tab() == 1:
            self._programmer_frame.update_button_enable()
            self._programmer_frame.url = my_parse.monitor_info[self._programmer_frame.version_combobox.get(
            )]
            self._programmer_frame.online_fw_button_set_str(
                self._programmer_frame.version_combobox.get())
        elif self.current_selected_tab() == 2:
            self._programmer_frame.update_button_enable()
            self._programmer_frame.url = my_parse.event_vrx_info[self._programmer_frame.version_combobox.get(
            )]
            self._programmer_frame.online_fw_button_set_str(
                self._programmer_frame.version_combobox.get())

    def on_load_local_firmware(self):
        self._programmer_frame.online_fw_button_show()
        self._programmer_frame.select_local_file()

        if self._programmer_frame.local_file_path == '':
            return

        if self.current_selected_tab() == 0:
            self._programmer_frame.mode = 1
            self._programmer_frame.update_button_enable()
            my_ch341.fw_path = self._programmer_frame.local_file_path

        elif self.current_selected_tab() == 1:
            self._programmer_frame.update_button_enable()
            self._programmer_frame.mode = 1
            my_ch341.fw_path = self._programmer_frame.local_file_path

        elif self.current_selected_tab() == 2:
            self._programmer_frame.update_button_enable()
            self._programmer_frame.mode = 1
            my_ch341.fw_path = self._programmer_frame.local_file_path

    def on_update(self):
        if self.current_selected_tab() == 0:

            if self._programmer_frame.is_cancel == 0:
                my_ch341.status = ch341_status.VTX_DISCONNECTED.value  # to connect vtx
                my_download.to_stop = 0

                self.notebook_disable()

                self._vtx_frame.radio_button_disable()

                # self._programmer_frame.update_button_disable()
                self._programmer_frame.update_button_set_text_cancel()
                self._programmer_frame.update_button_enable()
                self._programmer_frame.version_combobox_disable()
                self._programmer_frame.local_fw_button_disable()
                self._programmer_frame.online_fw_button_disable()

                self._statusbar_frame.status_label_set_text(
                    "Connecting VTX ...", "SystemButtonFace")
                self._statusbar_frame.progress_bar_set_value(0)
            else:
                my_ch341.status = ch341_status.IDLE.value
                my_download.to_stop = 1

                self.notebook_enable()

                self._vtx_frame.radio_button_enable()

                self._programmer_frame.update_button_set_text_update("VTX")
                self._programmer_frame.update_button_enable()
                self._programmer_frame.version_combobox_enable()
                self._programmer_frame.local_fw_button_enable()
                self._programmer_frame.online_fw_button_enable(
                    self.network_error)

                self._statusbar_frame.label_hidden()
                self._statusbar_frame.progress_bar_set_value(0)

        elif self.current_selected_tab() == 1:
            if self._programmer_frame.is_cancel == 0:
                self.is_update_monitor = 1
                my_ch341.monitor_connected = 0
                my_ch341.status = ch341_status.IDLE.value
                my_download.to_stop = 0

                self.notebook_disable()

                self._monitor_frame.setting_disable()

                self._programmer_frame.update_button_set_text_cancel()
                self._programmer_frame.update_button_enable()
                self._programmer_frame.version_combobox_disable()
                self._programmer_frame.local_fw_button_disable()
                self._programmer_frame.online_fw_button_disable()

                self._statusbar_frame.status_label_set_text(
                    "Connecting Monitor ...", "SystemButtonFace")
                self._statusbar_frame.progress_bar_set_value(0)
            else:
                print("cancel Monitor programmer")
                self.is_update_monitor = 0
                my_ch341.monitor_connected = 0
                self.monitor_is_alive = 0
                my_ch341.status = ch341_status.IDLE.value
                my_download.to_stop = 1

                self.notebook_enable()

                self._monitor_frame.setting_disable()

                self._programmer_frame.update_button_set_text_update(
                    "Monitor")
                self._programmer_frame.update_button_enable()
                self._programmer_frame.version_combobox_enable()
                self._programmer_frame.local_fw_button_enable()
                self._programmer_frame.online_fw_button_enable(
                    self.network_error)

                self._statusbar_frame.label_hidden()
                self._statusbar_frame.progress_bar_set_value(0)

        elif self.current_selected_tab() == 2:
            if self._programmer_frame.is_cancel == 0:
                my_ch341.status = ch341_status.EVENT_VRX_DISCONNECTED.value
                my_download.to_stop = 0

                self.notebook_disable()

                self._programmer_frame.update_button_set_text_cancel()
                self._programmer_frame.update_button_enable()
                self._programmer_frame.version_combobox_disable()
                self._programmer_frame.local_fw_button_disable()
                self._programmer_frame.online_fw_button_disable()
                self._statusbar_frame.status_label_set_text(
                    "Connecting Event VRX ...", "SystemButtonFace")
                self._statusbar_frame.progress_bar_set_value(0)
            else:
                my_download.to_stop = 1
                my_ch341.status = ch341_status.IDLE.value

                self.notebook_enable()

                self._programmer_frame.update_button_set_text_update(
                    "Event VRX")
                self._programmer_frame.update_button_disable()
                self._programmer_frame.version_combobox_enable()
                self._programmer_frame.local_fw_button_enable()
                self._programmer_frame.online_fw_button_enable(
                    self.network_error)

                self._statusbar_frame.label_hidden()
                self._statusbar_frame.progress_bar_set_value(0)

    def on_tab_changed(self, event):
        print("Selected tab:", self.current_selected_tab())
        self._statusbar_frame.label_hidden()
        if self.current_selected_tab() == 0:
            self._vtx_frame.radio_button_reset()  # select first vtx target

            self._programmer_frame.version_combobox_update_values("")
            self._programmer_frame.version_combobox_set_default()
            self._programmer_frame.version_combobox_disable()
            # self._programmer_frame.local_fw_button_disable()
            self._programmer_frame.update_button_set_text_update("VTX")
            self._programmer_frame.update_button_disable()
            self._programmer_frame.online_fw_button_show()

            self.on_select_vtx_target()
            my_ch341.status = ch341_status.IDLE.value

        elif self.current_selected_tab() == 1:
            self._monitor_frame.setting_disable()

            version_list = list(my_parse.monitor_info.keys())
            self._programmer_frame.version_combobox_update_values(version_list)
            self._programmer_frame.version_combobox_set_default()
            self._programmer_frame.version_combobox_enable()
            self._programmer_frame.local_fw_button_enable()
            self._programmer_frame.update_button_set_text_update(
                "Monitor")
            self._programmer_frame.update_button_disable()
            self._programmer_frame.online_fw_button_show()
            self.monitor_is_alive = 0
            my_ch341.monitor_connected = 0

            # to connect Monitor
            my_ch341.status = ch341_status.MONITOR_CHECK_ALIVE.value
        elif self.current_selected_tab() == 2:
            version_list = list(my_parse.event_vrx_info.keys())
            self._programmer_frame.version_combobox_update_values(version_list)
            self._programmer_frame.version_combobox_enable()
            self._programmer_frame.version_combobox_set_default()
            self._programmer_frame.local_fw_button_enable()
            self._programmer_frame.update_button_set_text_update("Event VRX")
            self._programmer_frame.update_button_disable()
            self._programmer_frame.online_fw_button_show()

            my_ch341.status = ch341_status.IDLE.value

        self._programmer_frame.deselect()
        self._programmer_frame.online_fw_button_set_str_default()
        self._programmer_frame.online_fw_button_enable(self.network_error)
        self._programmer_frame.local_fw_button_set_str_default()

    def current_selected_tab(self):
        return self._tabCtrl.index(self._tabCtrl.select())

    def create_downloading_firmware_window(self):
        if self.downloading_window_status == 1:
            pass
        screenWidth = self._main_window.winfo_screenwidth()
        screenHeight = self._main_window.winfo_screenheight()
        x = int((screenWidth - 300) / 2)
        y = int((screenHeight - 50) / 2)

        self.downloading_window = tk.Toplevel()
        self.downloading_window.geometry("%sx%s+%s+%s" %
                                         (300, 50, x, y))
        self.downloading_window.resizable(False, False)

        self.downloading_window.title("Downloading")
        self.downloading_label = tk.Label(self.downloading_window,
                                          text="Downloading firmware list from github ...")
        self.downloading_label.pack(pady=10)

        self.downloading_window_status = 1
        self.downloading_window.overrideredirect(True)

        #self._main_window.attributes('-disable', True)

    def set_downloading_label(self, str):
        self.downloading_label.config(text=str)

    def destroy_downloading_firmware_window(self):
        self.downloading_window.destroy()
        self.notebook_enable()
        self._main_window.focus_force()

    def refresh(self):
        '''
        1. update vtx
        -   press update button
        -   connect vtx
        -   wait until vtx is connected
        -   download fw if use online fw
        -   wait until download is done if use online fw
        -   write vtx id & fw to flash
        -   wait until write done

        2. update Monitor
        -
        -
        3. update event vrx
        '''

        # init
        if my_download.status == download_status.FILE_PARSE.value:
            my_download.status = download_status.IDLE.value
            my_parse.parse_vtx_common()
            ret0 = my_parse.parse_vtx_releases()
            ret1 = my_parse.parse_event_vrx_releases()
            ret2 = my_parse.parse_monitor_releases()
            ret3 = my_parse.parse_vtx_tragets_image(
                len(list(my_parse.vtx_info.keys())))

            if ret0 == 0 or ret1 == 0 or ret2 == 0 or ret3 == 0:
                self.network_error = 1
                self.set_downloading_label("Download firmware list failed")
                self._main_window.update()
                time.sleep(1)
            self.destroy_downloading_firmware_window()

            self._vtx_frame.create_radio_button_list(
                list(my_parse.vtx_info.keys()), self.on_select_vtx_target, my_parse.vtx_target_image)
            #self._main_window.attributes('-disable', False)

        # vtx
        if self.current_selected_tab() == 0:
            # download
            if my_download.status == download_status.DOWNLOAD_VTX_FW_DONE.value:
                my_download.status = download_status.IDLE.value
                selected_target = self._vtx_frame.vtx_target.get()
                my_ch341.target_id = my_parse.vtx_info[selected_target]["id"]
                my_ch341.fw_path = my_download.save_path
                my_ch341.written_len = 0
                my_ch341.status = ch341_status.VTX_UPDATE.value
                self._statusbar_frame.label_hidden()
                self._programmer_frame.update_button_set_text_update("VTX")
                self._programmer_frame.update_button_disable()
            elif my_download.status == download_status.DOWNLOAD_VTX_FW_FAILED.value:
                my_download.status = download_status.IDLE.value
                my_ch341.status = ch341_status.IDLE.value

                self.notebook_enable()

                self._vtx_frame.radio_button_enable()

                self._programmer_frame.version_combobox_enable()
                self._programmer_frame.online_fw_button_enable(
                    self.network_error)
                self._programmer_frame.version_combobox_set_default()
                self._programmer_frame.local_fw_button_enable()
                self._programmer_frame.update_button_set_text_update("VTX")
                # self._programmer_frame.update_button_disable()
                self._programmer_frame.deselect()

                self._statusbar_frame.progress_bar_set_value(0)
                self._statusbar_frame.status_label_set_text(
                    "Firmware update failed. Network error.", "red")

            # update
            if my_ch341.status == ch341_status.VTX_CONNECTED.value:  # vtx is connected
                my_ch341.status = ch341_status.IDLE.value
                if self._programmer_frame.mode == 0:
                    my_download.url = self._programmer_frame.url
                    my_download.save_path = "resource/FW"
                    my_download.status = download_status.DOWNLOAD_VTX_FW.value  # download url
                    self._statusbar_frame.status_label_set_text(
                        "Downloading Firmware ...", "SystemButtonFace")
                else:
                    selected_target = self._vtx_frame.vtx_target.get()
                    my_ch341.target_id = my_parse.vtx_info[selected_target]["id"]
                    my_ch341.fw_path = self._programmer_frame.local_file_path
                    my_ch341.status = ch341_status.VTX_UPDATE.value
                    self._statusbar_frame.label_hidden()
                    self._programmer_frame.update_button_set_text_update("VTX")
                    self._programmer_frame.update_button_disable()

            elif my_ch341.status == ch341_status.VTX_UPDATE.value:  # refresh progress bar
                value = (my_ch341.written_len /
                         my_ch341.to_write_len * 100) % 101
                self._statusbar_frame.progress_bar_set_value(value)
            elif my_ch341.status == ch341_status.VTX_UPDATEDONE.value:  # vtx update done
                self._statusbar_frame.progress_bar_set_value(100)
                self._statusbar_frame.status_label_set_text(
                    "Firmware updated. Connect another VTX(the same type) to update, or click cancel to finish.", "#06b025")
                my_ch341.status = ch341_status.VTX_RECONNECT.value
                self._programmer_frame.update_button_set_text_cancel()
                self._programmer_frame.update_button_enable()

                """
                my_ch341.status = ch341_status.IDLE.value

                self.notebook_enable()

                self._vtx_frame.radio_button_enable()

                self._programmer_frame.version_combobox_enable()
                self._programmer_frame.version_combobox_set_default()

                self._programmer_frame.online_fw_button_enable(
                    self.network_error)
                self._programmer_frame.online_fw_button_set_str_default()
                self._programmer_frame.online_fw_button_show()

                self._programmer_frame.local_fw_button_enable()
                self._programmer_frame.local_fw_button_set_str_default()

                self._programmer_frame.update_button_set_text_update("VTX")
                # self._programmer_frame.update_button_disable()

                self._statusbar_frame.progress_bar_set_value(100)
                self._programmer_frame.deselect()
                """
            elif my_ch341.status == ch341_status.VTX_UPDATE_FAILED.value:  # vtx update failed
                self._statusbar_frame.progress_bar_set_value(0)
                self._statusbar_frame.status_label_set_text(
                    "Firmware updated failed. Disconnect/reconnect the vtx to try again, or click cancel to finish.", "red")
                my_ch341.status = ch341_status.VTX_RECONNECT.value
                self._programmer_frame.update_button_set_text_cancel()
                self._programmer_frame.update_button_enable()

            elif my_ch341.status == ch341_status.VTX_RECONNECTDONE.value:
                my_ch341.status = ch341_status.VTX_UPDATE.value
                self._programmer_frame.update_button_set_text_update("VTX")
                self._programmer_frame.update_button_disable()
                self._statusbar_frame.label_hidden()

            elif my_ch341.status == ch341_status.VTX_FW_ERROR.value:  # vtx fw error
                my_ch341.status = ch341_status.IDLE.value

                self.notebook_enable()

                self._vtx_frame.radio_button_enable()

                self._programmer_frame.version_combobox_enable()
                self._programmer_frame.online_fw_button_enable(
                    self.network_error)
                self._programmer_frame.version_combobox_set_default()
                self._programmer_frame.local_fw_button_enable()
                self._programmer_frame.local_fw_button_set_str_default()
                self._programmer_frame.update_button_set_text_update("VTX")
                # self._programmer_frame.update_button_disable()
                self._programmer_frame.deselect()

                self._statusbar_frame.progress_bar_set_value(0)
                self._statusbar_frame.status_label_set_text(
                    "Firmware update failed. Firmware error", "red")

        # ------------ Monitor ---------------
        if self.current_selected_tab() == 1:
            # download
            if my_download.status == download_status.DOWNLOAD_MONITOR_FW_DONE.value:
                my_download.status = download_status.IDLE.value
                my_ch341.fw_path = my_download.save_path
                my_ch341.written_len = 0
                my_ch341.to_write_len = os.path.getsize(my_ch341.fw_path)

                self._statusbar_frame.label_hidden()
                self._programmer_frame.update_button_set_text_update(
                    "Monitor")
                self._programmer_frame.update_button_disable()
                my_ch341.status = ch341_status.MONITOR_UPDATE.value
            elif my_download.status == download_status.DOWNLOAD_MONITOR_FW_FAILED.value:
                my_download.status = download_status.IDLE.value
                self.is_update_monitor = 0
                my_ch341.monitor_connected = 0
                my_ch341.status = ch341_status.MONITOR_CHECK_ALIVE.value

                self.notebook_enable()

                self._programmer_frame.version_combobox_enable()
                self._programmer_frame.online_fw_button_enable(
                    self.network_error)
                self._programmer_frame.version_combobox_set_default()
                self._programmer_frame.local_fw_button_enable()
                self._programmer_frame.local_fw_button_set_str_default()
                self._programmer_frame.update_button_set_text_update(
                    "Monitor")
                # self._programmer_frame.update_button_disable()
                self._programmer_frame.deselect()

                self._statusbar_frame.progress_bar_set_value(0)
                self._statusbar_frame.status_label_set_text(
                    "Firmware update failed. Network error.", "red")

            # update
            if self.is_update_monitor == 1:
                if my_ch341.status == ch341_status.IDLE.value and my_ch341.monitor_connected == 0:  # to connect Monitor
                    my_ch341.status = ch341_status.MONITOR_CHECK_ALIVE.value
                elif my_ch341.status == ch341_status.MONITOR_CHECK_ALIVE.value and my_ch341.monitor_connected == 1:  # Monitor is connected
                    my_ch341.status = ch341_status.IDLE.value
                    if self._programmer_frame.mode == 0:
                        my_download.url = self._programmer_frame.url
                        my_download.save_path = "resource/FW"
                        my_download.status = download_status.DOWNLOAD_MONITOR_FW.value  # download url
                        self._statusbar_frame.status_label_set_text(
                            "Downloading Firmware ...", "SystemButtonFace")
                    else:
                        my_ch341.written_len = 0
                        my_ch341.to_write_len = os.path.getsize(
                            my_ch341.fw_path)
                        self._statusbar_frame.label_hidden()
                        self._programmer_frame.update_button_set_text_update(
                            "Monitor")
                        self._programmer_frame.update_button_disable()
                        my_ch341.status = ch341_status.MONITOR_UPDATE.value

                elif my_ch341.status == ch341_status.MONITOR_UPDATE.value:  # refresh progress bar
                    value = (my_ch341.written_len /
                             my_ch341.to_write_len * 100) % 101
                    self._statusbar_frame.progress_bar_set_value(value)

                elif my_ch341.status == ch341_status.MONITOR_UPDATEDONE.value:  # Monitor update done
                    self.is_update_monitor = 0
                    my_ch341.monitor_connected = 0
                    my_ch341.status = ch341_status.MONITOR_CHECK_ALIVE.value

                    self.notebook_enable()

                    self._programmer_frame.update_button_set_text_update(
                        "Monitor")
                    self._programmer_frame.update_button_enable()
                    self._programmer_frame.version_combobox_enable()
                    self._programmer_frame.local_fw_button_enable()
                    self._programmer_frame.online_fw_button_enable(
                        self.network_error)

                    self._statusbar_frame.progress_bar_set_value(100)
                    self._statusbar_frame.status_label_set_text(
                        "Firmware updated.", "#06b025")

                elif my_ch341.status == ch341_status.MONITOR_FW_ERROR.value:  # fw error
                    self.is_update_monitor = 0
                    my_ch341.monitor_connected = 0
                    my_ch341.status = ch341_status.MONITOR_CHECK_ALIVE.value

                    self.notebook_enable()

                    self._programmer_frame.update_button_set_text_update(
                        "Monitor")
                    self._programmer_frame.update_button_enable()
                    self._programmer_frame.version_combobox_enable()
                    self._programmer_frame.local_fw_button_enable()
                    self._programmer_frame.online_fw_button_enable(
                        self.network_error)

                    self._statusbar_frame.progress_bar_set_value(0)
                    self._statusbar_frame.status_label_set_text(
                        "Firmware udpate failed. Firmware error.", "red")

            elif my_ch341.status == ch341_status.MONITOR_CHECK_ALIVE.value:
                if self.monitor_is_alive == 0 and my_ch341.monitor_connected == 1:  # to connect monitor
                    self._monitor_frame.setting_enable()

                    self._programmer_frame.version_combobox_enable()
                    self._programmer_frame.online_fw_button_enable(
                        self.network_error)
                    self._programmer_frame.local_fw_button_enable()
                    self._programmer_frame.local_fw_button_set_str_default()
                    # self._programmer_frame.update_button_disable()

                    self._monitor_frame.write_setting(global_var.brightness, global_var.contrast, global_var.saturation,
                                                      global_var.backlight, global_var.cell_count, global_var.warning_cell_voltage, global_var.osd)
                    self.monitor_is_alive = 1
                elif self.monitor_is_alive == 1 and my_ch341.monitor_connected == 0:  # to disconnect monitor
                    self.monitor_is_alive = 0

                    self._monitor_frame.reset_scale()
                    self._monitor_frame.setting_disable()

                    self._programmer_frame.version_combobox_enable()
                    self._programmer_frame.online_fw_button_enable(
                        self.network_error)
                    self._programmer_frame.local_fw_button_enable()
                    self._programmer_frame.local_fw_button_set_str_default()
                    # self._programmer_frame.update_button_disable()

                elif self.monitor_is_alive == 1 and my_ch341.monitor_connected == 1:  # monitor is alive
                    # settting
                    self._monitor_frame.usb_heart()

        # --------------------- event_vrx -------------------------------
        if self.current_selected_tab() == 2:
            # download
            if my_download.status == download_status.DOWNLOAD_EVENT_VRX_FW_DONE.value:
                my_download.status = download_status.IDLE.value
                my_ch341.fw_path = my_download.save_path
                my_ch341.written_len = 0
                my_ch341.to_write_len = os.path.getsize(my_ch341.fw_path)

                self._statusbar_frame.label_hidden()
                self._programmer_frame.update_button_set_text_update(
                    "Event VRX")
                self._programmer_frame.update_button_disable()
                my_ch341.status = ch341_status.EVENT_VRX_UPDATE.value
            elif my_download.status == download_status.DOWNLOAD_EVENT_VRX_FW_FAILED.value:
                my_download.status = download_status.IDLE.value
                my_ch341.status = ch341_status.IDLE.value

                self.notebook_enable()

                self._programmer_frame.version_combobox_enable()
                self._programmer_frame.online_fw_button_enable(
                    self.network_error)
                self._programmer_frame.version_combobox_set_default()
                self._programmer_frame.local_fw_button_enable()
                self._programmer_frame.local_fw_button_set_str_default()
                self._programmer_frame.update_button_set_text_update(
                    "Event VRX")
                # self._programmer_frame.update_button_disable()
                self._programmer_frame.deselect()

                self._statusbar_frame.progress_bar_set_value(0)
                self._statusbar_frame.status_label_set_text(
                    "Firmware update failed. Network error", "red")

            # update
            if my_ch341.status == ch341_status.EVENT_VRX_CONNECTED.value:  # event_vrx is connected
                my_ch341.status = ch341_status.IDLE.value
                if self._programmer_frame.mode == 0:
                    my_download.url = self._programmer_frame.url
                    my_download.save_path = "resource/FW"
                    my_download.status = download_status.DOWNLOAD_EVENT_VRX_FW.value  # download url
                    self._statusbar_frame.status_label_set_text(
                        "Downloading Firmware ...", "SystemButtonFace")
                else:
                    my_ch341.written_len = 0
                    my_ch341.to_write_len = os.path.getsize(my_ch341.fw_path)
                    self._programmer_frame.update_button_set_text_update(
                        "Event VRX")
                    self._programmer_frame.update_button_disable()
                    self._statusbar_frame.label_hidden()
                    my_ch341.status = ch341_status.EVENT_VRX_UPDATE.value

            elif my_ch341.status == ch341_status.EVENT_VRX_UPDATE.value:  # event_vrx refresh progress bar
                value = (my_ch341.written_len /
                         my_ch341.to_write_len * 100) % 101
                self._statusbar_frame.progress_bar_set_value(value)

            elif my_ch341.status == ch341_status.EVENT_VRX_UPDATEDONE.value:  # event_vrx update done
                my_ch341.status = ch341_status.IDLE.value

                self.notebook_enable()

                self._programmer_frame.update_button_set_text_update(
                    "Event VRX")
                self._programmer_frame.update_button_enable()
                self._programmer_frame.version_combobox_enable()
                self._programmer_frame.local_fw_button_enable()
                self._programmer_frame.online_fw_button_enable(
                    self.network_error)

                self._statusbar_frame.progress_bar_set_value(100)
                self._statusbar_frame.status_label_set_text(
                    "Firmware updated.", "#06b025")

            elif my_ch341.status == ch341_status.EVENT_VRX_FW_ERROR.value:
                my_ch341.status = ch341_status.IDLE.value

                self.notebook_enable()

                self._programmer_frame.update_button_set_text_update(
                    "Event VRX")
                self._programmer_frame.update_button_enable()
                self._programmer_frame.version_combobox_enable()
                self._programmer_frame.local_fw_button_enable()
                self._programmer_frame.online_fw_button_enable(
                    self.network_error)

                self._statusbar_frame.progress_bar_set_value(0)
                self._statusbar_frame.status_label_set_text(
                    "Fiwamre update failed. Firmware error", "red")

        self._main_window.after(100, self.refresh)


def on_closing():
    my_download.status = download_status.DOWNLOAD_EXIT.value
    my_ch341.status = ch341_status.STATUS_EXIT.value
    sys.exit()


global my_gui


def main_window_ui():
    global my_gui
    root = tk.Tk()

    my_gui = MyGUI(root)
    my_gui.refresh()

    if my_gui.downloading_window_status == 0:
        my_gui._main_window.after(
            100, my_gui.create_downloading_firmware_window)

    root.protocol("WM_DELETE_WINDOW", on_closing)

    my_gui._main_window.mainloop()
