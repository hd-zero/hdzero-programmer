import threading
from ui import UI_mainloop
from Download import DownloadThreadProc


def main():
    DownloadFile_Thread = threading.Thread(
        target=DownloadThreadProc, name='download_file')
    DownloadFile_Thread.start()

    UI_Thread = threading.Thread(
        target=UI_mainloop, name='UI_mainloop')
    UI_Thread.start()


if __name__ == '__main__':
    main()
