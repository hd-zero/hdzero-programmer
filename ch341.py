import os
import time
from ctypes import *

class CH341(object):
    ch341dll = None
    IsConnected = 0

    def __init__(self):
        ch341dllPath = './dll/CH341DLL.DLL'
        super(CH341,self).__init__()
        try:
            self.ch341dll = cdll.LoadLibrary(ch341dllPath)
        except:
            print("Error: Can't find"+ch341dllPath)
    
    def OpenDevice(self, iIndex):
        return self.ch341dll.CH341OpenDevice(iIndex);

    def CloseDevice(self, iIndex):
        self.ch341dll.CH341CloseDevice(iIndex);

    def GetVersion(self):
        return self.ch341dll.CH341GetVersion();

    def GetDrvVersion(self):
        return self.ch341dll.CH341GetDrvVersion();

    # def GetDeviceDescr(self,iIndex):
    #     self.ch341dll.CH341GetDeviceDescr(iIndex, self.oBuffer_P, self.ioLength);

def ch341ThreadProc():
    print('start ch341ThreadProc')
    ch341 = CH341()
    print('ch341GetVersion: %d' %ch341.GetVersion())
    print('ch341GetDrvVersion: %d' %ch341.GetDrvVersion())
    
    while True:

        # wait ch341 connect to PC
        while ch341.IsConnected==0:    
            if ch341.OpenDevice(0) > 0:
                ch341.IsConnected = 1
                print("DBG: ch341 is connected")
            time.sleep(0.01)
        
        # get device description
        # ch341.GetDeviceDescr(0)
        # print(ch341.ioLength)
        # print(ch341.oBuffer)

        
