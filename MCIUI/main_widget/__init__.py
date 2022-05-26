from PyQt5 import QtWidgets, QtGui

from MCIUI.IP_probe import IPprobe
from MCIUI.tab_probe import probe_wave
from MCIUI.tabpage import Tabadd
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

        pix = QtGui.QPixmap("static/img.png")
        self.picture.setPixmap(pix)
        self.picture.setScaledContents(True)

        '''
        pixmap = QtGui.QPixmap("static/img.png").scaled(self.picture.width(), self.picture.height())
        self.picture.setPixmap(pixmap)
        '''

    def addawg(self):
        self.ip1 = IPloading(self)
        self.ip1.exec()
        self.addr = self.ip1.IPlineEdit.text
        if not self.ip1.click_ok:
            return
        self.tabname = 'AWG-' + str(self.i)
        if self.addr() in self.awg_ip_list:
            print("已经打开相同IP的AWG页面")
            return
        self.pagea = Tabadd(self, self.addr())
        self.awg_ip_list.append(self.addr())
        self.AWGADD = QtWidgets.QWidget(self)
        awg_layout = QtWidgets.QGridLayout(self.AWGADD)
        awg_layout.addWidget(self.pagea)
        awg_layout.setContentsMargins(0, 0, 0, 0)
        self.AWGADD.setObjectName("AWGADD")
        self.tab.addTab(self.AWGADD, '{}'.format(self.tabname))
        self.tab.setCurrentIndex(self.k)
        self.page_dic[self.addr()] = self.pagea
        self.i = self.i + 1
        self.k = self.k + 1


    def addprobe(self):
        self.ip2 = IPprobe(self)
        self.ip2.exec()
        self.addr_P = self.ip2.ipaddr.text
        if not self.ip2.click_ok:
            return
        if self.addr_P() in self.awg_ip_list:  # 判断输入ip是否在列表中
            self.getdata= self.page_dic[self.addr_P()].alldata  # 前面将IP：tab页面内容存在字典page_dic中 想直接通过这个字典获取响应页面的alldata
            self.page_dic[self.addr_P()].manual_config.setEnabled(False)
            self.page_dic[self.addr_P()].manual_trig.setEnabled(False)
            self.page_dic[self.addr_P()].external_config.setEnabled(False)
            self.page_dic[self.addr_P()].external_trig.setEnabled(False)
            self.page_dic[self.addr_P()].internal_config.setEnabled(False)
            self.page_dic[self.addr_P()].internal_trig.setEnabled(False)


        self.tabname1 = 'Probe-' + str(self.j)
        self.pageb = probe_wave(self, self.addr_P())
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

