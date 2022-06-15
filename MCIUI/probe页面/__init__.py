import random

import numpy
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog

from MCIUI.多通道频率相位 import Chnls_list
from MCIUI.probe页面.probe_page import Ui_Form
import numpy as np


class Probe_widget(QtWidgets.QWidget, Ui_Form):
    def __init__(self, ui_parent, ip):
        super(Probe_widget, self).__init__()
        self.setupUi(self)
        self.ui_parent = ui_parent
        self.widget_internal.hide()
        self.widget_external.hide()
        self.Trig_Mode.currentIndexChanged.connect(self.trig_mode)
        self.shot_txt = self.shots.text
        self.pointnumber_txt = self.PointNumber.text
        self.triggerdelay_txt = self.triggerdelay.text
        self.MODE.currentIndexChanged.connect(self.mode)
        self.MODE2.hide()

        self.all_data = {}
        self.all_waves = []
        self.numpy_data = {}
        self.dif_chnl_list = []
        self.i = 0
        self.tabWidget.removeTab(0)
        self.tabWidget.removeTab(0)
        self.x = []
        self.y = []
        # self.initprobe()
        self.q1 = np.random.normal(size=1024)+10
        self.q2 = np.random.normal(size=1024)+5

        for i in range(20):
            self.mode_list = Chnls_list(self)
            self.mode_add = QtWidgets.QWidget(self)
            awg_layout = QtWidgets.QGridLayout(self.mode_add)
            awg_layout.addWidget(self.mode_list)
            awg_layout.setContentsMargins(0, 0, 0, 0)
            self.tabname = 'chnl-' + str(i)
            self.mode_add.setObjectName("mode_chnls")
            self.tabWidget.addTab(self.mode_add, '{}'.format(self.tabname))
            self.dif_chnl_list.append(self.mode_list)

    def mode(self, i):
        if i == 1:
            self.mode_2()
        else:
            self.mode_1()

    def mode_1(self):
        self.MODE1.show()
        self.MODE2.hide()

    def mode_2(self):
        self.MODE2.show()
        self.MODE1.hide()

    def trig_mode(self, i):
        if i == 1:
            self.inter_trigger()
        elif i == 2:
            self.exter_trigger()
        else:
            self.manual_trigger()

    def manual_trigger(self):
        self.widget_manual.show()
        self.widget_external.hide()
        self.widget_internal.hide()

    def inter_trigger(self):
        self.widget_internal.show()
        self.widget_external.hide()
        self.widget_manual.hide()

    def exter_trigger(self):
        self.widget_external.show()
        self.widget_manual.hide()
        self.widget_internal.hide()

    def get_file(self):
        fname = QFileDialog.getOpenFileName(self, '打开文件', './')
        if fname[0]:
            # with open(fname[0], 'r', encoding='gb18030', errors='ignore') as f:
            self.numpy_data.append(numpy.load(fname[0]))
        self.file_path.setText(str(fname[0]))


    def add_plot(self, number):
        # self.add_data = add_data
        # for i in range(len(self.add_data)):
        #     self.x.append(self.add_data[i][0])
        #     self.y.append(self.add_data[i][1])
        self.all_waves[number].plot(self.q1, self.q2, pen=None, symbol='o', symbolSize=1,
                                         symbolPen=(
                                             random.uniform(130, 255), random.uniform(130, 255), random.uniform(130, 255),
                                             random.uniform(130, 255)),
                                         symbolBrush=(0, 0, 255, 150))
        self.x = []
        self.y = []

