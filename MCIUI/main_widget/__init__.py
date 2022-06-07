import re

from PyQt5 import QtWidgets, QtGui

from MCIUI.IP_probe import IPprobe
from MCIUI.tab_probe import Probe_wave
from MCIUI.tabpage import Addawg
from MCIUI.IP_load import IPloading
from MCIUI.main_widget.frame import Ui_Form


class MAIN(QtWidgets.QWidget, Ui_Form):
    def __init__(self, ui_parent):
        super(MAIN, self).__init__()
        self.setupUi(self)
        self.ui_parent = ui_parent
        self.tab.removeTab(0)
        self.tab.removeTab(0)
        self.page_dic = {}
        self.i = 0
        self.j = 0
        self.k = 0
        self.awg_ip_list = []
        self.probe_ip_list = []
        # 插入logo
        self.frame_25.hide()
        pixmap = QtGui.QPixmap("MCIUI/static/img.png").scaled(self.picture.width(), self.picture.height())
        self.picture.setPixmap(pixmap)
        self.picture.setScaledContents(True)

        self.btn_close.clicked.connect(self.close)
        self.btn_min.clicked.connect(self.showMinimized)
        self.btn_max.clicked.connect(self.max_func)

    # 点击按钮尺寸缩放
    def max_func(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    # 根据IP增加主页面下awg页面，不允许同IP打开多个页面

    def addawg(self):
        self.ip1 = IPloading(self)
        self.addr = self.ip1.IPlineEdit.text
        self.ip1.exec()
        if not self.ip1.click_ok:
            return

        self.tabname = 'AWG-' + str(self.i)
        if self.addr() in self.awg_ip_list:
            print("已经打开相同IP的AWG页面")
            return
        self.check_ip(self.addr())
        self.pagea = Addawg(self, self.addr())
        self.awg_ip_list.append(self.addr())
        self.AWGADD = QtWidgets.QWidget(self)
        awg_layout = QtWidgets.QGridLayout(self.AWGADD)
        awg_layout.addWidget(self.pagea)
        awg_layout.setContentsMargins(0, 0, 0, 0)
        self.AWGADD.setObjectName("AWGADD")
        self.tab.addTab(self.AWGADD, '{}'.format(self.tabname))
        self.tab.setCurrentIndex(self.k)
        self.page_dic[self.addr()] = self.pagea
        if self.addr() in self.probe_ip_list:
            self.page_dic[self.addr()].manual_config.setEnabled(False)
            self.page_dic[self.addr()].manual_trig.setEnabled(False)
            self.page_dic[self.addr()].external_config.setEnabled(False)
            self.page_dic[self.addr()].external_trig.setEnabled(False)
            self.page_dic[self.addr()].internal_config.setEnabled(False)
            self.page_dic[self.addr()].internal_trig.setEnabled(False)
        self.i = self.i + 1
        self.k = self.k + 1

    # 判断IP地址是否合法

    def check_ip(self, ip):
        compile_ip = re.compile(
            '^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
        if compile_ip.match(ip):
            return True
        else:
            self.ip1.exit(0) or self.ip2.exit(1)

    # 根据IP地址增加probe页面，同IP只可打开一个界面，当前界面下有同IP的awg页面的情况下将awg页面的配置按钮设置为不可用

    def addprobe(self):
        self.ip2 = IPprobe(self)
        self.ip2.exec()
        self.addr_P = self.ip2.ipaddr.text
        if not self.ip2.click_ok:
            return
        self.check_ip(self.addr_P())
        if self.addr_P() in self.probe_ip_list:
            print("已经打开相同IP的probe页面")
            return
        if self.addr_P() in self.awg_ip_list:  # 判断输入ip是否在列表中
            self.getdata = self.page_dic[self.addr_P()].alldata  # 前面将IP：tab页面内容存在字典page_dic中 想直接通过这个字典获取响应页面的alldata
            self.page_dic[self.addr_P()].manual_config.setEnabled(False)
            self.page_dic[self.addr_P()].manual_trig.setEnabled(False)
            self.page_dic[self.addr_P()].external_config.setEnabled(False)
            self.page_dic[self.addr_P()].external_trig.setEnabled(False)
            self.page_dic[self.addr_P()].internal_config.setEnabled(False)
            self.page_dic[self.addr_P()].internal_trig.setEnabled(False)

        self.tabname1 = 'Probe-' + str(self.j)
        self.pageb = Probe_wave(self, self.addr_P())
        self.probe_ip_list.append(self.addr_P())
        self.AWGProbe = QtWidgets.QWidget(self)
        awg_layout1 = QtWidgets.QGridLayout(self.AWGProbe)
        awg_layout1.addWidget(self.pageb)
        awg_layout1.setContentsMargins(0, 0, 0, 0)
        self.AWGProbe.setObjectName("AWGProbe")
        self.tab.addTab(self.AWGProbe, '{}'.format(self.tabname1))
        self.tab.setCurrentIndex(self.k)
        self.j = self.j + 1
        self.k = self.k + 1
