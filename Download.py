import requests
import sys
import time
from global_var import *
import os
import zipfile


class download:
    def __init__(self):

        self.status = download_status.IDLE.value
        self.url = ""
        self.save_path = ""
        self.to_stop = 0

    def download_file(self, url, save_path, clear):
        print(f"Downloading {url}")
        if clear:
            if os.path.exists(save_path):
                os.remove(save_path)
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(save_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        if self.to_stop == 1:
                            self.to_stop = 0
                            return 2
                        if chunk:
                            file.write(chunk)
                if self.status == download_status.DOWNLOAD_EXIT.value:
                    sys.exit()
                return 1
            else:
                if self.status == download_status.DOWNLOAD_EXIT.value:
                    sys.exit()
                print("Failed to download file.")
                return 0
        except:
            return 0


my_download = download()


def download_thread_proc():
    my_download.download_file(
        "https://api.github.com/repos/hd-zero/hdzero-vtx/releases", "resource/vtx_releases", 1)
    my_download.download_file(
        "https://raw.githubusercontent.com/hd-zero/hdzero-vtx/main/src/common.h", "resource/vtx_common", 0)
    my_download.download_file(
        "https://raw.githubusercontent.com/hd-zero/hdzero-vtx/main/vtx_targets.png", "resource/vtx_targets.png", 0)
    my_download.download_file(
        "https://api.github.com/repos/ligenxxxx/event-vrx/releases", "resource/event_vrx_releases", 1)
    my_download.download_file(
        "https://api.github.com/repos/ligenxxxx/hv/releases", "resource/monitor_releases", 1)

    time.sleep(1)
    my_download.status = download_status.FILE_PARSE.value

    while True:
        if my_download.status == download_status.DOWNLOAD_VTX_FW.value:
            ret = my_download.download_file(
                my_download.url, my_download.save_path+".zip", 1)
            if ret == 1:
                # unzip file
                with zipfile.ZipFile(my_download.save_path+".zip", 'r') as zip_ref:
                    zip_ref.extractall("resource/")

                # rename file
                if (os.path.exists(my_download.save_path)):
                    os.remove(my_download.save_path)
                os.rename("resource/HDZERO_TX.bin", my_download.save_path)

                my_download.status = download_status.DOWNLOAD_VTX_FW_DONE.value
            elif ret == 2:  # stop
                my_download.status = download_status.IDLE.value
            else:
                my_download.status = download_status.DOWNLOAD_VTX_FW_FAILED.value

        elif my_download.status == download_status.DOWNLOAD_MONITOR_FW.value:
            ret = my_download.download_file(
                my_download.url, my_download.save_path, 1)
            if ret == 1:
                my_download.status = download_status.DOWNLOAD_MONITOR_FW_DONE.value
            elif ret == 2:  # stop
                my_download.status = download_status.IDLE.value
            else:
                my_download.status = download_status.DOWNLOAD_MONITOR_FW_FAILED.value

        elif my_download.status == download_status.DOWNLOAD_EVENT_VRX_FW.value:
            ret = my_download.download_file(
                my_download.url, my_download.save_path, 1)
            if ret == 1:
                my_download.status = download_status.DOWNLOAD_EVENT_VRX_FW_DONE.value
            elif ret == 2:  # stop
                my_download.status = download_status.IDLE.value
            else:
                my_download.status = download_status.DOWNLOAD_EVENT_VRX_FW_FAILED.value

        elif my_download.status == download_status.DOWNLOAD_EXIT.value:
            sys.exit()

        time.sleep(0.01)
