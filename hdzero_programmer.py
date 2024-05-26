import threading
import os
import sys
from main_window import main_window_ui
from downloader import download_thread_proc
from ch341 import ch341_thread_proc

run_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
os.chdir(run_path)

def main():

    download_thread = threading.Thread(target=download_thread_proc, name="downloader")
    download_thread.start()

    ch341_thread = threading.Thread(target=ch341_thread_proc, name="ch341")
    ch341_thread.start()

    main_window_ui()

if __name__ == '__main__':
    main()
