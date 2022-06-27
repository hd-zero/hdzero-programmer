import os
import time
from ctypes import *

class USB():
    ch341dllPath = './dll/CH341DLL.LIB'
    ch341 = windll.LoadLibrary(ch341dllPath)
def ch341ThreadProc():
    print('start ch341ThreadProc')