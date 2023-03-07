import time
from Download import *

class flash_class(object):
    def __init__(self):
        self.id = 0
        self.connectde = 0


def flash_read_id(ch341):
    ch341.iobuffer[0] = 0x90
    ch341.iobuffer[1] = 0x90
    ch341.iobuffer[2] = 0x90
    ch341.iobuffer[3] = 0x90
    ch341.iobuffer[4] = 0x90
    ch341.iobuffer[5] = 0x90
    ch341.ilength = 6

    ch341.set_stream(0)
    ch341.stream_spi4()
    ch341.set_stream(1)

    return int.from_bytes(ch341.iobuffer[4], byteorder='big') * 256 \
            + int.from_bytes(ch341.iobuffer[5], byteorder='big')

def flash_connect(ch341):
    while True:
        flash_id = flash_read_id(ch341)
        if flash_id == 0xEF13:
            print("DBG: flash is found")
            return
        else:
            time.sleep(0.2)

def flash_read_vtx_id(ch341):
    raddr = 0x10000
    ch341.iobuffer[0] = 0x03;
    ch341.iobuffer[1] = (raddr >> 16) & 0xff
    ch341.iobuffer[2] = (raddr >> 8) & 0xff
    ch341.iobuffer[3] = raddr & 0xff
    ch341.iobuffer[4] = 0x00
    ch341.ilength = 16
    
    ch341.set_stream(0)
    ch341.stream_spi4()
    ch341.set_stream(1)