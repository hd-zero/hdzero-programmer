import os
import sys
import time
from ctypes import *
from flash import *


class ch341_class_windows(object):

    def __init__(self):
        self.dll = None
        self.dev_connected = 0
        self.dll_path = './dll/windows/x64/CH341DLL.DLL'
        self.iobuffer = create_string_buffer(65544)
        self.ilength = 0
        self.iIndex = 0
        self.flash_connected = 0
        self.status = 0  # 0:idle
        self.command = 0
        self.vtx_id = 0
        self.fw_path = ""
        self.fw_full_size = 0
        self.fw_done_size = 0
        self.update_state = 0
        self.percent = 0
        self.write_crc = 0
        self.read_crc = 0
        self.success = 0

        try:
            self.dll = cdll.LoadLibrary(self.dll_path)
        except:
            a = 1  # print("Error: Can't find"+self.dll_path)

    def open_device(self):
        return self.dll.CH341OpenDevice(self.iIndex)

    def close_device(self):
        self.dll.CH341CloseDevice(self.iIndex)

    def get_version(self):
        return self.dll.CH341GetVersion()

    def get_driver_version(self):
        return self.dll.CH341GetDrvVersion()

    def get_chip_version(self):
        return self.dll.CH341GetVerIC(self.iIndex)

    def set_stream(self, cs):
        if cs == True:
            self.dll.CH341SetStream(self.iIndex, 0x80)
        else:
            self.dll.CH341SetStream(self.iIndex, 0x81)

    def stream_spi4(self):
        self.dll.CH341StreamSPI4(
            self.iIndex, 0x80, self.ilength, self.iobuffer)

    # def GetDeviceDescr(self,iIndex):
    #     self.dll.CH341GetDeviceDescr(iIndex, self.oBuffer_P, self.ioLength);
    def dev_connect(self):
        if self.dev_connected == 0:
            if self.open_device() > 0:
                self.dev_connected = 1
                # print("DBG: ch341 is connected")
            # else:
            #    time.sleep(0.1)
        elif self.dev_connected == 1 and self.status == 0:
            if self.get_chip_version() == 0:
                self.dev_connected = 0
                # print("DBG: ch341 is disconnected")
                if self.flash_connected == 1:
                    self.flash_connected = 0
                    # print("DBG: flash is disconnected")


class ch341_class_linux(object):

    def __init__(self):
        self.dll = None
        self.dev_connected = 0
        self.dll_path = './dll/linux/x64/libch347.so'
        self.iobuffer = create_string_buffer(65544)
        self.ilength = 0
        self.iIndex = 0
        self.flash_connected = 0
        self.status = 0  # 0:idle
        self.command = 0
        self.vtx_id = 0
        self.fw_path = ""
        self.fw_full_size = 0
        self.fw_done_size = 0
        self.update_state = 0
        self.percent = 0
        self.write_crc = 0
        self.read_crc = 0
        self.success = 0

        try:
            self.dll = cdll.LoadLibrary(self.dll_path)
        except:
            a = 1  # print("Error: Can't find"+self.dll_path)

    def open_device(self):
        self.iIndex = self.dll.CH34xOpenDevice("/dev/ch34x_pis0".encode())
        return self.iIndex

    def close_device(self):
        self.dll.CH34xCloseDevice(self.iIndex)

    def get_version(self):
        return self.dll.CH34xGetVersion()

    def get_driver_version(self):
        return self.dll.CH34xGetDrvVersion() 

    def get_chip_version(self):
        ver_str = create_string_buffer(1)
        self.dll.CH34x_GetChipVersion(self.iIndex, ver_str)
        return int.from_bytes(ver_str[0], byteorder='big')

    def set_stream(self, cs):
        if cs == True:
            self.dll.CH34xSetStream(self.iIndex, 0x80)
        else:
            self.dll.CH34xSetStream(self.iIndex, 0x81)

    def stream_spi4(self):
        self.dll.CH34xStreamSPI4(
            self.iIndex, 0x80, self.ilength, self.iobuffer)

    # def GetDeviceDescr(self,iIndex):
    #     self.dll.CH341GetDeviceDescr(iIndex, self.oBuffer_P, self.ioLength);
    def dev_connect(self):
        if self.dev_connected == 0:
            if self.open_device() > 0:
                self.dev_connected = 1
                # print("DBG: ch341 is connected")
            # else:
            #    time.sleep(0.1)
        elif self.dev_connected == 1 and self.status == 0:
            if self.get_chip_version() == 0:
                self.dev_connected = 0 
                # print("DBG: ch341 is disconnected")
                if self.flash_connected == 1:
                    self.flash_connected = 0
                    # print("DBG: flash is disconnected")



def flash_read_id(ch341):
    ch341.iobuffer[0] = 0x9f
    ch341.iobuffer[1] = 0x9f
    ch341.iobuffer[2] = 0x9f
    ch341.iobuffer[3] = 0x9f
    ch341.iobuffer[4] = 0x9f
    ch341.iobuffer[5] = 0x9f
    ch341.ilength = 6

    ch341.set_stream(0)
    ch341.stream_spi4()
    ch341.set_stream(1)

    return int.from_bytes(ch341.iobuffer[1], byteorder='big') * 256 * 256 \
        + int.from_bytes(ch341.iobuffer[2], byteorder='big') * 256 \
        + int.from_bytes(ch341.iobuffer[3], byteorder='big')


def flash_connect(ch341):
    if ch341.dev_connected == 0:
        ch341.flash_connected = 0
        return
    else:
        if ch341.flash_connected == 0:
            flash_id = flash_read_id(ch341)
            if flash_id == 0xEF4014 or flash_id == 0x5E6014:
                # print("DBG: flash is connected")
                ch341.flash_connected = 1
                return
            else:
                time.sleep(0.5)
        elif ch341.flash_connected == 1:
            if ch341.status == 0:
                flash_id = flash_read_id(ch341)
                if flash_id == 0xEF4014 or flash_id == 0x5E6014:
                    return
                else:
                    # print("DBG: flash is disconnected")
                    ch341.flash_connected = 0

if sys.platform.startswith('win'):
    ch341 = ch341_class_windows()
elif sys.platform.startswith('linux'):
    ch341 = ch341_class_linux()
else:
    ch341 = ch341_class_windows()


def ch341ThreadProc():
    # print('start ch341ThreadProc')

    while True:
        ch341.dev_connect()
        # flash_connect(ch341)  
        if ch341.command == 1:
            flash_read_vtx_id(ch341)
            ch341.vtx_id = int.from_bytes(ch341.iobuffer[4], byteorder='big')
            ch341.command = 0
        elif ch341.command == 2:
            ch341.success = 0
            ch341.fw_full_size = os.path.getsize(ch341.fw_path)
            ch341.fw_done_size = 0
            ch341.percent = 0
            ch341.update_state = 1
            flash_erase(ch341)
            ch341.update_state = 2
            flash_write_target(ch341, [ch341.vtx_id])
            flash_write_file(ch341)
            flash_read_file(ch341)
            ch341.update_state = 3
            if ch341.write_crc == ch341.read_crc:
                ch341.success = 1
            else:
                ch341.success = 0
            ch341.command = 0
        elif ch341.command == 255:
            sys.exit()
        else:
            ch341.update_state = 0

        time.sleep(0.1)
