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
        self.manualcycle = self.manual_trigge_cycle.text

        self.tabadd = self.frame_19
        self.ip1 = IPloading(self)
        self.ip1.exec()
        self.ip = self.ip1.IPlineEdit.text
        self.driver = Driver(self.ip())
        sysparam = {
            'MixMode': 2, 'RefClock': 'out', 'DAC抽取倍数': 1, 'DAC本振频率': 0  # , 'DArate': 4e9
        }
        self.driver.open(system_parameter=sysparam)

        self.alldata = {}
        self.allwave = []
        #self.pydata = {}
        # for i in range(24):
        #     self.waves()


    @property
    def intrigcycle(self):
        return self.trigger_cycle.text()

    @property
    def intrigtimes(self):
        return self.repeat_times_2.text()

    @property
    def pytext(self):
        return self.textEditpy.toPlainText()

    def waves(self, value=None, tabname=None):
        value = np.random.normal(size=300) if value is None else value
        waveui = wave(self)
        self.param1 = 12
        self.param2 = 23
        self.chnlname = 'chnl-' + str(self.i)
        self.i = self.i + 1
        waveui.chnl_0.setText(self.chnlname)
        self.plot_win = pg.GraphicsLayoutWidget(self)
        self.p1 = self.plot_win.addPlot()
        self.data1 = value
        self.alldata[self.chnlname] = self.data1
        self.curve1 = self.p1.plot(self.data1)
        self.data2 = '参数1：{}，参数2：{}'.format(self.param1, self.param2)
        self.p1.setLabel('top', self.data2)
        waveui.verticalLayout.addWidget(self.plot_win)
        self.verticalLayout.addWidget(waveui)

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
        for i, data_i in self.alldata.items():
            self.driver.set('Waveform', data_i, i)
        self.driver.set('Shot', 1)
        self.driver.set('StartCapture')  # 启动指令
        self.driver.set('GenerateTrig', self.manualcycle())

    def internal_config_sign(self):
        for i, data_i in self.alldata.items():
            self.driver.set('Waveform', data_i, i)
        self.driver.set('Shot', self.intrigtimes)
        self.driver.set('StartCapture')  # 启动指令
        self.driver.set('GenerateTrig', self.intrigcycle)

    def externalsign(self):
        for i, data_i in self.alldata.items():
            self.driver.set('Waveform', data_i, i)
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
        self.manual_config_sign()

    def createpy(self):
        pydata = {}
        try:
            exec(self.pytext, globals(), pydata)
        except Exception as e:
            print(e)

        try:
            if type(pydata['out_wave']) == dict:
                self.py_data = pydata['out_wave']
                for i, data_i in self.py_data.items():
                    self.waves(data_i, i)

            else:
                print("请将数据类型处理为字典。")
        except Exception as e:
            print(e)
