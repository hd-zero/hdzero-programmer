import os
import time
from ctypes import *


class ch341_class(object):

    def __init__(self):
        self.dll = None
        self.connected = 0
        self.dll_path = './dll/CH341DLL.DLL'
        self.iobuffer = [0x00] * 65544
        self.ilength = 0
        self.iIndex = 0
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
        self.dll.CH341StreamSPI4(self.iIndex, 0x80, self.ilength, c_void_p(self.iobuffer))

    # def GetDeviceDescr(self,iIndex):
    #     self.dll.CH341GetDeviceDescr(iIndex, self.oBuffer_P, self.ioLength);
    def init(self):
        while self.connected == 0:
            for i in range(0 , 8):
                if self.open_device(i) > 0:
                    self.connected = 1
                    self.iIndex = i
                    print("DBG: ch341 is connected")
                time.sleep(0.1)


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
    
def ch341ThreadProc():
    print('start ch341ThreadProc')
    ch341 = ch341_class()

    while True:
        ch341.init()
        flash_read_id(ch341)
        time.sleep(1)

