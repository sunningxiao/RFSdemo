import serial
from serial.tools import list_ports
from threading import Thread, Lock, Event
from tools.printLog import *
from PyQt5.QtCore import QTimer


class SerialUIMixin:
    checksum_map = {'NONE': serial.PARITY_NONE, 'ODD': serial.PARITY_ODD, 'EVEN': serial.PARITY_EVEN,
                    'MARK': serial.PARITY_MARK, 'SPACE': serial.PARITY_SPACE}
    byte_size_map = {'5': serial.FIVEBITS, '6': serial.SIXBITS, '7': serial.SEVENBITS, '8': serial.EIGHTBITS}
    stop_bits_map = {'1': serial.STOPBITS_ONE, '1.5': serial.STOPBITS_ONE_POINT_FIVE, '2': serial.STOPBITS_TWO}
    stream_map = {
        'NONE': {'xonxoff': False, 'rtscts': False, 'dsrdtr': False},
        'XON/XOFF': {'xonxoff': True, 'rtscts': False, 'dsrdtr': False},
        'RTS/CTS': {'xonxoff': False, 'rtscts': True, 'dsrdtr': False},
        'DSR/DTR': {'xonxoff': False, 'rtscts': False, 'dsrdtr': True},
        'RTS/CTS/XON/XOFF': {'xonxoff': True, 'rtscts': True, 'dsrdtr': False},
        'DSR/DTR/XON/XOFF': {'xonxoff': True, 'rtscts': False, 'dsrdtr': True},
    }

    def __init__(self):
        self.available_com = {}
        self.device_serial = None
        self._serial_stop_event = Event()
        self._serial_stopped_event = Event()
        self._serial_scan_timer = QTimer(self)

    def init_serial_ui(self):
        self._serial_scan_timer.timeout.connect(self.scanning_com)
        self._serial_scan_timer.start(2000)

        self.ui.select_com_checksum.clear()
        for item in self.checksum_map:
            self.ui.select_com_checksum.addItem(item)

        self.ui.select_com_data_bit.clear()
        for item in self.byte_size_map:
            self.ui.select_com_data_bit.addItem(item)
        self.ui.select_com_data_bit.setCurrentIndex(3)

        self.ui.select_com_stop_bit.clear()
        for item in self.stop_bits_map:
            self.ui.select_com_stop_bit.addItem(item)

        self.ui.select_com_stream.clear()
        for item in self.stream_map:
            self.ui.select_com_stream.addItem(item)

    def scanning_com(self):
        coms = {}
        for com in list_ports.comports():
            coms[str(com)] = com.device
        if coms != self.available_com:
            self.ui.select_com_id.clear()
            for com in coms:
                self.ui.select_com_id.addItem(str(com))
            self.available_com = coms

    def connect_com(self, port, baud_rate, check_sum, byte_size, stop_bits, stream_str):
        self._serial_stop_event.set()
        self._serial_stopped_event.wait(1)
        if self.device_serial is not None:
            self.device_serial.close()
        self.device_serial = serial.Serial(port=self.available_com.get(port, port),
                                           baudrate=int(baud_rate),
                                           bytesize=self.byte_size_map[byte_size],
                                           parity=self.checksum_map[check_sum],
                                           stopbits=self.stop_bits_map[stop_bits],
                                           **self.stream_map[stream_str],
                                           timeout=1)
        self._serial_stopped_event.clear()
        self._serial_stop_event.clear()
        if self.device_serial.isOpen():
            _thread = Thread(target=self.start_recv)
            _thread.start()

    def start_recv(self):
        while True:
            if self._serial_stop_event.is_set():
                break

            try:
                self.device_serial: serial.Serial
                data = self.device_serial.read(1024).decode('ascii')
                if data != '':
                    printColor(data, '#DEB887')
            except UnicodeDecodeError as e:
                printException(e)

        self._serial_stopped_event.set()
