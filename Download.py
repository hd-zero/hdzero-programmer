import os
import time
import wget
import shutil
import json
import requests
import sys

LocalRootPath = './Data/Github/'
LocaLFirmwarePath = LocalRootPath+'firmware/'
LocalTargetInfoPath = LocalRootPath+'Target_Info/'
LocaLTempPath = './Data/Temp/'
LocalTargetListString = LocalRootPath + 'TargetList'
LocalHDZeroString = LocalRootPath + 'HDZero.png'

WebRootPath = 'https://raw.githubusercontent.com/ligenxxxx/HDZeroFirmware/main/'
WebTargetListString = WebRootPath + 'TargetList'
WebHDZeroString = WebRootPath + 'HDZero.png'


downloadLink = ""
localTemp = ""
downloadCommand = 0
firmware_link_list = {}
version_list = ["Choose a Version"]
vtx_name_list = [["Choose a VTX"]]
vtx_id_list = {}
user_vtx_id = 0xff
success = 0


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


def DownloadOnlineFile(OnlinePath, LocalPath):
    try:
        # print('\nDBG:', 'Downloading ' + OnlinePath)
        if 0:
            fname = wget.download(url=OnlinePath, out=LocalPath)
        else:
            respose = requests.get(OnlinePath, timeout=10)
            with open(LocalPath, "wb") as f:
                f.write(respose.content)
        return 1

    except:
        # print('\r\nDBG:Download Failed. Please check if the network is connected.')
        return 0


def ParseReleaseInfo():
    try:
        with open('./Data/Github/releases.json') as f:
            data = json.load(f)
        # print()
        for i in range(len(data)):
            # parser version number
            version_list.append(data[i]['tag_name'])
            firmware_link_list.update({data[i]['tag_name']: {}})

            # parser firmware link and target name
            link_list = []
            name_list = []
            name_list.append("Choose a VTX")
            for j in range(len(data[i]['assets'])):
                link_list.append(data[i]['assets'][j]['browser_download_url'])
                name_start = link_list[j].rfind('/') + len('/')
                name_end = link_list[j].index(".zip", name_start)
                name_list.append(link_list[j][name_start:name_end])

            for j in range(1, len(name_list)):
                firmware_link_list[data[i]['tag_name']].update(
                    {name_list[j]: link_list[j - 1]})
            vtx_name_list.append(name_list)

    except:
        a = 1
        # print()
        # print("something error")


def ParseCommonInfo():
    try:
        with open("./Data/Github/common", 'r') as file:
            lines = file.readlines()
            start = 0
            id_list = []
            for i in range(len(lines)):
                if start == 1:
                    words = lines[i].split()
                    for j in range(len(words)):
                        if words[j] == "defined":
                            vtx_name_list[0].append(words[j+1].lower())
                        if words[j] == "VTX_ID":
                            if words[j+1] != "0x00":
                                word = words[j+1].strip("0x")
                                id_list.append(int(words[j+1].strip("0x"), 16))
                if lines[i] == "/* define VTX ID start */\n":
                    start = 1
                elif lines[i] == "/* define VTX ID end */\n":
                    start = 0

            for i in range(1, len(vtx_name_list[0])):
                vtx_id_list.update({vtx_name_list[0][i]: id_list[i-1]})
            vtx_name_list[0][1:] = sorted(vtx_name_list[0][1:])
    except:
        a = 1
        # print("Cant't find common")


def DownloadReleases():
    ret = 0
    DetectLocalPath()
    if DownloadOnlineFile("https://api.github.com/repos/hd-zero/hdzero-vtx/releases", "./Data/Temp/releases.json") == 1:
        shutil.copy2("./Data/Temp/releases.json",
                     "./Data/Github/releases.json")
        ret = 1
    if os.path.exists("./Data/Temp/releases.json"):
        os.remove("./Data/Temp/releases.json")
    return ret


def DownloadCommon():
    ret = 0
    DetectLocalPath()
    if DownloadOnlineFile("https://raw.githubusercontent.com/hd-zero/hdzero-vtx/main/src/common.h", "./Data/Temp/common") == 1:
        shutil.copy2("./Data/Temp/common",
                     "./Data/Github/common")
        ret = 1
    if os.path.exists("./Data/Temp/common"):
        os.remove("./Data/Temp/common")
    return ret


def DownloadThreadProc():
    global downloadCommand
    global firmware_link_list
    global version_list
    global vtx_name_list
    global vtx_id_list
    global user_vtx_id
    global success

    ParseReleaseInfo()
    ParseCommonInfo()
    while True:
        if downloadCommand == 1:
            if DownloadReleases() and DownloadCommon():
                firmware_link_list = {}
                version_list = ["Choose a Version"]
                vtx_name_list = [["Choose a VTX"]]
                vtx_id_list = {}
                user_vtx_id = 0xff
                ParseReleaseInfo()
                ParseCommonInfo()
                success = 1
            else:
                success = 0
            downloadCommand = 0
        elif downloadCommand == 2:
            if os.path.exists(localTemp):
                os.remove(localTemp)
            if DownloadOnlineFile(downloadLink, localTemp):
                success = 1
            else:
                success = 0
            downloadCommand = 0
        elif downloadCommand == 255:
            sys.exit()
        time.sleep(0.01)
