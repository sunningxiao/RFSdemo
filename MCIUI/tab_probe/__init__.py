from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog
import sys
from MCIUI.tab_probe.probe_page import Ui_Form
import qdarkstyle
from quantum_driver.NS_MCI import Driver
import pyqtgraph as pg
import numpy as np


class probe_wave(QtWidgets.QWidget, Ui_Form):
    def __init__(self, ui_parent, ip=None):
        super(probe_wave, self).__init__(ui_parent)
        self.setupUi(self)
        self.ui_parent = ui_parent
        self.widget_internal.hide()
        self.widget_external.hide()
        self.Trig_Mode.currentIndexChanged.connect(self.trig_mode)
        self.shot_txt = self.shots.text
        self.pointnumber_txt = self.PointNumber.text
        self.triggerdelay_txt = self.triggerdelay.text
        self.frequencylist_txt = self.FrequencyList.text
        self.Phase_txt = self.Phase.text
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

        for i in range(12):
            self.a = int(i / 4)
            self.b = int(i % 4)
            self.add_probe()

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

    def manual_config(self):
        for i, data_i in self.all_data.items():
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
        pass

    def inter_trig(self):
        self.driver = Driver(self.ip)
        sysparam = {
            'MixMode': 2, 'RefClock': 'in', 'DAC抽取倍数': 1, 'DAC本振频率': 0  # , 'DArate': 4e9
        }
        self.driver.open(system_parameter=sysparam)
        self.inter_config()

    def exter_config(self):
        pass

    def get_file(self):

        my_file_path = QFileDialog.getOpenFileName(None, '选择文件', r'C:', "")
        with open(my_file_path[0]) as f:
            my_file = f.read()
        self.t.setText(my_file)


    def add_probe(self):
        self.probes = pg.GraphicsLayoutWidget()
        plt2 = self.probes.addPlot()
        self.probes.setMinimumSize(0, 200)
        self.x = np.random.normal(size=50)
        self.y = np.random.normal(size=50)
        plt2.plot(self.x, self.y, pen=None, symbol='o', symbolSize=5, symbolPen=(255,255,255,200), symbolBrush=(0,0,255,150))
        self.gridLayout_4.addWidget(self.probes, self.a, self.b)


