import tkinter as tk
from tkinter import ttk
import ctypes
import global_var


class frame_monitor:
    def __init__(self, parent):
        self._parent = parent
        self._frame = tk.Frame(parent)
        parent.add(self._frame, text="Monitor")

        self.dll_name = "CH341DLL.DLL"
        self.color_background = "#303030"
        self.color_label = "white"

        self.heart_cnt = 0
        self.addr_usb_heart = 0x13
        self.addr_usb_write_fpga_device = 0x65  # 7bit address
        self.addr_usb_write_brightness = 0x14
        self.addr_usb_write_contrast = 0x15
        self.addr_usb_write_saturation = 0x16
        self.addr_usb_write_backlight = 0x17
        self.addr_usb_write_cell_count = 0x18
        self.addr_usb_write_warning_cell_voltage = 0x19
        self.addr_usb_write_osd = 0x1A

        self.brightness_min = 0
        self.brightness_max = 254
        self.brightness_default = 136
        self.contrast_min = 0
        self.contrast_max = 254
        self.contrast_default = 86
        self.saturation_min = 0
        self.saturation_max = 254
        self.saturation_default = 143
        self.backlight_min = 1
        self.backlight_max = 100
        self.backlight_default = 80
        self.cell_count_min = 1     # 1 auto
        self.cell_count_max = 5
        self.cell_count_default = 1
        self.warning_cell_voltage_min = 28
        self.warning_cell_voltage_max = 42
        self.warning_cell_voltage_default = 28
        self.osd_min = 0
        self.osd_max = 1
        self.osd_default = 1

        self.brightness_scale = 0
        self.contrast_scale = 0
        self.saturation_scale = 0
        self.backlight_scale = 0
        self.cell_count_scale = 0
        self.warning_cell_voltage_scale = 0
        self.osd_checkbutton = 0
        self.reset_button = 0

        self.osd_var = tk.BooleanVar()

        self._frame.grid_rowconfigure(0, weight=1)
        self._frame.grid_rowconfigure(1, weight=1)
        self._frame.grid_rowconfigure(2, weight=1)
        self._frame.grid_rowconfigure(3, weight=1)
        self._frame.grid_rowconfigure(4, weight=1)
        self._frame.grid_rowconfigure(5, weight=1)
        self._frame.grid_rowconfigure(6, weight=1)

        self._frame.grid_columnconfigure(0, weight=0)
        self._frame.grid_columnconfigure(1, weight=0)
        self._frame.grid_columnconfigure(2, weight=0)

        self.init_image_setting()
        self.init_power_setting()
        self.init_osd_setting()
        self.init_reset_button()

        try:
            self.dll = ctypes.WinDLL(self.dll_name)
        except:
            print("Please check ch341 driver")

    def usb_heart(self):
        self.heart_cnt += 1
        if self.heart_cnt == 255:
            self.heart_cnt = 0
        self.write_i2c(self.addr_usb_heart, self.heart_cnt)

    def write_i2c(self, addr, byte):
        self.dll.CH341WriteI2C(0, self.addr_usb_write_fpga_device, addr, byte)

    def write_brightness(self, b):
        global_var.brightness = b
        self.write_i2c(self.addr_usb_write_brightness, b)
        # print(f"write_brightness {b}")

    def write_contrast(self, c):
        global_var.contrast = c
        self.write_i2c(self.addr_usb_write_contrast, c)
        # print(f"write_contrast {c}")

    def write_saturation(self, s):
        global_var.saturation = s
        self.write_i2c(self.addr_usb_write_saturation, s)
        # print(f"write_saturation {s}")

    def write_backlight(self, l):
        global_var.backlight = l
        self.write_i2c(self.addr_usb_write_backlight, l)
        # print(f"write_backlight {l}")

    def write_cell_count(self, cell):
        global_var.cell_count = cell
        self.write_i2c(self.addr_usb_write_cell_count, cell)
        # print(f"write_cell_count {cell}")

    def write_warning_cell_voltage(self, warning_cell):
        global_var.warning_cell_voltage = warning_cell
        self.write_i2c(self.addr_usb_write_warning_cell_voltage, warning_cell)
        # print(f"write_warning_cell_voltage {warning_cell}")

    def write_osd(self, osd):
        global_var.osd = osd
        self.write_i2c(self.addr_usb_write_osd, osd)

    def write_setting(self, b, c, s, l, cell, warning_cell, osd):
        """write setting from vrx.
        usually used for sync vrx setting.
        NOTE: Must run after setting_enable
        """
        if b < self.brightness_min or b > self.brightness_max:
            b = self.brightness_default
        if c < self.contrast_min or c > self.contrast_max:
            c = self.contrast_default
        if s < self.saturation_min or s > self.saturation_max:
            s = self.saturation_default
        if l < self.backlight_min or l > self.backlight_max:
            l = self.backlight_default
        if cell < self.cell_count_min or cell > self.cell_count_max:
            cell = self.cell_count_default
        if warning_cell < self.warning_cell_voltage_min or warning_cell > self.warning_cell_voltage_max:
            warning_cell = self.warning_cell_voltage_default

        if osd < self.osd_min or osd > self.osd_max:
            osd = self.osd_default

        self.write_brightness(b)
        self.write_contrast(c)
        self.write_saturation(s)
        self.write_backlight(l)
        self.write_cell_count(cell)
        self.write_warning_cell_voltage(warning_cell)
        self.write_osd(osd)

        # update scale
        self.brightness_scale.set(b)
        self.contrast_scale.set(c)
        self.saturation_scale.set(s)
        self.backlight_scale.set(l)
        self.cell_count_scale.set(cell)
        self.warning_cell_voltage_scale.set(warning_cell)

        if osd == 1:
            self.osd_var.set(True)
        else:
            self.osd_var.set(False)

        # update label
        self.brightness_label.config(text=f'{b}')
        self.contrast_label.config(text=f'{c}')
        self.saturation_label.config(text=f'{s}')
        self.backlight_label.config(text=f'{l}')

        option = ["Auto", "2S", "3S", "4S", "5S"]
        self.cell_count_label.config(text=option[cell-1])
        self.warning_cell_voltage_label.config(text=f"{warning_cell/10}")

    def setting_disable(self):
        self.brightness_scale.configure(state="disabled")
        self.contrast_scale.configure(state="disabled")
        self.saturation_scale.configure(state="disabled")
        self.backlight_scale.configure(state="disabled")
        self.cell_count_scale.configure(state="disabled")
        self.warning_cell_voltage_scale.configure(state="disabled")
        self.osd_checkbutton.configure(state="disabled")

    def setting_enable(self):
        self.brightness_scale.configure(state="normal")
        self.contrast_scale.configure(state="normal")
        self.saturation_scale.configure(state="normal")
        self.backlight_scale.configure(state="normal")
        self.cell_count_scale.configure(state="normal")
        self.warning_cell_voltage_scale.configure(state="normal")
        self.osd_checkbutton.configure(state="normal")

    def reset_scale(self):
        self.brightness_scale.set(self.brightness_min)
        self.contrast_scale.set(self.contrast_min)
        self.saturation_scale.set(self.saturation_min)
        self.backlight_scale.set(self.backlight_min)
        self.cell_count_scale.set(self.cell_count_min)
        self.warning_cell_voltage_scale.set(self.warning_cell_voltage_min)
        self.osd_var.set(False)

        self.brightness_label.config(text=f"{int(float(self.brightness_min))}")
        self.brightness_label.config(text=f"{int(float(self.contrast_min))}")
        self.saturation_label.config(text=f"{int(float(self.saturation_min))}")
        self.backlight_label.config(text=f"{int(float(self.brightness_min))}")

        self.on_cell_count_scale_changed(self.cell_count_min)
        self.on_warning_cell_voltage_scale_changed(
            self.warning_cell_voltage_min)
        self.osd_var.set(False)
        self.on_osd_checkoutbutton_changed()

    def frame(self):
        return self._frame

    def on_brightness_scale_changed(self, value):
        self.brightness_label.config(text=f"{int(float(value))}")
        self.write_brightness(int(float(value)))

    def on_contrast_scale_changed(self, value):
        self.contrast_label.config(text=f"{int(float(value))}")
        self.write_contrast(int(float(value)))

    def on_saturation_scale_changed(self, value):
        self.saturation_label.config(text=f"{int(float(value))}")
        self.write_saturation(int(float(value)))

    def on_backlight_scale_changed(self, value):
        self.backlight_label.config(text=f"{int(float(value))}")
        self.write_backlight(int(float(value)))

    def on_cell_count_scale_changed(self, value):
        option = ["Auto", "2S", "3S", "4S", "5S"]
        self.cell_count = int(float(value))
        self.cell_count_label.config(text=option[self.cell_count-1])
        self.write_cell_count(int(float(value)))

    def on_warning_cell_voltage_scale_changed(self, value):
        self.warning_cell_voltage = int(float(value))
        self.warning_cell_voltage_label.config(
            text=f"{self.warning_cell_voltage/10}")
        self.write_warning_cell_voltage(int(float(value)))

    def on_osd_checkoutbutton_changed(self):
        if self.osd_var.get() == True:
            self.write_osd(1)
        else:
            self.write_osd(0)
            
    def on_reset_button_press(self):
        self.brightness_scale.set(self.brightness_default)
        self.contrast_scale.set(self.contrast_default)
        self.saturation_scale.set(self.saturation_default)
        self.backlight_scale.set(self.backlight_default)
        self.cell_count_scale.set(self.cell_count_default)
        self.warning_cell_voltage_scale.set(self.warning_cell_voltage_default)
        self.osd_var.set(True)

        self.brightness_label.config(text=f"{int(float(self.brightness_default))}")
        self.brightness_label.config(text=f"{int(float(self.contrast_default))}")
        self.saturation_label.config(text=f"{int(float(self.saturation_default))}")
        self.backlight_label.config(text=f"{int(float(self.backlight_default))}")

        self.on_cell_count_scale_changed(self.cell_count_default)
        self.on_warning_cell_voltage_scale_changed(
            self.warning_cell_voltage_default)
        self.osd_var.set(True)
        self.on_osd_checkoutbutton_changed()

    def init_image_setting(self):
        # brighrness
        row = 0
        label = ttk.Label(self._frame, text="Brightness")
        label.grid(row=row, column=0, sticky="w", padx=20)

        self.brightness_scale = ttk.Scale(self._frame, from_=self.brightness_min, to=self.brightness_max, orient="horizontal",
                                          length=350, command=self.on_brightness_scale_changed)
        self.brightness_scale.grid(row=row, column=1, sticky="w", padx=20)

        self.brightness_label = ttk.Label(self._frame, text="0")
        self.brightness_label.grid(row=row, column=2, sticky="w", padx=10)

        # contrast
        row += 1
        label = ttk.Label(self._frame, text="Contrast")
        label.grid(row=row, column=0, sticky="w", padx=20)

        self.contrast_scale = ttk.Scale(self._frame, from_=self.contrast_min, to=self.contrast_max, orient="horizontal",
                                        length=350, command=self.on_contrast_scale_changed)
        self.contrast_scale.grid(row=row, column=1, sticky="w", padx=20)

        self.contrast_label = ttk.Label(self._frame, text="0")
        self.contrast_label.grid(row=row, column=2, sticky="w", padx=10)

        # saturation
        row += 1
        label = ttk.Label(self._frame, text="Saturation")
        label.grid(row=row, column=0, sticky="w", padx=20)

        self.saturation_scale = ttk.Scale(self._frame, from_=self.saturation_min, to=self.saturation_max, orient="horizontal",
                                          length=350, command=self.on_saturation_scale_changed)
        self.saturation_scale.grid(row=row, column=1, sticky="w", padx=20)

        self.saturation_label = ttk.Label(self._frame, text="0")
        self.saturation_label.grid(row=row, column=2, sticky="w", padx=10)

        # Backlight
        row += 1
        label = ttk.Label(self._frame, text="Backlight")
        label.grid(row=row, column=0, sticky="w", padx=20)

        self.backlight_scale = ttk.Scale(self._frame, from_=self.backlight_min, to=self.backlight_max, orient="horizontal",
                                         length=350, command=self.on_backlight_scale_changed)
        self.backlight_scale.grid(row=row, column=1, sticky="w", padx=20)

        self.backlight_label = ttk.Label(self._frame, text="0")
        self.backlight_label.grid(row=row, column=2, sticky="w", padx=10)

    def init_power_setting(self):
        row = 4
        label = ttk.Label(self._frame, text="Cell Count")
        label.grid(row=row, column=0, sticky="w", padx=20)

        self.cell_count_scale = ttk.Scale(self._frame, from_=self.cell_count_min, to=self.cell_count_max, orient="horizontal",
                                          length=350, command=self.on_cell_count_scale_changed)
        self.cell_count_scale.grid(row=row, column=1, sticky="w", padx=20)

        self.cell_count_label = ttk.Label(self._frame, text="Auto")
        self.cell_count_label.grid(row=row, column=2, sticky="w", padx=10)

        row += 1
        label = ttk.Label(self._frame, text="Warning Cell Voltage")
        label.grid(row=row, column=0, sticky="w", padx=20)

        self.warning_cell_voltage_scale = ttk.Scale(self._frame, from_=self.warning_cell_voltage_min, to=self.warning_cell_voltage_max,
                                                    orient="horizontal", length=350, command=self.on_warning_cell_voltage_scale_changed)
        self.warning_cell_voltage_scale.grid(
            row=row, column=1, sticky="w", padx=20)

        self.warning_cell_voltage_label = ttk.Label(self._frame, text="2.8")
        self.warning_cell_voltage_label.grid(
            row=row, column=2, sticky="w", padx=10)

    def init_osd_setting(self):
        row = 6

        label = ttk.Label(self._frame, text="OSD")
        label.grid(row=row, column=0, sticky="w", padx=20)

        self.osd_checkbutton = ttk.Checkbutton(
            self._frame, variable=self.osd_var, text = "", command=self.on_osd_checkoutbutton_changed)
        self.osd_checkbutton.grid(row=row, column=0, sticky="w", padx=100)
        
    def init_reset_button(self):
        row = 6
        
        self.reset_button = tk.Button(self._frame, text="Reset all settings to default value", command=self.on_reset_button_press)
        self.reset_button.grid(row=row, column=1, sticky="w", padx=100)
