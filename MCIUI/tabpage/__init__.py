import os
from PyQt5 import QtWidgets, QtCore, QtGui

from MCIUI.tabpage.addtabpage import Ui_addtab
from MCIUI.通道波形 import wave
import numpy as np
from quantum_driver.NS_MCI import Driver


class Tabadd(QtWidgets.QWidget, Ui_addtab):
    def __init__(self, ui_parent, ip):
        super(Tabadd, self).__init__(ui_parent)
        self.setupUi(self)
        self.ip = ip
        self.ui_parent = ui_parent
        self.frame_external.hide()
        self.frame_internal.hide()
        self.changepy.clicked.connect(self.action_exec_user_code)
        self.i = 0

        # 配置控制按钮
        self.external_trig.setEnabled(False)
        self.manual_config.clicked.connect(self.manual_config_sign)
        self.internal_config.clicked.connect(self.internal_config_sign)
        self.comboBox_2.currentIndexChanged.connect(self.trig_mode)
        self.external_config.clicked.connect(self.externalsign)
        self.manual_trig.clicked.connect(self.manualsign)
        self.internal_trig.clicked.connect(self.internalsign)
        self.manualcycle = self.manual_trigge_cycle.text

        self.driver = Driver(self.ip)
        sysparam = {
            'MixMode': 2, 'RefClock': 'out', 'DAC抽取倍数': 1, 'DAC本振频率': 0  # , 'DArate': 4e9
        }
        self.driver.open(system_parameter=sysparam)

        self.alldata = {}
        self.allwave = []
        # self.pydata = {}
        for i in range(10):
            self.waves()

    # 初始化波形
    def init_wave(self, data, chnl):
        for i in range(chnl):
            self.waves(data)

    # 给python编译器增加关键字高亮
    def setupUi(self, addtab):
        super(Tabadd, self).setupUi(addtab)
        self.textEditpy.load(
            QtCore.QUrl('file:///' + os.path.abspath('./MCIUI/tabpage/static/index.html').replace('\\', '/')))
        # QtWidgets.QApplication.instance.processEvent()

    # def showEvent(self, a0: QtGui.QShowEvent) -> None:
    #     if self.j == 0:
    #         self.j = self.j + 1
    #         self.textEditpy.reload()
    #     super(Tabadd, self).showEvent(a0)

    @property
    def intrigcycle(self):
        return self.trigger_cycle.text()

    @property
    def intrigtimes(self):
        return self.repeat_times_2.text()

    def action_exec_user_code(self):
        self.textEditpy.page().runJavaScript('save()', self.createpy)

    # awg页面波形控件调用展示波形
    def waves(self, value=None):
        value = np.random.normal(size=300) if value is None else value
        waveui = wave(self)
        self.chnlname = 'chnl-' + str(self.i)
        self.i = self.i + 1
        waveui.chnl_0.setText(self.chnlname)
        self.data1 = value
        self.alldata[self.chnlname] = self.data1
        self.curve1 = waveui.p1.plot(self.data1)
        self.verticalLayout.addWidget(waveui)
        self.allwave.append(waveui)

    def trig_mode(self, i):
        if i == 1:
            self.internal_trigger()
        elif i == 2:
            self.external_trigger()
        else:
            self.Manaul_trigger()

    # 配置按照模式显示不同的配置指令
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
        self.driver.set('StartCapture')  # 启动指令


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
                    self.fixwave(data_i, i)
            else:
                print("请将数据类型处理为字典。")
        except Exception as e:
            print(e)

    def fixwave(self, fix_data, chnls):
        self.allwave[chnls].p1.plot(fix_data, clear=True)
