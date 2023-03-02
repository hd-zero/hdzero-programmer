import threading
from ui import UI_mainloop
from Download import DownloadThreadProc
from ch341_wrapper import ch341ThreadProc

def main():
    
    ch341_Thread = threading.Thread(
        target=ch341ThreadProc, name='ch341')
    ch341_Thread.start()

    DownloadFile_Thread = threading.Thread(
        target=DownloadThreadProc, name='download_file')
    DownloadFile_Thread.start()

    UI_Thread = threading.Thread(
        target=UI_mainloop, name='UI_mainloop')
    UI_Thread.start()


if __name__ == '__main__':
    main()
