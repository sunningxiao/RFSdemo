import random

import numpy
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog

from MCIUI.chnl_mode_list import Chnls_list
from MCIUI.tab_probe.probe_page import Ui_Form
from quantum_driver.NS_MCI import Driver
import pyqtgraph as pg
import numpy as np


class Probe_wave(QtWidgets.QWidget, Ui_Form):
    def __init__(self, ui_parent, ip):
        super(Probe_wave, self).__init__()
        self.setupUi(self)
        self.ui_parent = ui_parent
        self.widget_internal.hide()
        self.widget_external.hide()
        self.Trig_Mode.currentIndexChanged.connect(self.trig_mode)
        self.shot_txt = self.shots.text
        self.pointnumber_txt = self.PointNumber.text
        self.triggerdelay_txt = self.triggerdelay.text
        # self.frequencylist_txt = self.FrequencyList.text
        # self.Phase_txt = self.Phase.text
        self.MODE.currentIndexChanged.connect(self.mode)
        self.MODE2.hide()

        # 信号槽链接

        self.manualconfig.clicked.connect(self.manual_config)
        self.manualtrig.clicked.connect(self.manual_trig)
        self.interconfig.clicked.connect(self.inter_config)
        self.intertrig.clicked.connect(self.inter_trig)
        self.exterconfig.clicked.connect(self.exter_config)
        self.extertrig.setEnabled(False)
        self.select_file_path.clicked.connect(self.get_file)

        self.ip = ip
        self.driver = Driver(self.ip)
        sysparam = {
            'MixMode': 2, 'RefClock': 'out', 'DAC抽取倍数': 1, 'DAC本振频率': 0  # , 'DArate': 4e9
        }
        self.driver.open(system_parameter=sysparam)
        self.all_data = {}
        self.all_waves = []
        self.numpy_data = {}
        self.dif_chnl_list = []
        self.i = 0
        self.tabWidget.removeTab(0)
        self.tabWidget.removeTab(0)
        # self.initprobe()

        for i in range(12):
            self.mode_list = Chnls_list(self)
            self.mode_add = QtWidgets.QWidget(self)
            awg_layout = QtWidgets.QGridLayout(self.mode_add)
            awg_layout.addWidget(self.mode_list)
            awg_layout.setContentsMargins(0, 0, 0, 0)
            self.tabname = 'chnl-' + str(i)
            self.mode_add.setObjectName("mode_chnls")
            self.tabWidget.addTab(self.mode_add, '{}'.format(self.tabname))
            self.dif_chnl_list.append(self.mode_list)

        for i in range(12):
            self.a = int(i / 3)
            self.b = int(i % 3)
            self.add_probe(None)


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

    # 控制按钮调用driver，参数配置

    def manual_config(self):
        if self.MODE.currentIndex() == 0:
            for i in range(len(self.dif_chnl_list)):
                self.driver.set('FrequencyList', self.dif_chnl_list[i].FrequencyList.text(), i)
                self.driver.set('PhaseList', self.dif_chnl_list[i].PhaseList.text(), i)
        else:
            for i, data_i in self.numpy_data.items():
                self.driver.set('FrequencyList', data_i, i)
                self.driver.set('PhaseList', data_i, i)

        self.driver.set('StartCapture')
        self.driver.set('Shot', self.shot_txt())
        self.driver.set('PointNumber', self.pointnumber_txt())
        self.driver.set('TriggerDelay', self.triggerdelay, 9)

    def manual_trig(self):
        self.driver = Driver(self.ip)
        sysparam = {
            'MixMode': 2, 'RefClock': 'in', 'DAC抽取倍数': 1, 'DAC本振频率': 0  # , 'DArate': 4e9
        }

        self.driver.open(system_parameter=sysparam)
        self.manual_config()

    def inter_config(self):
        if self.MODE.currentIndex() == 0:
            for i in range(len(self.dif_chnl_list)):
                self.driver.set('FrequencyList', self.dif_chnl_list[i].FrequencyList.text(), i)
                self.driver.set('PhaseList', self.dif_chnl_list[i].PhaseList.text(), i)
        else:
            for i, data_i in self.numpy_data.items():
                self.driver.set('FrequencyList', data_i, i)
                self.driver.set('PhaseList', data_i, i)
        self.driver.set('StartCapture')
        self.driver.set('Shot', self.shot_txt())
        self.driver.set('PointNumber', self.pointnumber_txt())
        self.driver.set('TriggerDelay', self.triggerdelay, 9)

    def inter_trig(self):
        self.driver = Driver(self.ip)
        sysparam = {
            'MixMode': 2, 'RefClock': 'in', 'DAC抽取倍数': 1, 'DAC本振频率': 0  # , 'DArate': 4e9
        }
        self.driver.open(system_parameter=sysparam)
        self.inter_config()

    def exter_config(self):
        if self.MODE.currentIndex() == 0:
            for i in range(len(self.dif_chnl_list)):
                self.driver.set('FrequencyList', self.dif_chnl_list[i].FrequencyList.text(), i)
                self.driver.set('PhaseList', self.dif_chnl_list[i].PhaseList.text(), i)
        else:
            for i, data_i in self.numpy_data.items():
                self.driver.set('FrequencyList', data_i, i)
                self.driver.set('PhaseList', data_i, i)
        self.driver.set('StartCapture')
        self.driver.set('Shot', self.shot_txt())
        self.driver.set('PointNumber', self.pointnumber_txt())
        self.driver.set('TriggerDelay', self.triggerdelay, 9)

    # 从文件中读取FrequencyList和PhaseList

    def get_file(self):
        fname = QFileDialog.getOpenFileName(self, '打开文件', './')
        if fname[0]:
            # with open(fname[0], 'r', encoding='gb18030', errors='ignore') as f:
            self.numpy_data.append(numpy.load(fname[0]))
        self.file_path.setText(str(fname[0]))

    # probe页面实例化波形斑图控件并添加图层

    def add_probe(self, value):
        if value is None:
            self.x = np.random.normal(size=1024)
            self.y = np.random.normal(size=1024)
        else:
            self.value = value
        self.probes = pg.GraphicsLayoutWidget()
        self.plt2 = self.probes.addPlot()
        self.probes.setMinimumSize(0, 200)
        self.plt2.plot(self.x, self.y, pen=None, symbol='o', symbolSize=1, symbolPen=(random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255)),
                       symbolBrush=(0, 0, 255, 150))
        self.gridLayout_4.addWidget(self.probes, self.a, self.b)
        self.all_data[self.i] = self.x, self.y
        self.i = self.i + 1
        self.all_waves.append(self.probes)

    # 通过波形控件添加图像对比效果

    def add_plot(self, add_data, number):
        self.add_data = add_data
        for i in range(len(self.add_data)):
            self.x.append(self.add_data[i][0])
            self.y.append(self.add_data[i][1])

        self.all_waves[number].plt2.plot(self.x, self.y, pen=None, symbol='o', symbolSize=1,
                                         symbolPen=(random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255)),
                                         symbolBrush=(0, 0, 255, 150))


