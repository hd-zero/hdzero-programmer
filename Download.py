import os
import time
import wget
import shutil
import json

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
target_List = []
firmware_link_list = []
version_list = ["Choose a Version"]
vtx_name_list = [["Choose a VTX"]]


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
    # else:
    #     ParseTargetList()


def DownloadTargetList():
    print('\r\nDBG:Downloading TargetList...')
    try:
        wget.download(url=WebTargetListString, out=LocaLTempPath)
        if os.path.exists(LocalTargetListString):
            os.remove(LocalTargetListString)
        shutil.move(LocaLTempPath+'TargetList', LocalTargetListString)

    except:
        print('\r\nDBG:Download Failed. Please check if the network is connected.')

    # print('\r\nDBG:Downloading HDZero.png...')
    # try:
    #     wget.download(url=WebHDZeroString, out=LocaLTempPath)
    #     if os.path.exists(LocalHDZeroString):
    #         os.remove(LocalHDZeroString)
    #     shutil.move(LocaLTempPath+'HDZero.png', LocalHDZeroString)

    # except:
    #     print('\r\nDBG:Download Failed. Please check if the network is connected.')


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
    targetTypeList.insert(0, "Choose a VTX")
    print('DBG:', targetTypeList)
    f.close()

    return targetTypeList


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


def DownloadOnlineFile(OnlinePath, LocalPath):
    try:
        print('\nDBG:', 'Downloading ' + OnlinePath)
        fname = wget.download(url=OnlinePath, out=LocalPath)
        return 1

    except:
        print('\r\nDBG:Download Failed. Please check if the network is connected.')
        return 0


def ParseReleaseInfo():
    global version_list
    try:
        with open('./Data/Github/releases.json') as f:
            data = json.load(f)
        print()
        for i in range(len(data)):
            #parser version number
            version_list.append(data[i]['tag_name'])
            
            # parser firmware link and target name
            link_list = []
            name_list = []
            name_list.append("Choose a VTX")
            for j in range(len(data[i]['assets'])):
                link_list.append(data[i]['assets'][j]['browser_download_url'])
                name_start = link_list[j].rfind('/') + len('/')
                name_end = link_list[j].index(".zip", name_start)
                name_list.append(link_list[j][name_start:name_end])
            firmware_link_list.append(link_list)
            vtx_name_list.append(name_list)

    except:
        print()
        version_list.append("Choose a Version")
        print("something error")

    return version_list


def DownloadReleases():
    DetectLocalPath()
    DownloadTargetList()
    if DownloadOnlineFile("https://api.github.com/repos/hd-zero/hdzero-vtx/releases", "./Data/Temp/releases.json") == 1:
        # if DownloadOnlineFile("https://api.github.com/repos/hd-zero/hdzero-goggle/releases", "./Data/Temp/releases.json") == 1:
        # if DownloadOnlineFile("https://api.github.com/repos/betaflight/betaflight/releases", "./Data/Temp/releases.json") == 1:
        shutil.copy2("./Data/Temp/releases.json",
                     "./Data/Github/releases.json")

    if os.path.exists("./Data/Temp/releases.json"):
        os.remove("./Data/Temp/releases.json")


def LoadGithubFirmwareRequest():
    global downloadCommand
    downloadCommand = 1


def DownloadThreadProc():
    global downloadCommand
    while True:
        # if downloadCommand == 1:
        #     DetectLocalPath()
        #     LoadGithubFirmware()
        #     downloadCommand = 0
        time.sleep(0.1)
