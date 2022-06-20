import threading
from RootWindow import RootThreadProc

def main():
    RootWindowThread = threading.Thread(target=RootThreadProc(), name='window')
    RootWindowThread.start()

if __name__ == '__main__':
    main()