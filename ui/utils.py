import os
import socket
import time
import threading

import serial
from typing import TYPE_CHECKING
import re
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
        self.temp_sign = 0
        self.ADC_adel_adjust = [1, 1, 1, 1]
        self.DAC_adel_adjust = [1, 1, 1, 1]
        self.change_done_0 = [0, 0, 0, 0, 0, 0, 0, 0]
        self.change_done_1 = [0, 0, 0, 0, 0, 0, 0, 0]
        self.cache = ''
        self._lock = threading.Lock()
        self.list = []

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
                data = self.device_serial.read(19500).decode('ascii')
                if data != '':
                    printColor(data, '#DEB887')
                    self.cache += data
                    if self.calibration:
                        thread = threading.Thread(target=self.read_cachedata, daemon=True)
                        thread.start()

            except UnicodeDecodeError as e:
                printException(e)

        self._serial_stopped_event.set()

    def read_cachedata(self):

        if self.cache is None:
            pass
        else:
            self.read_str(self.cache)

    def read_str(self, cache_data):
        temp = re.findall(r"Temp:(\d(\d)?(\d)?)", cache_data)
        match_sign = re.findall(r"Zynq Server : Send feedback to Client done", cache_data)
        if temp:
            for i in range(len(temp)):
                if int(temp[i][0]) + 5 < int(self.temp_sign) or int(temp[i][0]) - 5 > int(
                        self.temp_sign):
                    self.temp_sign = temp[i][0]
                    self.linking_button('RF配置', need_feedback=True, need_file=False)()
                else:
                    pass
        if match_sign:
            self.deal_clock_data(self.cache)
            self.match_sign = False

        # if self.change_done != 16:
        #     self.linking_button('RF配置', need_feedback=True, need_file=False)()

    def deal_clock_data(self, match_data):
        self.clock_data = re.findall(
            r"(metal: info:      (ADC|DAC)(\d): \d...............................................................................................................................)",
            match_data)
        self.list += self.clock_data
        self.cache = ''
        if len(self.list) >= 16:
            self.DAC0_dtc0 = self.list[0][0]
            self.DAC1_dtc0 = self.list[1][0]
            self.DAC2_dtc0 = self.list[2][0]
            self.DAC3_dtc0 = self.list[3][0]
            self.DAC0_dtc1 = self.list[4][0]
            self.DAC1_dtc1 = self.list[5][0]
            self.DAC2_dtc1 = self.list[6][0]
            self.DAC3_dtc1 = self.list[7][0]
            self.ADC0_dtc0 = self.list[8][0]
            self.ADC1_dtc0 = self.list[9][0]
            self.ADC2_dtc0 = self.list[10][0]
            self.ADC3_dtc0 = self.list[11][0]
            self.ADC0_dtc1 = self.list[12][0]
            self.ADC1_dtc1 = self.list[13][0]
            self.ADC2_dtc1 = self.list[14][0]
            self.ADC3_dtc1 = self.list[15][0]
            self.clock_data = None
            self.list = self.list[16:]
            self.ADC_dtc0 = [self.ADC0_dtc0, self.ADC1_dtc0, self.ADC2_dtc0, self.ADC3_dtc0]
            self.ADC_dtc1 = [self.ADC0_dtc1, self.ADC1_dtc1, self.ADC2_dtc1, self.ADC3_dtc1]
            self.DAC_dtc0 = [self.DAC0_dtc0, self.DAC1_dtc0, self.DAC2_dtc0, self.DAC3_dtc0]
            self.DAC_dtc1 = [self.DAC0_dtc1, self.DAC1_dtc1, self.DAC2_dtc1, self.DAC3_dtc1]
            self.judge()

    # def adel_adjust(self, former_adel, dtc_code0, dtc_code1, dtc_code2, dtc_code3, step):
    #     position_of_hash = 88
    # # 首先确认调整范围
    # span_right = former_adel
    # span_left = 30 - former_adel
    # ##确定警号和星号的位置
    # position_of_hash = 0
    # position_of_star = 0
    # while (dtc_code[position_of_hash] != '#') & (position_of_hash < len(dtc_code) - 3):
    #     position_of_hash += 1
    # if position_of_hash == len(dtc_code) - 3:
    #     adjust_adel = former_adel
    #     return adjust_adel
    #
    # while dtc_code[position_of_star] != '*':
    #     position_of_star += 1
    # adjust = position_of_hash - position_of_star
    # if (adjust > 0):
    #     dir = +1
    # else:
    #     dir = -1
    # adjust = adjust / step
    # if (former_adel + adjust > 0) & (former_adel + adjust < 30):
    #     adjust_adel = former_adel + adjust
    # else:
    #     position_of_zero_near = position_of_hash - 1
    #     while 1:
    #         if (dtc_code[position_of_zero_near] != '0') & (
    #                 dtc_code[position_of_zero_near + 1 * dir] == '0'):
    #             break
    #         else:
    #             position_of_zero_near += 1 * dir
    #     position_of_zero_beyond = position_of_zero_near
    #     while 1:
    #         if (dtc_code[position_of_zero_beyond] == '0') & (
    #                 dtc_code[position_of_zero_beyond + 1 * dir] != '0'):
    #             break
    #         else:
    #             position_of_zero_beyond += 1 * dir
    #     adjust = (position_of_hash - (position_of_zero_beyond + position_of_zero_near) / 2) / step
    #     adjust_adel = adjust + former_adel
    #     if (adjust_adel < 0) & (adjust_adel > 30):
    #         adjust_adel = -999
    # adjust_adel = int(adjust_adel)

    def judge(self):
        print(self.DAC_adel_adjust)
        print(self.ADC_adel_adjust)
        self.rfs_kit.set_param_value('DAC0延迟', int(self.DAC_adel_adjust[0]))
        self.rfs_kit.set_param_value('DAC2延迟', int(self.DAC_adel_adjust[2]))
        self.rfs_kit.set_param_value('ADC0延迟', int(self.ADC_adel_adjust[0]))
        self.rfs_kit.set_param_value('ADC1延迟', int(self.ADC_adel_adjust[1]))
        self.rfs_kit.set_param_value('ADC2延迟', int(self.ADC_adel_adjust[2]))
        self.rfs_kit.set_param_value('ADC3延迟', int(self.ADC_adel_adjust[3]))

        self.change_done_0[0] = self.adel_detect(self.DAC_dtc0[0])
        self.change_done_0[1] = self.adel_detect(self.DAC_dtc1[0])
        self.change_done_0[2] = self.adel_detect(self.DAC_dtc0[2])
        self.change_done_0[3] = self.adel_detect(self.DAC_dtc1[2])
        self.change_dac0_sign = self.change_done_0[0] + self.change_done_0[1]
        self.change_dac1_sign = self.change_done_0[2] + self.change_done_0[3]
        for i in range(4):
            self.change_done_1[i] = self.adel_detect(self.ADC_dtc0[i])
        for i in range(4):
            self.change_done_1[i + 4] = self.adel_detect(self.ADC_dtc1[i])
        self.change_adc0_sign = self.change_done_1[0] + self.change_done_1[4]
        self.change_adc1_sign = self.change_done_1[1] + self.change_done_1[5]
        self.change_adc2_sign = self.change_done_1[2] + self.change_done_1[6]
        self.change_adc3_sign = self.change_done_1[3] + self.change_done_1[7]

        if self.change_dac0_sign != 2 and self.DAC_adel_adjust[0] < 30:
            self.DAC_adel_adjust[0] += 1
            self.linking_button('RF配置', need_feedback=True, need_file=False)()
        elif self.change_dac1_sign != 2 and self.DAC_adel_adjust[2] < 30:
            self.DAC_adel_adjust[2] += 1
            self.linking_button('RF配置', need_feedback=True, need_file=False)()
        elif self.change_adc0_sign != 2 and self.ADC_adel_adjust[0] < 30:
            self.ADC_adel_adjust[0] += 1
            self.linking_button('RF配置', need_feedback=True, need_file=False)()
        elif self.change_adc1_sign != 2 and self.ADC_adel_adjust[1] < 30:
            self.ADC_adel_adjust[1] += 1
            self.linking_button('RF配置', need_feedback=True, need_file=False)()
        elif self.change_adc2_sign != 2 and self.ADC_adel_adjust[2] < 30:
            self.ADC_adel_adjust[2] += 1
            self.linking_button('RF配置', need_feedback=True, need_file=False)()
        elif self.change_adc3_sign != 2 and self.ADC_adel_adjust[3] < 30:
            self.ADC_adel_adjust[3] += 1
            self.linking_button('RF配置', need_feedback=True, need_file=False)()
        if self.change_adc3_sign == 2:
            self.write_txt(self.temp_sign, self.DAC_adel_adjust[0], self.DAC_adel_adjust[2], self.ADC_adel_adjust[0],
                           self.ADC_adel_adjust[1], self.ADC_adel_adjust[2], self.ADC_adel_adjust[3])
            self.DAC_adel_adjust[0] = 1
            self.DAC_adel_adjust[2] = 1
            self.ADC_adel_adjust[0] = 1
            self.ADC_adel_adjust[1] = 1
            self.ADC_adel_adjust[2] = 1
            self.ADC_adel_adjust[3] = 1

    def adel_detect(self, dtc_code):
        change_done = 0
        position_of_hash = 0
        position_of_star = 0
        while (dtc_code[position_of_hash] != '#') & (position_of_hash < len(dtc_code) - 3):
            position_of_hash += 1
        if position_of_hash == len(dtc_code) - 3:
            change_done = 1
            return change_done
        position_of_zuo = position_of_hash
        position_of_you = position_of_hash
        while 1:
            if (dtc_code[position_of_zuo] == '1') | (dtc_code[position_of_zuo] == '2') | (
                    dtc_code[position_of_zuo] == '3'):
                break
            if (position_of_zuo == 0):
                break
            position_of_zuo -= 1
        while 1:
            if (dtc_code[position_of_you] == '1') | (dtc_code[position_of_you] == '2') | (
                    dtc_code[position_of_you] == '3'):
                break
            if (position_of_you == len(dtc_code) - 3):
                break
            position_of_you += 1
        if (position_of_hash - position_of_zuo) > (position_of_you - position_of_hash):
            adjust = position_of_you - position_of_hash
        else:
            adjust = position_of_hash - position_of_zuo
        if adjust > 3:
            change_done = 1
        return change_done

    def write_txt(self, tempa, DAC_adel_adjust0, DAC_adel_adjust2, ADC_adel_adjust0, ADC_adel_adjust1, ADC_adel_adjust2,
                  ADC_adel_adjust3):
        full_path = fr'./handled.txt'
        file = open(full_path, 'a')
        file.write(str("%04d" % int(tempa)))
        file.write(str("%04d" % int(DAC_adel_adjust0)))
        file.write(str("%04d" % int(DAC_adel_adjust2)))
        file.write(str("%04d" % int(ADC_adel_adjust0)))
        file.write(str("%04d" % int(ADC_adel_adjust1)))
        file.write(str("%04d" % int(ADC_adel_adjust2)))
        file.write(str("%04d" % int(ADC_adel_adjust3)))
        file.write("\r\n")
        file.close()


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
