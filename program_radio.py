import serial.tools.list_ports
import time
import esptool
import sys

def flash_esp_api(
    port,
    baud,
    chip,
    flash_args,
):
    """
    flash_args:
        [
            (0x1000, "bootloader.bin"),
            (0x8000, "partition-table.bin"),
            (0x10000, "app.bin"),
        ]
    """

    # 等价于命令行参数
    argv = [
        "--chip", chip,
        "--port", port,
        "--baud", str(baud),
        "write-flash",
    ]

    for addr, path in flash_args:
        argv.append(hex(addr))
        argv.append(path)

    # esptool 内部就是解析 sys.argv
    old_argv = sys.argv
    try:
        sys.argv = ["esptool.py"] + argv
        esptool.main()
    finally:
        sys.argv = old_argv


class radio_class(object):
    def __init__(self):
        self.ser = ''
        self.status = 0
        self.com = ''

    def find_word_in_string(self, s, word):
        words = s.split()
        for w in words:
            if w == word:
                return 1
        return 0

    def serial_tx(self,str):
        self.ser.write(str.encode('utf-8'))


    def serial_rx(self, sleep_sec):
        data_received = b''
        time.sleep(sleep_sec)
        while self.ser.in_waiting:
            data_received = self.ser.read(self.ser.in_waiting)
            return data_received.decode('utf-8')

    def getc(self, size, timeout=1):
        return self.ser.read(size)

    def putc(self, data, timeout=1):
        return self.ser.write(data)

    def search_stm32_port(self):
        ports = list(serial.tools.list_ports.comports())
        for i in range(0, len(ports)):
            if (self.find_word_in_string(ports[i].description, 'STMicroelectronics')):
                self.com = ports[i].name
                time.sleep(1)
                self.ser = serial.Serial(self.com, 115200, timeout=2)
                return 1
        return 0
    
    def search_elrs_tx_port(self):
        ports = list(serial.tools.list_ports.comports())
        for i in range(0, len(ports)):
            if (self.find_word_in_string(ports[i].description, 'CH340')):
                self.com = ports[i].name
                time.sleep(1)
                self.ser = serial.Serial(self.com, 115200, timeout=2)
                return 1
        return 0

    def unzip_radio_firmware(self, file_path, dest_folder):
        import zipfile
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(dest_folder)

    def radio_is_active(self):
        if self.search_stm32_port() == 0:
            return False
        
        cmd = "ATPING\r\n"
        self.ser.write(cmd.encode('utf-8'))
        rx = self.serial_rx(0.1)

        self.ser.close()
        if self.find_word_in_string(rx, "HDZero"):
            return True
        else:
            return False
    
    def program_elrs_tx(self, base_address, fw):
        if self.search_stm32_port() == 0:
            return False

        cmd = "ATPGTX\r\n"
        self.ser.write(cmd.encode('utf-8'))
        time.sleep(0.2)
        self.ser.close()

        time.sleep(1)
        if self.search_elrs_tx_port() == 0:
            return False
        self.ser.close()
        
        flash_esp_api(
            port=self.ser.port,
            baud=460800,
            chip="esp32",
            flash_args=[
                (base_address, fw),
            ],
        )

        return True

    def program_elrs_backpack(self, base_address, fw):
        if self.search_stm32_port() == 0:
            return False

        cmd = "ATPGBP\r\n"
        self.ser.write(cmd.encode('utf-8'))
        time.sleep(0.2)
        self.ser.close()

        time.sleep(1)
        if self.search_elrs_tx_port() == 0:
            return False
        self.ser.close()
        
        flash_esp_api(
            port=self.ser.port,
            baud=460800,
            chip="esp32c3",
            flash_args=[
                (base_address, fw),
            ],
        )

        return True
    
my_radio = radio_class()