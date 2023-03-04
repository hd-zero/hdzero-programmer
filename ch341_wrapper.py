import os
import time
from ctypes import *
from flash import *

class ch341_class(object):

    def __init__(self):
        self.dll = None
        self.dev_connected = 0
        self.dll_path = './dll/CH341DLL.DLL'
        self.iobuffer = create_string_buffer(65544)
        self.ilength = 0
        self.iIndex = 0
        self.flash_connected = 0
        self.status = 0 # 0:idle
        try:
            self.dll = cdll.LoadLibrary(self.dll_path)
        except:
            print("Error: Can't find"+self.dll_path)

    def open_device(self, iIndex):
        return self.dll.CH341OpenDevice(iIndex)

    def close_device(self, iIndex):
        self.dll.CH341CloseDevice(iIndex)

    def get_version(self):
        return self.dll.CH341GetVersion()

    def get_driver_version(self):
        return self.dll.CH341GetDrvVersion()

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
            if self.open_device(0) > 0:
                self.dev_connected = 1
                print("DBG: ch341 is connected")
            #else:
            #    time.sleep(0.1)
        elif self.dev_connected == 1 and self.status == 0:
            if self.open_device(0) < 0:
                self.dev_connected = 0
                print("DBG: ch341 is disconnected")
                if self.flash_connected == 1:
                    self.flash_connected = 0
                    print("DBG: flash is disconnected")

def flash_read_id(ch341):
    ch341.iobuffer[0] = 0x90
    ch341.iobuffer[1] = 0x90
    ch341.iobuffer[2] = 0x90
    ch341.iobuffer[3] = 0x90
    ch341.iobuffer[4] = 0x90
    ch341.iobuffer[5] = 0x90
    ch341.ilength = 6

    ch341.set_stream(0)
    ch341.stream_spi4()
    ch341.set_stream(1)

    return int.from_bytes(ch341.iobuffer[4], byteorder='big') * 256 \
            + int.from_bytes(ch341.iobuffer[5], byteorder='big')


def flash_connect(ch341):
    if ch341.dev_connected == 0:
        ch341.flash_connected = 0
        return;
    else:
        if ch341.flash_connected == 0:
            flash_id = flash_read_id(ch341)
            if flash_id == 0xEF13:
                print("DBG: flash is connected")
                ch341.flash_connected = 1
                return
            else:
                time.sleep(0.5)
        elif ch341.flash_connected == 1:
            if ch341.status == 0:
                flash_id = flash_read_id(ch341)
                if flash_id == 0xEF13:
                    return
                else:
                    print("DBG: flash is disconnected")
                    ch341.flash_connected = 0

ch341 = ch341_class()
def ch341ThreadProc():
    print('start ch341ThreadProc')

    while True:
        ch341.dev_connect()
        flash_connect(ch341)

        time.sleep(0.1)
