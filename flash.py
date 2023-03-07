import time
from Download import *

class flash_class(object):
    def __init__(self):
        self.id = 0
        self.connectde = 0

flash_status_reg1 = 1

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

def flash_write_enable(ch341):
    ch341.iobuffer[0] = 0x06
    ch341.ilength = 1

    ch341.set_stream(0)
    ch341.stream_spi4()
    ch341.set_stream(1)

def flash_write_disable(ch341):
    ch341.iobuffer[0] = 0x04
    ch341.ilength = 1

    ch341.set_stream(0)
    ch341.stream_spi4()
    ch341.set_stream(1)

def flash_erase_block64(ch341):
    ch341.iobuffer[0] = 0xd8
    ch341.iobuffer[1] = 0
    ch341.iobuffer[2] = 0
    ch341.iobuffer[3] = 0
    ch341.ilength = 4

    ch341.set_stream(0)
    ch341.stream_spi4()
    ch341.set_stream(1)

def flash_read_status(ch341):
    global flash_status_reg1
    ch341.iobuffer[0] = 0x05
    ch341.iobuffer[1] = 0x00
    ch341.ilength = 2

    ch341.set_stream(0)
    ch341.stream_spi4()
    ch341.set_stream(1)
    flash_status_reg1 = int.from_bytes(ch341.iobuffer[1], byteorder='big')



def flash_wait_busy(ch341):
    global flash_read_status
    flash_read_status(ch341)
    while flash_status_reg1 & 0x01:
        flash_read_status(ch341)
        time.sleep(0.001)

def flash_erase(ch341):
    print()
    print("erase flash")
    flash_write_enable(ch341)
    flash_erase_block64(ch341)
    flash_wait_busy(ch341)
    flash_write_disable(ch341)

def flash_write_page(ch341, baseAddress, len, firmware):
    ch341.iobuffer[0] = 0x02
    ch341.iobuffer[1] = (baseAddress >> 16) & 0xff
    ch341.iobuffer[2] = (baseAddress >> 8) & 0xff
    ch341.iobuffer[3] = (baseAddress >> 0) & 0xff
    ch341.ilength = 4 + len

    for i in range(len):
        try:
            ch341.iobuffer[4+i] = firmware[i]
        except:
            ch341.iobuffer[4+i] = 0xff
        
    ch341.set_stream(0)
    ch341.stream_spi4()
    ch341.set_stream(1)


def flash_write_file(ch341):
    f = open(ch341.fw_path, "rb")
    firmware = f.read()
    pageNum = (ch341.fw_full_size + + (1<<8) - 1) >> 8;

    ch341.percent = 0
    
    for page in range(pageNum):
        ch341.percent = int(page * 100 / pageNum) + 1
        print(ch341.percent)
        
        baseAddress = page << 8

        flash_write_enable(ch341)
        flash_write_page(ch341, baseAddress, 256, firmware[baseAddress:])
        flash_write_disable(ch341)
        flash_wait_busy(ch341)

