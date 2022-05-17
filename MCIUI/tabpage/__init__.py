from PyQt5 import QtWidgets

from MCIUI.IP_load import IPloading
from MCIUI.tabpage.addtabpage import Ui_addtab
from MCIUI.通道波形 import wave
import pyqtgraph as pg
import numpy as np
from quantum_driver.NS_MCI import Driver


class Tabadd(QtWidgets.QWidget, Ui_addtab):
    def __init__(self, ui_parent):
        super(Tabadd, self).__init__(ui_parent)
        self.setupUi(self)
        self.ui_parent = ui_parent
        self.frame_external.hide()
        self.frame_internal.hide()
        self.changepy.clicked.connect(self.createpy)
        self.i = 0

        self.external_trig.setEnabled(False)
        self.manual_config.clicked.connect(self.manual_config_sign)
        self.internal_config.clicked.connect(self.internal_config_sign)
        self.comboBox_2.currentIndexChanged.connect(self.trig_mode)
        self.external_config.clicked.connect(self.externalsign)
        self.manual_trig.clicked.connect(self.manualsign)
        self.internal_trig.clicked.connect(self.internalsign)
        self.intrigtimes = self.repeat_times_2.text()
        self.intrigcycle = self.trigger_cycle.text()
        self.manualcycle = self.manual_trigge_cycle.text()
        self.pytext = self.textEditpy.toPlainText()

        self.tabadd = self.frame_19
        self.ip1 = IPloading(self)
        self.ip1.exec()
        self.ip = self.ip1.IPlineEdit.text()

        self.driver = Driver(self.ip)
        sysparam = {
            'MixMode': 2, 'RefClock': 'out', 'DAC抽取倍数': 1, 'DAC本振频率': 0  # , 'DArate': 4e9
        }
        self.driver.open(system_parameter=sysparam)

        self.alldata = []
        for i in range(24):
            self.waves()

    def waves(self):
        # self.date1 = value
        waveui = wave(self)
        self.param1 = 12
        self.param2 = 23
        self.chnlname = 'chnl-' + str(self.i)
        self.i = self.i + 1
        waveui.chnl_0.setText(self.chnlname)
        self.plot_win = pg.GraphicsLayoutWidget(self)
        self.p1 = self.plot_win.addPlot()
        self.data1 = np.random.normal(size=300)
        self.alldata.append(self.data1)
        self.curve1 = self.p1.plot(self.data1)
        self.data2 = '参数1：{}，参数2：{}'.format(self.param1, self.param2)
        self.p1.setLabel('top', self.data2)
        waveui.verticalLayout.addWidget(self.plot_win)
        self.verticalLayout.addWidget(waveui)

        def update1():
            self.data1[:-1] = self.data1[1:]
            self.data1[-1] = np.random.normal()
            self.curve1.setData(self.data1)

        def update():
            update1()

        timer = pg.QtCore.QTimer()
        timer.timeout.connect(update)
        timer.start(50)

    def trig_mode(self, i):
        if i == 1:
            self.internal_trigger()
        elif i == 2:
            self.external_trigger()
        else:
            self.Manaul_trigger()

    def external_trigger(self):
        self.frame_external.show()
        self.frame_internal.hide()
        self.frame_manual.hide()

    def internal_trigger(self):
        self.frame_internal.show()
        self.frame_external.hide()
        self.frame_manual.hide()

    def Manaul_trigger(self):
        self.frame_manual.show()
        self.frame_external.hide()
        self.frame_internal.hide()

    def manual_config_sign(self):
        for i in range(24):
            self.driver.set('Waveform', self.alldata[i], i + 1)
        self.driver.set('Shot', 1)
        self.driver.set('StartCapture')  # 启动指令
        self.driver.set('GenerateTrig', self.manualcycle)

    def internal_config_sign(self):
        for i in range(24):
            self.driver.set('Waveform', self.alldata[i], i + 1)
        self.driver.set('Shot', self.intrigtimes)
        self.driver.set('StartCapture')  # 启动指令
        self.driver.set('GenerateTrig', self.intrigcycle)

    def externalsign(self):
        for i in range(24):
            self.driver.set('Waveform', self.alldata[i], i + 1)
        self.driver.set('Shot', 1)

    def internalsign(self):
        self.driver = Driver(self.ip)
        sysparam = {
            'MixMode': 2, 'RefClock': 'in', 'DAC抽取倍数': 1, 'DAC本振频率': 0  # , 'DArate': 4e9
        }
        self.driver.open(system_parameter=sysparam)
        self.internal_config_sign()

    def manualsign(self):

        self.driver = Driver(self.ip)
        sysparam = {
            'MixMode': 2, 'RefClock': 'in', 'DAC抽取倍数': 1, 'DAC本振频率': 0  # , 'DArate': 4e9
        }

        self.driver.open(system_parameter=sysparam)
        self.internal_config_sign()
        self.manual_config_sign()

    def createpy(self):
        self.inputdata = exec(compile(self.pytext))
        for i in range(len(self.inputdata)):
            self.waves(self.inputdata[i])
