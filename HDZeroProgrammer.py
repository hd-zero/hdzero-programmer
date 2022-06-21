import threading
from RootWindow import RootThreadProc
from RootWindow import root
from Download import DownloadThreadProc


def main():
    RootWindowThread = threading.Thread(
        target=RootThreadProc, name='root_window')
    RootWindowThread.start()

    DownloadFileThread = threading.Thread(
        target=DownloadThreadProc, name='download_file')
    DownloadFileThread.start()

    root.mainloop()


if __name__ == '__main__':
    main()
