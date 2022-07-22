import os
import socket
import time
import serial
from typing import TYPE_CHECKING
from serial.tools import list_ports
from threading import Thread, Lock, Event
from tools.printLog import *
from PyQt5.QtCore import QTimer
from PyQt5 import QtWidgets, QtCore
import numpy as np

if TYPE_CHECKING:
    from core import RFSKit


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
            _thread = Thread(target=self.start_recv, daemon=True)
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


def center_move2_point(widget: QtWidgets.QWidget, point: QtCore.QPoint) -> None:
    """
    将widget的中心移动导指定的点

    :param widget: 目标widget
    :param point: 目标点
    :return: 无
    """
    frame = widget.frameGeometry()
    frame.moveCenter(point)
    widget.move(frame.topLeft())


def get_git_version():
    if __file__.endswith('.pyc'):
        return
    import git
    _git = git.Git()
    version = _git.describe('--tags')
    with open('./VERSION', 'w', encoding='utf-8') as fp:
        fp.write(version)


def send_command(ip, port, command):
    """
    最简指令发送

    :param ip:
    :param port:
    :param command:
    :return:
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.settimeout(5)
    try:
        sock.connect((ip, port))
        command_len = len(command)
        while command_len > 0:
            sent = sock.send(command)
            command = command[sent:]
            command_len -= sent
            # printColor(f'未发送{command_len}字节', 'green')
        _feedback = sock.recv(20)

        sock.close()
    except Exception as e:
        return False

    return True


def save_data_by_timer(rfskit: "RFSKit", package_num: int):
    self = rfskit._data_solve
    file_path = 0
    while os.path.exists(str(file_path)):
        file_path += 1
    os.mkdir(str(file_path))
    file_name = 0
    file = open(os.path.join(fr'./{file_path}', f'{file_name}.data'), 'wb')
    while not self.has_data_upload_event.wait(1):
        ...
    try:
        start_time = time.time()
        recv_length = data_length = 0
        split_length = max(self.once_package*package_num, self.once_package)
        self.write_speed = 0
        while not self.upload_stop_event.is_set():
            _data = rfskit.get_stream_data()
            if isinstance(_data, np.ndarray):
                file.write(_data)
                data_size = _data.size * 4
                recv_length += data_size
                data_length += data_size
                end_time = time.time()
                if recv_length >= split_length:
                    file.close()
                    file_name += 1
                    file = open(os.path.join(fr'./{file_path}', f'{file_name}.data'), 'wb')
                    recv_length = 0
                if end_time - start_time > 1:
                    self.write_speed = data_length / (end_time - start_time) / 1024 ** 2
                    start_time = time.time()
                    data_length = 0
    except AssertionError as e:
        printDebug(e)
        file.close()
    except Exception as e:
        printException(e)
        file.close()
    finally:
        file.close()
        printColor("文件保存完成", 'green')
        # us_signal.status_trigger.emit((0, 0))
