import threading
import os
import sys
import shutil
from main_window import ui_thread_proc
from download import download_thread_proc
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
    download_thread = threading.Thread(
        target=download_thread_proc, name="download")
    download_thread.start()

    ui_thread = threading.Thread(target=ui_thread_proc, name="ui")
    ui_thread.start()

    ch341_thread = threading.Thread(target=ch341_thread_proc, name="ch341")
    ch341_thread.start()


if __name__ == '__main__':
    main()
