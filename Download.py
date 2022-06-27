import os
import time
import wget
import shutil

LocalRootPath = './Data/Github/'
LocaLFirmwarePath = LocalRootPath+'firmware/'
LocalTargetInfoPath = LocalRootPath+'Target_Info/'
LocaLTempPath = './Data/Temp/'
LocalTargetListString = LocalRootPath + 'TargetList'
LocalHDZeroString = LocalRootPath + 'HDZero.png'

WebRootPath = 'https://raw.githubusercontent.com/ligenxxxx/HDZeroFirmware/main/'
WebTargetListString = WebRootPath + 'TargetList'
WebHDZeroString = WebRootPath + 'HDZero.png'

downloadCommand = 0
targetTypeNum = 0
targetTypeList = []


def DetectLocalPath():
    if not os.path.exists(LocalRootPath):
        os.makedirs(LocalRootPath)
    if not os.path.exists(LocaLFirmwarePath):
        os.makedirs(LocaLFirmwarePath)
    if not os.path.exists(LocaLTempPath):
        os.makedirs(LocaLTempPath)
    if not os.path.exists(LocalTargetInfoPath):
        os.makedirs(LocalTargetInfoPath)
    if not os.path.exists(LocalTargetListString):
        f = open(LocalTargetListString, "w")
        f.write("0")
        f.close()
    else:
        ParseTargetList()


def DownloadTargetList():
    print('\r\nDBG:Downloading TargetList...')
    try:
        wget.download(url=WebTargetListString, out=LocaLTempPath)
        if os.path.exists(LocalTargetListString):
            os.remove(LocalTargetListString)
        shutil.move(LocaLTempPath+'TargetList', LocalTargetListString)

    except:
        print('\r\nDBG:Download Failed. Please check if the network is connected.')

    print('\r\nDBG:Downloading HDZero.png...')
    try:
        wget.download(url=WebHDZeroString, out=LocaLTempPath)
        if os.path.exists(LocalHDZeroString):
            os.remove(LocalHDZeroString)
        shutil.move(LocaLTempPath+'HDZero.png', LocalHDZeroString)

    except:
        print('\r\nDBG:Download Failed. Please check if the network is connected.')

    


def ParseTargetList():
    global targetTypeNum
    global targetTypeList
    f = open(LocalTargetListString, "r")

    # parse targetTypeNum
    line = f.readline()
    targetTypeNum = int(line)
    print('\r\nDBG:targetTypeNum:%d' % targetTypeNum)

    # parse targetTypeList
    targetTypeList = f.read().splitlines()
    print('DBG:', targetTypeList)

    f.close()


def DownloadTargetPicture():
    print('DBG:', 'Downloading Target Picture...')
    for t in targetTypeList:
        webTargetPicturePath = WebRootPath + 'Target_Info/' + t + '/' + t + '.png'
        localTargetPicturePath = LocalRootPath + 'Target_Info/' + t + '/' + t + '.png'
        try:
            print('\nDBG:', 'Downloading '+t+'.png...')
            fname = wget.download(url=webTargetPicturePath, out=LocaLTempPath)
            if not os.path.exists(LocalRootPath + 'Target_Info/' + t + '/'):
                os.makedirs(LocalRootPath + 'Target_Info/' + t + '/')
            if os.path.exists(localTargetPicturePath):
                os.remove(localTargetPicturePath)
            shutil.move(LocaLTempPath+t + '.png', localTargetPicturePath)

        except:
            print('\r\nDBG:Download Failed. Please check if the network is connected.')
            return
    print()
    print('DBG:', 'Download Target Picture done.\r\n')


def LoadGithubFirmware():
    DownloadTargetList()
    ParseTargetList()
    DownloadTargetPicture()


def LoadGithubFirmwareRequest():
    global downloadCommand
    downloadCommand = 1


def DownloadThreadProc():
    global downloadCommand
    while True:
        if downloadCommand == 1:
            DetectLocalPath()
            LoadGithubFirmware()
            downloadCommand = 0
        time.sleep(0.1)
