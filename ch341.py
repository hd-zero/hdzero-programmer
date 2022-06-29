import os
import time
from ctypes import *

def ch341LoadDLL():
    ch341dllPath = './dll/CH341DLL.DLL'
    ch341 = windll.LoadLibrary(ch341dllPath)
    return ch341
def ch341ThreadProc():
    ch341 = ch341LoadDLL()
    print('start ch341ThreadProc')
    print(ch341)
    