from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from MCIUI.tab_probe.probe_page import Ui_Form
from quantum_driver.NS_MCI import Driver
import pyqtgraph as pg
import numpy as np


class probe_wave(QtWidgets.QWidget, Ui_Form):
    def __init__(self, ui_parent, ip):
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
        self.all_waves = []
        self.txt = []
        self.i = 0
        from MCIUI.main_widget import MAIN
        mainui = MAIN(ui_parent=None)
        if self.ip in mainui.ip_list:
            pass

        for i in range(12):
            self.a = int(i / 4)
            self.b = int(i % 4)
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

    def manual_config(self):
        # if self.MODE.currentIndex() == 0:
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
        for i, data_i in self.all_data.items():
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
        for i, data_i in self.all_data.items():
            self.driver.set('FrequencyList', data_i, i)
            self.driver.set('PhaseList', data_i, i)
        self.driver.set('StartCapture')
        self.driver.set('Shot', self.shot_txt())
        self.driver.set('PointNumber', self.pointnumber_txt())
        self.driver.set('TriggerDelay', self.triggerdelay, 9)

    def get_file(self):
        fname = QFileDialog.getOpenFileName(self, '打开文件', './')
        if fname[0]:
            with open(fname[0], 'r', encoding='gb18030', errors='ignore') as f:
                self.txt.append(f.read())
        self.file_path.setText(str(fname[0]))

    def add_probe(self, value=None):
        if value is None:
            self.x = np.random.normal(size=1024)
            self.y = np.random.normal(size=1024)
        else:
            self.value = value
        self.probes = pg.GraphicsLayoutWidget()
        self.plt2 = self.probes.addPlot()
        self.probes.setMinimumSize(0, 200)
        self.plt2.plot(self.x, self.y, pen=None, symbol='o', symbolSize=1, symbolPen=(255, 255, 255, 200),
                       symbolBrush=(0, 0, 255, 150))
        self.gridLayout_4.addWidget(self.probes, self.a, self.b)
        self.all_data[self.i] = self.x, self.y
        self.i = self.i + 1
        self.all_waves.append(self.probes)

    def add_plot(self, add_data, number):
        self.add_data = add_data

        self.all_waves[number].plt2.plot(self.x, self.y, pen=None, symbol='o', symbolSize=1,
                                         symbolPen=(155, 200, 160, 200),
                                         symbolBrush=(0, 0, 255, 150))
