import sys
import re

import qdarkstyle
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

from MCIUI.main_widget import MAIN
from MCIUI.tabpage import Addawg
from MCIUI.tab_probe import Probe_wave
from MCIUI.IP_probe import IPprobe
from MCIUI.IP_load import IPloading

class ConfigWidget:

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_ui = MAIN()
        self.main_ui.Connect_AWG.clicked.connect(self.add_awg)
        self.main_ui.Connect_Probe_2.clicked.connect(self.add_probe)
        self.i = 0
        self.j = 0
        self.k = 0
        self.awg_ip_list = []
        self.probe_ip_list = []
        self.page_dic = {}

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
        self.main_ui.ip1.IPlineEdit.clear()
        if not self.check_ip(addr):
            return
        self.add_awg_function(addr)

    def add_probe(self):
        self.main_ui.ip2.exec()
        if not self.main_ui.ip2.click_ok:
            return
        addr = self.main_ui.ip2.ipaddr.text()
        self.main_ui.ip2.ipaddr.clear()
        if not self.check_ip(addr):
            return
        self.add_probe_function(addr)

    def run_ui(self):
        self.app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.main_ui.show()
        sys.exit(self.app.exec())

    def add_awg_function(self, addr):
        self.tabname = 'AWG-' + str(self.i)
        if addr in self.awg_ip_list:
            print("已经打开相同IP的AWG页面")
            return
        self.pagea = Addawg(self, addr)
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
        self.i = self.i + 1
        self.k = self.k + 1

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

        self.tabname1 = 'Probe-' + str(self.j)
        self.pageb = Probe_wave(self, addr)
        self.probe_ip_list.append(addr)
        self.AWGProbe = QtWidgets.QWidget()
        awg_layout1 = QtWidgets.QGridLayout(self.AWGProbe)
        awg_layout1.addWidget(self.pageb)
        awg_layout1.setContentsMargins(0, 0, 0, 0)
        self.AWGProbe.setObjectName("AWGProbe")
        self.main_ui.tab.addTab(self.AWGProbe, '{}'.format(self.tabname1))
        self.main_ui.tab.setCurrentIndex(self.k)
        self.j = self.j + 1
        self.k = self.k + 1


