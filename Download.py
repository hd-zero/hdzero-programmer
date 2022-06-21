import os
import time
import wget
import shutil

LocalRootPath = './Data/Github/'
LocaLFirmwarePath = LocalRootPath+'firmware/'
LocaLTempPath = './Data/Temp/'
LocalTargetListString = LocalRootPath + 'TargetList'

WebRootPath = 'https://raw.githubusercontent.com/ligenxxxx/HDZeroFirmware/main/'
WebTargetListString = WebRootPath + 'TargetList'

downloadCommand = 0
targetTypeNum = 0


def DetectLocalPath():
    if not os.path.exists(LocalRootPath):
        os.makedirs(LocalRootPath)
    if not os.path.exists(LocaLFirmwarePath):
        os.makedirs(LocaLFirmwarePath)
    if not os.path.exists(LocaLTempPath):
        os.makedirs(LocaLTempPath)
    if not os.path.exists(LocalTargetListString):
        f = open(LocalTargetListString,"w")
        f.write("0")
        f.close()
    else:
        ParseTargetList()

def DownloadTargetList():
    print('\r\nDBG:Downloading TargetList from Github.com.')
    try:
        wget.download(url=WebTargetListString, out=LocaLTempPath)
        if os.path.exists(LocalTargetListString):
            os.remove(LocalTargetListString)
        print('\r\nDBG:Done.')
        shutil.move(LocaLTempPath+'TargetList', LocalTargetListString)

    except:
        print('\r\nDBG:Download Failed. Please check if the network is connected.')

def ParseTargetList():
    global ParseTargetList
    f = open(LocalTargetListString, "r")
    line = f.readline()
    targetTypeNum = int(line)
    print('DBG:targetTypeNum:%d' % targetTypeNum)


def LoadGithubFirmware():
    DownloadTargetList()
    ParseTargetList()


def LoadGithubFirmwareRequest():
    global downloadCommand
    downloadCommand = 1


def DownloadThreadProc():
    global downloadCommand
    DetectLocalPath()
    while True:
        if downloadCommand == 1:
            LoadGithubFirmware()
            downloadCommand = 0
        time.sleep(0.1)
