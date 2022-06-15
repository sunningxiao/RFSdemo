import os

from PyQt5 import QtWidgets, QtCore
from MCIUI.awg页面.addtabpage import Ui_addtab
from MCIUI.通道波形 import Chnl_wave
import numpy as np


class Awg_widget(QtWidgets.QWidget, Ui_addtab):
    def __init__(self, ui_parent, ip):
        super(Awg_widget, self).__init__()
        self.setupUi(self)
        self.ip = ip
        self.ui_parent = ui_parent
        self.frame_external.hide()
        self.frame_internal.hide()
        self.i = 0
        self.alldata = {}
        self.allwave = []

    def setupUi(self, addtab):
        super(Awg_widget, self).setupUi(addtab)
        self.textEditpy.load(
            QtCore.QUrl('file:///' + os.path.abspath('./MCIUI/awg页面/static/index.html').replace('\\', '/')))

    @property
    def intrigcycle(self):
        return self.trigger_cycle.text()

    @property
    def intrigtimes(self):
        return self.repeat_times_2.text()

    # awg页面波形控件调用展示波形
    def waves(self, value=None):
        value = np.random.normal(size=300) if value is None else value
        waveui = Chnl_wave(self)
        self.chnlname = 'chnl-' + str(self.i)
        self.i = self.i + 1
        waveui.chnl_0.setText(self.chnlname)
        self.data1 = value
        self.alldata[self.chnlname] = self.data1
        self.curve1 = waveui.p1.plot(self.data1, pen=(115, 135, 116))
        self.verticalLayout.addWidget(waveui)
        self.allwave.append(waveui)

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

    def fixwave(self, fix_data, chnls):
        self.allwave[chnls].p1.plot(fix_data, pen=(115, 135, 116), clear=True)
