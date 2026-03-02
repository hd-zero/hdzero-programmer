import threading
import os
import sys
import shutil
import time
from main_window import ui_thread_proc
from download import download_thread_proc
from download import download_vtx_releases
from download import download_vtx_common
from download import download_vtx_targets_image
from download import download_event_vrx_releases
from download import download_monitor_releases
from download import download_radio_releases
from ch341 import ch341_thread_proc


def get_resource_folder():
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    resource_folder = os.path.join(base_path, "data_folder")
    print(resource_folder)

    return resource_folder


def check_and_release_resource():

    resource_folder = get_resource_folder()

    if os.path.exists("resource"):
        pass
    else:
        for filename in os.listdir(resource_folder):
            source_file = os.path.join(resource_folder, filename)
            destination_file = os.path.join("resource", filename)
            if os.path.isfile(source_file):
                shutil.copy(source_file, destination_file)
            elif os.path.isdir(source_file):
                shutil.copytree(source_file, destination_file)


def main():
    check_and_release_resource()

    ui_thread = threading.Thread(target=ui_thread_proc, name="ui")
    ui_thread.start()

    ch341_thread = threading.Thread(target=ch341_thread_proc, name="ch341")
    ch341_thread.start()

    time.sleep(1)

    download_0 = threading.Thread(
        target=download_vtx_releases, name="download_vtx_releases")
    download_0.start()
    download_1 = threading.Thread(
        target=download_vtx_common, name="download_vtx_common")
    download_1.start()

    download_2 = threading.Thread(
        target=download_vtx_targets_image, name="download_vtx_targets_image")
    download_2.start()

    download_3 = threading.Thread(
        target=download_event_vrx_releases, name="download_event_vrx_releases")
    download_3.start()

    download_4 = threading.Thread(
        target=download_monitor_releases, name="download_monitor_releases")
    download_4.start()

    download_5 = threading.Thread(
        target=download_radio_releases, name="download_radio_releases")
    download_5.start()

    download_thread = threading.Thread(
        target=download_thread_proc, name="download")
    download_thread.start()

if __name__ == '__main__':
    main()
