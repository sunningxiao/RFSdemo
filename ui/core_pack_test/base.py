import datetime
import locale
import os
import shutil
import socket
import threading
import time
from typing import List, Dict, Any, TYPE_CHECKING

import serial
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor

from ui.core_pack_test import utils as core_testutil
from ui.core_pack_test.core_pack_test import Ui_CorePackTest
from tools.printLog import *

if TYPE_CHECKING:
    from ui import RFSControl


class CorePackTestUI(QtWidgets.QWidget, Ui_CorePackTest):
    test_status_Signal = QtCore.pyqtSignal(int, object)
    test_name = {
        "0": "串口测试", "1": "射频状态测试", "2": "AD/DA自回环测试", "3": "DDR状态测试", "4": "GTY状态测试",
        "5": "GPIO状态测试", "6": "EMMC状态测试"
    }

    def __init__(self, parent):
        super(CorePackTestUI, self).__init__()
        self.ui_parent: "RFSControl" = parent
        self.setupUi(self)
        self._scan_timer = QTimer(self)
        self.trans = QtCore.QTranslator()
        self.device_serial = None
        self.is_listen = False
        self.now_test = 0
        self.select_language.currentTextChanged.connect(self._trigger_language)
        self.auto_language()
        self.available_com = {}
        self.btn_start.clicked.connect(self.btn_start_click)
        self.btn_serial_detial.clicked.connect(self.btn_serial_detial_click)
        self.btn_rf_detial.clicked.connect(self.btn_rf_detial_click)
        self.btn_chnl_detial.clicked.connect(self.btn_chnl_detial_click)
        self.btn_ddr_detial.clicked.connect(self.btn_ddr_detial_click)
        self.btn_gty_detial.clicked.connect(self.btn_gty_detial_click)
        self.btn_gpio_detial.clicked.connect(self.btn_gpio_detial_click)
        self.btn_emmc_detial.clicked.connect(self.btn_emmc_detial_click)
        self.btn_output.clicked.connect(self.btn_output_click)
        self.test_status_Signal.connect(self.change_test_status)
        self._scan_timer.timeout.connect(self.scanning)
        self._scan_timer.start(2000)
        self.record = None


        threading.Thread(target=self.test, daemon=True).start()

    def scanning(self):
        coms = core_testutil.scan_coms()
        if self.available_com != coms:
            self.select_comm.clear()
            for com in coms:
                self.select_comm.addItem(str(com))
            self.available_com = coms

    def test(self):
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.udp_socket.bind(('192.168.1.100', 15000))
        self.udp_socket.settimeout(3)
        while True:
            try:
                self.udp_socket.sendto(b"____\x10\x00\x002\x00\x00\x00\x00\x14\x00\x00\x00\x00\x00\x00\x00", ('<broadcast>', 5003))
                (_, addr) = self.udp_socket.recvfrom(2048)
                if '192.168.1.152' in addr:
                    self.network.setStyleSheet("background-color: rgba(0, 255, 0, 0.3)")
            except Exception as e:
                self.network.setStyleSheet("background-color: rgba(255, 0, 0, 0.3)")
            time.sleep(4)

    def change_test_status(self, status, value):
        # -7目标设备网络不通 -6测试完成 -4测试记录 -3日志 -2串口 -1进度条
        if status == -1:
            self.bar_process.setProperty("value", value)
        elif status == -2:
            if value == '串口连接已断开':
                self.text_serial_print.append(str(f'<font color=red>{value}</font>'))
            elif value != '':
                self.text_serial_print.append(str(value))
                self.record.reports[self.now_test].serial_data.append(value)
        elif status == -3:
            self.text_log_print.append(str(value))
        elif status == -4:
            self.list_test_history.addItem(f"{self.test_name.get(str(value))}开始")
        elif status == -5:
            self.now_test = value
        elif status == -6:
            self.is_listen = False
            self.btn_start.setEnabled(value)
            self.select_comm.setEnabled(value)
            self.device_serial.close()
            self.btn_output.setEnabled(True)
            self.process_test_status.setMaximum(1)
            self.text_log_print.append(f'<font color=green>测试完成</font>')
        elif status == -7:
            self.is_listen = False
            self.btn_start.setEnabled(value)
            self.select_comm.setEnabled(value)
            self.device_serial.close()
            self.btn_serial_detial.setEnabled(True)
            self.btn_rf_detial.setEnabled(True)
            self.btn_ddr_detial.setEnabled(True)
            self.btn_gty_detial.setEnabled(True)
            self.btn_gpio_detial.setEnabled(True)
            self.btn_emmc_detial.setEnabled(True)
            self.btn_chnl_detial.setEnabled(True)
            self.btn_output.setEnabled(True)
            self.process_test_status.setMaximum(1)
        # 0:串口状态    1:射频状态、RF配置   2:AD/DA回环    3:DDR状态   4:GTY状态   5:GPIO状态  6:EMMC状态
        elif status == 0:
            if value:
                self.label_status_serial.setStyleSheet("background-color: rgba(0, 255, 0, 0.25)")
                self.label_status_serial.setText('success')
                self.btn_serial_detial.setEnabled(True)
            else:
                self.label_status_serial.setStyleSheet("background-color: rgba(255, 0, 0, 0.25)")
                self.label_status_serial.setText('failed')
                self.btn_serial_detial.setEnabled(True)
        elif status == 1:
            if value:
                self.label_status_rf.setStyleSheet("background-color: rgba(0, 255, 0, 0.25)")
                self.label_status_rf.setText('success')
                self.btn_rf_detial.setEnabled(True)
            else:
                self.label_status_rf.setStyleSheet("background-color: rgba(255, 0, 0, 0.25)")
                self.label_status_rf.setText('failed')
                self.btn_rf_detial.setEnabled(True)
        elif status == 2:
            row = 0
            col = 0
            for result in value:
                if result == 0:
                    item = QtWidgets.QTableWidgetItem('正常')
                    item.setBackground(QColor(0, 255, 0, 63))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                else:
                    item = QtWidgets.QTableWidgetItem('异常')
                    item.setBackground(QColor(255, 0, 0, 63))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.table_status_chnl.setItem(row, col, item)
                col += 1
            self.btn_chnl_detial.setEnabled(True)
        elif status == 3:
            if value:
                self.label_status_ddr.setStyleSheet("background-color: rgba(0, 255, 0, 0.25)")
                self.label_status_ddr.setText('success')
                self.btn_ddr_detial.setEnabled(True)
            else:
                self.label_status_ddr.setStyleSheet("background-color: rgba(255, 0, 0, 0.25)")
                self.label_status_ddr.setText('failed')
                self.btn_ddr_detial.setEnabled(True)
        elif status == 4:
            if value:
                self.label_status_gty.setStyleSheet("background-color: rgba(0, 255, 0, 0.25)")
                self.label_status_gty.setText('success')
                self.btn_gty_detial.setEnabled(True)
            else:
                self.label_status_gty.setStyleSheet("background-color: rgba(255, 0, 0, 0.25)")
                self.label_status_gty.setText('failed')
                self.btn_gty_detial.setEnabled(True)
        elif status == 5:
            row = 0
            col = 0
            for result in value:
                if result == 0:
                    item = QtWidgets.QTableWidgetItem('收发均正常')
                    item.setBackground(QColor(0, 255, 0, 63))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                else:
                    item = QtWidgets.QTableWidgetItem('异常')
                    item.setBackground(QColor(255, 0, 0, 63))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.table_status_gpio.setItem(row, col, item)
                col += 1
                if col == 8:
                    row += 1
                    col = 0
            self.btn_gpio_detial.setEnabled(True)
        elif status == 6:
            if value:
                self.label_status_emmc.setStyleSheet("background-color: rgba(0, 255, 0, 0.25)")
                self.label_status_emmc.setText('success')
                self.btn_emmc_detial.setEnabled(True)
            else:
                self.label_status_emmc.setStyleSheet("background-color: rgba(255, 0, 0, 0.25)")
                self.label_status_emmc.setText('failed')
                self.btn_emmc_detial.setEnabled(True)

    def init_test_status(self):
        """
            将7个结果显示框重置
        """
        self.bar_process_value = 0
        self.bar_process.setProperty("value", 0)
        self.label_status_serial.setStyleSheet("background-color: none")
        self.label_status_serial.clear()
        self.label_status_rf.setStyleSheet("background-color: none")
        self.label_status_rf.clear()
        self.label_status_ddr.setStyleSheet("background-color: none")
        self.label_status_ddr.clear()
        self.label_status_gty.setStyleSheet("background-color: none")
        self.label_status_gty.clear()
        self.label_status_emmc.setStyleSheet("background-color: none")
        self.label_status_emmc.clear()
        self.table_status_gpio.clear()
        self.table_status_chnl.clear()

    def connect_com(self, com):
        baud = 115200
        check_sum = serial.PARITY_NONE
        byte_size = serial.EIGHTBITS
        stop_bit = serial.STOPBITS_ONE
        stream_str = {'xonxoff': False, 'rtscts': False, 'dsrdtr': False}
        if self.device_serial is not None:
            self.device_serial.close()
        try:
            self.device_serial = serial.Serial(port=com,
                                               baudrate=int(baud),
                                               bytesize=byte_size,
                                               parity=check_sum,
                                               stopbits=stop_bit,
                                               **stream_str,
                                               timeout=1)
        except Exception as e:
            self.test_status_Signal.emit(-3, f'<font color=red>err: {com}不正确，请选择其它串口</font>')
            raise e

    def btn_start_click(self):
        edit_pack_number = self.edit_pack_number.text()
        com_name = self.available_com.get(self.select_comm.currentText())
        self.init_test_status()

        if os.path.exists('_data') is False:
            os.makedirs('_data')
        else:
            shutil.rmtree('_data')
            os.makedirs('_data')
        if os.path.exists('export') is False:
            os.makedirs('export')
        if edit_pack_number == '':
            self.text_log_print.append("<font color=red>err：請輸入核心板編號</font>")
        elif com_name == '' or com_name is None:
            self.text_log_print.append("<font color=red>err：未選擇串口</font>")
        else:
            self.process_test_status.setMaximum(0)
            self.btn_start.setEnabled(False)
            self.select_comm.setEnabled(False)
            self.btn_serial_detial.setEnabled(False)
            self.btn_rf_detial.setEnabled(False)
            self.btn_chnl_detial.setEnabled(False)
            self.btn_ddr_detial.setEnabled(False)
            self.btn_gty_detial.setEnabled(False)
            self.btn_gpio_detial.setEnabled(False)
            self.btn_emmc_detial.setEnabled(False)
            self.btn_output.setEnabled(False)
            self.connect_com(com_name)
            self.text_serial_print.append(f"{com_name}串口已连接")
            self.is_listen = True
            self.record = None
            self.record = core_testutil.test_record(self.ui_parent.rfs_kit)
            self.record.serial_number = edit_pack_number
            serial_listen_thread = threading.Thread(target=self._start_listen, daemon=True)
            test_thread = threading.Thread(target=self._start_test, daemon=True)
            serial_listen_thread.start()
            # 监听线程开启
            test_thread.start()
            # 测试线程开启

    def _start_listen(self):
        while self.is_listen:
            try:
                data = self.device_serial.read(19500).decode('ascii')
                self.test_status_Signal.emit(-2, data)
            except Exception as e:
                printException(e)
                self.test_status_Signal.emit(-2, '串口连接已断开')
                time.sleep(3)

    def _start_test(self):
        try:
            res = self.ui_parent.rfs_kit.start_command()
            if res is not True:
                self.test_status_Signal.emit(-3, '请检查目标设备网络是否连通')
                self.test_status_Signal.emit(-7, True)
            else:
                self.record.get_dna(self.ui_parent.rfs_kit)
                for index, report in enumerate(self.record.reports):
                    res = self.ui_parent.rfs_kit.start_command()
                    if res is not True:
                        self.test_status_Signal.emit(-3, '请检查目标设备网络是否连通')
                        self.test_status_Signal.emit(-7, True)
                        break
                    self.test_status_Signal.emit(-5, index)
                    self.test_status_Signal.emit(-4, index)
                    self.bar_process_value += 14.5
                    if self.bar_process_value > 100:
                        self.bar_process_value = 100
                    if index == 2:
                        if self.record.reports[1].cmd_run_right is not True:
                            self.test_status_Signal.emit(-3, f'<font color=red>RF配置错误，不执行AD/DA测试</font>')
                            continue
                    report.run(self.ui_parent.rfs_kit)
                    self.test_status_Signal.emit(-1, self.bar_process_value)
                    if index == 0:  # 串口
                        self.test_status_Signal.emit(-3, f'指令名:{report.cmd_name}')
                        self.test_status_Signal.emit(-3, f'是否通过:{report.cmd_run_right}')
                        self.test_status_Signal.emit(index, report.cmd_run_right)
                        continue
                    elif index == 2:  # adda
                        self.test_status_Signal.emit(index, report.cmd_result[2])
                        # pass
                    elif index == 5:  # gpio
                        self.test_status_Signal.emit(index, report.cmd_result[2])
                    else:
                        self.test_status_Signal.emit(index, report.cmd_run_right)
                    self.test_status_Signal.emit(-3, f'指令名:{report.cmd_name}')

                    if report.cmd_result[0] == '':
                        self.test_status_Signal.emit(-3, "结果数据:")
                        for detail in report.result_detail:
                            self.test_status_Signal.emit(-3, f'{detail}')
                    else:
                        self.test_status_Signal.emit(-3, f'<font color=red>错误:{report.cmd_result[0]}</font>')
                    self.test_status_Signal.emit(-3, f'是否通过:{report.cmd_run_right}')

                self.record.end_time = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                self.record.export('export/')
                self.test_status_Signal.emit(-6, True)
        except Exception as e:
            self.test_status_Signal.emit(-3, f'<font color=red>请检查目标设备网络是否连通</font>')
            self.test_status_Signal.emit(-7, True)

    def btn_serial_detial_click(self):
        self.text_log_print.append(f'指令名:{self.record.reports[0].cmd_name}')
        self.text_log_print.append(f'是否通过:{self.record.reports[0].cmd_run_right}')

    def btn_rf_detial_click(self):
        self.text_log_print.append(f'指令名:{self.record.reports[1].cmd_name}')
        if self.record.reports[1].cmd_result[0] == '':
            for detail in self.record.reports[1].result_detail:
                self.text_log_print.append(f'结果数据:{detail}')
        else:
            self.text_log_print.append(f'错误:{self.record.reports[1].cmd_result[0]}')
        self.text_log_print.append(f'是否通过:{self.record.reports[1].cmd_run_right}')

    def btn_chnl_detial_click(self):
        self.text_log_print.append(f'指令名:{self.record.reports[2].cmd_name}')
        if self.record.reports[2].cmd_result[0] == '':
            for detail in self.record.reports[2].result_detail:
                self.text_log_print.append(f'结果数据:{detail}')
        else:
            self.text_log_print.append(f'错误:{self.record.reports[2].cmd_result[0]}')
        self.text_log_print.append(f'是否通过:{self.record.reports[2].cmd_run_right}')

    def btn_ddr_detial_click(self):
        self.text_log_print.append(f'指令名:{self.record.reports[3].cmd_name}')
        if self.record.reports[3].cmd_result[0] == '':
            for detail in self.record.reports[3].result_detail:
                self.text_log_print.append(f'结果数据:{detail}')
        else:
            self.text_log_print.append(f'错误:{self.record.reports[3].cmd_result[0]}')
        self.text_log_print.append(f'是否通过:{self.record.reports[3].cmd_run_right}')

    def btn_gty_detial_click(self):
        self.text_log_print.append(f'指令名:{self.record.reports[4].cmd_name}')
        if self.record.reports[4].cmd_result[0] == '':
            for detail in self.record.reports[4].result_detail:
                self.text_log_print.append(f'结果数据:{detail}')
        else:
            self.text_log_print.append(f'错误:{self.record.reports[4].cmd_result[0]}')
        self.text_log_print.append(f'是否通过:{self.record.reports[4].cmd_run_right}')

    def btn_gpio_detial_click(self):
        self.text_log_print.append(f'指令名:{self.record.reports[5].cmd_name}')
        if self.record.reports[5].cmd_result[0] == '':
            for detail in self.record.reports[5].result_detail:
                self.text_log_print.append(f'结果数据:{detail}')
        else:
            self.text_log_print.append(f'错误:{self.record.reports[5].cmd_result[0]}')
        self.text_log_print.append(f'是否通过:{self.record.reports[5].cmd_run_right}')

    def btn_emmc_detial_click(self):
        self.text_log_print.append(f'指令名:{self.record.reports[6].cmd_name}')
        if self.record.reports[6].cmd_result[0] == '':
            for detail in self.record.reports[6].result_detail:
                self.text_log_print.append(f'结果数据:{detail}')
        else:
            self.text_log_print.append(f'错误:{self.record.reports[6].cmd_result[0]}')
        self.text_log_print.append(f'是否通过:{self.record.reports[6].cmd_run_right}')

    def btn_output_click(self):
        self.record.export('export/')
        self.text_log_print.append('数据已导出')

    def auto_language(self):
        language_num = self.select_language.count()
        _locale = locale.getdefaultlocale()[0]
        if _locale in [self.select_language.itemText(i) for i in range(language_num)]:
            self._trigger_language(_locale)
            self.select_language.setCurrentText(_locale)
        else:
            self._trigger_language(self.select_language.currentText())

    def _trigger_language(self, language):
        self.trans.load(f'language/core_pack_{language}')
        _app = QtWidgets.QApplication.instance()  # 获取app实例
        _app.installTranslator(self.trans)
        # 重新翻译界面
        self.retranslateUi(self)
