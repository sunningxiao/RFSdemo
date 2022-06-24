import sys
import re
import random
import threading

import numpy as np
import qdarkstyle
import pyqtgraph as pg
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

from MCIUI.主框架 import MAIN
from MCIUI.awg页面 import Awg_widget
from MCIUI.probe页面 import Probe_widget
from quantum_driver.NS_MCI import Driver
from quantum_driver.NS_QSYNC import Driver as QDriver


class ConfigWidget:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_ui = MAIN()
        self.main_ui.Connect_AWG.clicked.connect(self.add_awg)
        self.main_ui.Connect_Probe_2.clicked.connect(self.add_probe)
        self.main_ui.QSYNC.clicked.connect(self.config_QSYNC_ip)
        self.i, self.j, self.k, self.m = 0, 0, 0, 0
        self.awg_ip_list = []
        self.probe_ip_list = []
        self.page_dic = {}
        self.darate = {}

    def run_ui(self):
        self.app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.main_ui.show()
        sys.exit(self.app.exec())

    # 判断IP地址是否合法
    def check_ip(self, ip):
        compile_ip = re.compile(
            '^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
        return isinstance(compile_ip.match(ip), re.Match)

    def add_awg(self):
        self.main_ui.ip1.exec()
        if not self.main_ui.ip1.click_ok:
            return
        addr = self.main_ui.ip1.IPlineEdit.text()
        self.addr_g = addr
        self.main_ui.ip1.IPlineEdit.clear()
        if not self.check_ip(addr):
            return
        self.main_ui.ip1.click_ok = False
        _thread = threading.Thread(target=self.add_awg_function(addr), daemon=True)
        _thread.start()
        _thread = threading.Thread(target=self.cnt_open_qsync(), daemon=True)
        _thread.start()

    def add_probe(self):
        self.main_ui.ip2.exec()
        if not self.main_ui.ip2.click_ok:
            return
        addr = self.main_ui.ip2.ipaddr.text()
        self.addr_p = addr
        self.main_ui.ip2.ipaddr.clear()
        if not self.check_ip(addr):
            return
        self.darate[addr] = self.main_ui.ip1.DArate.text()

        self.main_ui.ip2.click_ok = False
        _thread = threading.Thread(target=self.add_probe_function(addr), daemon=True)
        _thread.start()
        _thread = threading.Thread(target=self.cnt_open_qsync(), daemon=True)
        _thread.start()


    def add_awg_function(self, addr):
        self.tabname = 'AWG-' + str(self.m)
        if addr in self.awg_ip_list:
            print("已经打开相同IP的AWG页面")
            return
        self.pagea = Awg_widget(self, addr)
        self.config_button()
        for i in range(5):
            self.pagea.waves()
        self.pagea.changepy.clicked.connect(self.action_exec_user_code)
        self.awg_ip_list.append(addr)
        self.AWGADD = QtWidgets.QWidget()
        awg_layout = QtWidgets.QGridLayout(self.AWGADD)
        awg_layout.addWidget(self.pagea)
        awg_layout.setContentsMargins(0, 0, 0, 0)
        self.AWGADD.setObjectName("AWGADD")
        self.main_ui.tab.addTab(self.AWGADD, '{}'.format(self.tabname))
        self.main_ui.tab.setCurrentIndex(self.k)
        self.page_dic[addr] = self.pagea
        if addr in self.probe_ip_list:
            self.page_dic[addr].manual_config.setEnabled(False)
            self.page_dic[addr].manual_trig.setEnabled(False)
            self.page_dic[addr].external_config.setEnabled(False)
            self.page_dic[addr].external_trig.setEnabled(False)
            self.page_dic[addr].internal_config.setEnabled(False)
            self.page_dic[addr].internal_trig.setEnabled(False)
        # _thread = threading.Thread(target=self.open_awg(self.addr_g), daemon=True)
        # _thread.start()
        self.open_awg(self.addr_g)
        self.m = self.m + 1
        self.k = self.k + 1
        self.pagea.Manual_2.setEnabled(False)
        self.pagea.pushButton.setEnabled(False)
        self.pagea.internal.setEnabled(False)
        self.main_ui.ip3.click_ok = False

    def add_probe_function(self, addr):
        if addr in self.probe_ip_list:
            print("已经打开相同IP的probe页面")
            return
        if addr in self.awg_ip_list:  # 判断输入ip是否在列表中
            self.getdata = self.page_dic[addr].alldata  # 前面将IP：tab页面内容存在字典page_dic中 想直接通过这个字典获取响应页面的alldata
            self.page_dic[addr].manual_config.setEnabled(False)
            self.page_dic[addr].manual_trig.setEnabled(False)
            self.page_dic[addr].external_config.setEnabled(False)
            self.page_dic[addr].external_trig.setEnabled(False)
            self.page_dic[addr].internal_config.setEnabled(False)
            self.page_dic[addr].internal_trig.setEnabled(False)

        self.judge_open_probe_param(addr)
        self.tabname1 = 'Probe-' + str(self.j)
        self.pageb = Probe_widget(self, addr)
        self.config_probe_button()
        self.probe_ip_list.append(addr)
        for i in range(12):
            self.a = int(i / 3)
            self.b = int(i % 3)
            self.add_scatter(None)
        for i in range(12):
            self.pageb.add_plot(i)

        self.AWGProbe = QtWidgets.QWidget()

        awg_layout1 = QtWidgets.QGridLayout(self.AWGProbe)
        awg_layout1.addWidget(self.pageb)
        awg_layout1.setContentsMargins(0, 0, 0, 0)
        self.AWGProbe.setObjectName("AWGProbe")
        self.main_ui.tab.addTab(self.AWGProbe, '{}'.format(self.tabname1))
        self.main_ui.tab.setCurrentIndex(self.k)
        self.j = self.j + 1
        self.k = self.k + 1
        self.pageb.pushButton.setEnabled(False)
        self.pageb.pushButton_6.setEnabled(False)
        self.pageb.pushButton_9.setEnabled(False)

    def open_awg(self, ip):
        self.driver_awg = Driver(ip)
        sysparam = {
            'MixMode': self.main_ui.ip1.MixMode_param, 'RefClock': self.main_ui.ip1.RefClock_param,
            'DArate': float(self.main_ui.ip1.DArate.text()), 'KeepAmp': self.main_ui.ip1.Keep_Amp_param
        }
        try:
            self.driver_awg.open(system_parameter=sysparam)
        except Exception as e:
            self.main_ui.ip3.error_handles.tips_text.setText(str(e))
            self.main_ui.ip3.error_handles.show()

    def open_change_probe(self, ip):
        self.driver_probe = Driver(ip)
        sysparam = {
            'MixMode': self.main_ui.ip2.MixMode_param, 'RefClock': self.main_ui.ip2.RefClock_param,
            'ADrate': float(self.main_ui.ip2.ADrate.text()), 'KeepAmp': self.main_ui.ip2.Keep_Amp_param,
            'DAtare': float(self.darate[ip])
        }
        try:
            self.driver_probe.open(system_parameter=sysparam)
        except Exception as e:
            self.main_ui.ip3.error_handles.tips_text.setText(str(e))
            self.main_ui.ip3.error_handles.show()

    def open_probe(self, ip):
        self.driver_probe = Driver(ip)
        sysparam = {
            'MixMode': self.main_ui.ip2.MixMode_param, 'RefClock': self.main_ui.ip2.RefClock_param,
            'ADrate': float(self.main_ui.ip2.ADrate.text()), 'KeepAmp': self.main_ui.ip2.Keep_Amp_param
        }
        try:
            self.driver_probe.open(system_parameter=sysparam)
        except Exception as e:
            self.main_ui.ip3.error_handles.tips_text.setText(str(e))
            self.main_ui.ip3.error_handles.show()

    def config_button(self):
        self.pagea.external_trig.setEnabled(False)
        self.pagea.manual_config.clicked.connect(self.manual_config_sign)
        self.pagea.internal_config.clicked.connect(self.internal_config_sign)
        self.pagea.comboBox_2.currentIndexChanged.connect(self.trig_mode)
        self.pagea.external_config.clicked.connect(self.external_config_sign)
        self.pagea.manual_trig.clicked.connect(self.manualsign)
        self.pagea.internal_trig.clicked.connect(self.internalsign)
        self.manualcycle = self.pagea.manual_trigge_cycle.text

    def manual_config_sign(self):
        for i, data_i in self.pagea.alldata.items():
            self.driver_awg.set('Waveform', data_i, i)
            self.QSYNC_driver.set('Waveform', data_i, i)
        self.driver_awg.set('Shot', 1)
        self.driver_awg.set('StartCapture')  # 启动指令
        self.driver_awg.set('GenerateTrig', self.manualcycle())
        self.QSYNC_driver.set('Shot', 1)
        self.QSYNC_driver.set('StartCapture')  # 启动指令
        self.QSYNC_driver.set('GenerateTrig', self.manualcycle())
        self.pagea.Manual_2.setStyleSheet("background-color: rgb(167, 167, 167);")


    def internal_config_sign(self):
        for i, data_i in self.pagea.alldata.items():
            self.driver_awg.set('Waveform', data_i, i)
            self.QSYNC_driver.set('Waveform', data_i, i)
        self.driver_awg.set('Shot', self.pagea.intrigtimes)
        self.driver_awg.set('StartCapture')  # 启动指令
        self.driver_awg.set('GenerateTrig', self.pagea.intrigcycle)
        self.QSYNC_driver.set('Shot', self.pagea.intrigtimes)
        self.QSYNC_driver.set('StartCapture')  # 启动指令
        self.QSYNC_driver.set('GenerateTrig', self.pagea.intrigcycle)
        self.pagea.internal.setStyleSheet("background-color: rgb(0, 61, 184);")

    def external_config_sign(self):
        for i, data_i in self.pagea.alldata.items():
            self.driver_awg.set('Waveform', data_i, i)
            self.QSYNC_driver.set('Waveform', data_i, i)
        self.driver_awg.set('Shot', 1)
        self.driver_awg.set('StartCapture')  # 启动指令
        self.QSYNC_driver.set('Shot', 1)
        self.QSYNC_driver.set('StartCapture')  # 启动指令
        self.pagea.pushButton.setStyleSheet("background-color: rgb(255, 85, 128);")


    def internalsign(self):
        self.driver_awg = Driver(self.addr_g)
        sysparam = {
            'MixMode': self.main_ui.ip1.MixMode_param, 'RefClock': self.main_ui.ip1.RefClock_param,
            'DArate': self.main_ui.ip1.DArate.text(), 'KeepAmp': self.main_ui.ip1.Keep_Amp_param
        }
        self.driver_awg.open(system_parameter=sysparam)
        self.internal_config_sign()

    def manualsign(self):

        self.driver_awg = Driver(self.addr_g)
        sysparam = {
            'MixMode': self.main_ui.ip1.MixMode_param, 'RefClock': self.main_ui.ip1.RefClock_param,
            'DArate': self.main_ui.ip1.DArate.text(), 'KeepAmp': self.main_ui.ip1.Keep_Amp_param
        }
        self.driver_awg.open(system_parameter=sysparam)
        self.manual_config_sign()

    def trig_mode(self, i):
        if i == 1:
            self.pagea.internal_trigger()
        elif i == 2:
            self.pagea.external_trigger()
        else:
            self.pagea.Manaul_trigger()

    def init_wave(self, data, chnl):
        for i in range(chnl):
            self.pagea.waves(data)

    def action_exec_user_code(self):
        self.pagea.textEditpy.page().runJavaScript('save()', self.createpy)

    def createpy(self, pytext):
        pydata = {}
        try:
            exec(pytext, globals(), pydata)
        except Exception as e:
            print(e)

        try:
            if type(pydata['out_wave']) == dict:
                self.py_data = pydata['out_wave']
                for i, data_i in self.py_data.items():
                    self.pagea.fixwave(data_i, i)
            else:
                print("请将数据类型处理为字典。")
        except Exception as e:
            print(e)

    def config_probe_button(self):
        self.pageb.manualconfig.clicked.connect(self.manual_config)
        self.pageb.manualtrig.clicked.connect(self.manual_trig)
        self.pageb.interconfig.clicked.connect(self.inter_config)
        self.pageb.intertrig.clicked.connect(self.inter_trig)
        self.pageb.exterconfig.clicked.connect(self.exter_config)
        self.pageb.extertrig.setEnabled(False)
        self.pageb.select_file_path.clicked.connect(self.pageb.get_file)

    def manual_config(self):
        if self.pageb.MODE.currentIndex() == 0:
            for i in range(len(self.pageb.dif_chnl_list)):
                self.driver_probe.set('FrequencyList', self.pageb.dif_chnl_list[i].FrequencyList.text(), i)
                self.driver_probe.set('PhaseList', self.pageb.dif_chnl_list[i].PhaseList.text(), i)
                self.QSYNC_driver.set('FrequencyList', self.pageb.dif_chnl_list[i].FrequencyList.text(), i)
                self.QSYNC_driver.set('PhaseList', self.pageb.dif_chnl_list[i].PhaseList.text(), i)
        else:
            for i, data_i in self.pageb.numpy_data.items():
                self.driver_probe.set('FrequencyList', data_i, i)
                self.driver_probe.set('PhaseList', data_i, i)
                self.QSYNC_driver.set('FrequencyList', data_i, i)
                self.QSYNC_driver.set('PhaseList', data_i, i)

        self.driver_probe.set('StartCapture')
        self.driver_probe.set('Shot', self.pageb.shot_txt())
        self.driver_probe.set('PointNumber', self.pageb.pointnumber_txt())
        self.driver_probe.set('TriggerDelay', self.pageb.triggerdelay, 9)
        self.QSYNC_driver.set('StartCapture')
        self.QSYNC_driver.set('Shot', self.pageb.shot_txt())
        self.QSYNC_driver.set('PointNumber', self.pageb.pointnumber_txt())
        self.QSYNC_driver.set('TriggerDelay', self.pageb.triggerdelay, 9)
        self.pageb.pushButton.setStyleSheet("background-color: rgb(167, 167, 167);")

    def manual_trig(self):
        self.judge_open_probe_param(self.addr_p)
        self.manual_config()

    def inter_config(self):
        if self.pageb.MODE.currentIndex() == 0:
            for i in range(len(self.pageb.dif_chnl_list)):
                self.driver_probe.set('FrequencyList', self.pageb.dif_chnl_list[i].FrequencyList.text(), i)
                self.driver_probe.set('PhaseList', self.pageb.dif_chnl_list[i].PhaseList.text(), i)
                self.QSYNC_driver.set('FrequencyList', self.pageb.dif_chnl_list[i].FrequencyList.text(), i)
                self.QSYNC_driver.set('PhaseList', self.pageb.dif_chnl_list[i].PhaseList.text(), i)
        else:
            for i, data_i in self.pageb.numpy_data.items():
                self.driver_probe.set('FrequencyList', data_i, i)
                self.driver_probe.set('PhaseList', data_i, i)
                self.QSYNC_driver.set('FrequencyList', data_i, i)
                self.QSYNC_driver.set('PhaseList', data_i, i)
        self.driver_probe.set('StartCapture')
        self.driver_probe.set('Shot', self.pageb.shot_txt())
        self.driver_probe.set('PointNumber', self.pageb.pointnumber_txt())
        self.driver_probe.set('TriggerDelay', self.pageb.triggerdelay, 9)
        self.QSYNC_driver.set('StartCapture')
        self.QSYNC_driver.set('Shot', self.pageb.shot_txt())
        self.QSYNC_driver.set('PointNumber', self.pageb.pointnumber_txt())
        self.QSYNC_driver.set('TriggerDelay', self.pageb.triggerdelay, 9)
        self.pageb.pushButton_6.setStyleSheet("background-color: rgb(0, 61, 184);")

    def inter_trig(self):
        self.judge_open_probe_param(self.addr_p)
        self.inter_config()

    def exter_config(self):
        if self.pageb.MODE.currentIndex() == 0:
            for i in range(len(self.pageb.dif_chnl_list)):
                self.driver_probe.set('FrequencyList', self.pageb.dif_chnl_list[i].FrequencyList.text(), i)
                self.driver_probe.set('PhaseList', self.pageb.dif_chnl_list[i].PhaseList.text(), i)
                self.QSYNC_driver.set('FrequencyList', self.pageb.dif_chnl_list[i].FrequencyList.text(), i)
                self.QSYNC_driver.set('PhaseList', self.pageb.dif_chnl_list[i].PhaseList.text(), i)
        else:
            for i, data_i in self.pageb.numpy_data.items():
                self.driver_probe.set('FrequencyList', data_i, i)
                self.driver_probe.set('PhaseList', data_i, i)
                self.QSYNC_driver.set('FrequencyList', data_i, i)
                self.QSYNC_driver.set('PhaseList', data_i, i)
        self.driver_probe.set('StartCapture')
        self.driver_probe.set('Shot', self.pageb.shot_txt())
        self.driver_probe.set('PointNumber', self.pageb.pointnumber_txt())
        self.driver_probe.set('TriggerDelay', self.pageb.triggerdelay, 9)
        self.QSYNC_driver.set('StartCapture')
        self.QSYNC_driver.set('Shot', self.pageb.shot_txt())
        self.QSYNC_driver.set('PointNumber', self.pageb.pointnumber_txt())
        self.QSYNC_driver.set('TriggerDelay', self.pageb.triggerdelay, 9)
        self.pageb.pushButton_9.setStyleSheet("background-color: rgb(255, 85, 128);")

    def add_scatter(self, value):
        if value is None:
            self.x = np.random.normal(size=1024)
            self.y = np.random.normal(size=1024)
        else:
            self.value = value
        self.probes = pg.GraphicsLayoutWidget()
        self.plt2 = self.probes.addPlot()
        self.probes.setMinimumSize(0, 200)
        self.plt2.plot(self.x, self.y, pen=None, symbol='o',
                       symbolSize=1, symbolPen=(random.uniform(130, 255),
                                                random.uniform(130, 255), random.uniform(130, 255), random.uniform(130, 255)),
                       symbolBrush=(0, 0, 255, 150))
        self.pageb.gridLayout_4.addWidget(self.probes, self.a, self.b)
        self.pageb.all_data[self.i] = self.x, self.y
        self.i = self.i + 1
        self.pageb.all_waves.append(self.plt2)

    def config_QSYNC_ip(self):
        self.main_ui.ip3.exec()
        if not self.main_ui.ip3.click_ok:
            return
        if not self.check_ip(self.main_ui.ip3.ip_edit.text()):
            return
        self.OK_link_bar()


    def OK_link_bar(self):
        try:
            self.main_ui.ip3.progress_bar(self.link_progress, self.display_status)
        except Exception as e:
            self.main_ui.ip3.error_handles.tips_text.setText(str(e))
            self.main_ui.ip3.error_handles.show()
            return False

    def link_progress(self, pthread=None):
        self.QSYNC_driver = QDriver(self.main_ui.ip3.ip_edit.text())
        self.open_qsync()

    def display_status(self):
        self.main_ui.QSYNC.setStyleSheet("font: 12pt'Arial';color: #33ffcc")

    def open_qsync(self):
        try:
            self.QSYNC_driver.open()
        except Exception as e:
            self.main_ui.ip3.error_handles.tips_text.setText(str(e))
            self.main_ui.ip3.error_handles.show()
            return False

    def judge_open_probe_param(self, ip):
        if ip in self.awg_ip_list:
            self.open_change_probe(self.addr_p)
        else:
            self.open_probe(self.addr_p)

    def cnt_open_qsync(self):
        if self.main_ui.ip3.QSYNC_flag is False:
            self.config_QSYNC_ip()
            if not self.main_ui.ip3.click_ok:
                return
