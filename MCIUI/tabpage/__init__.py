from PyQt5 import QtWidgets
from MCIUI.tabpage.addtabpage import Ui_addtab
from MCIUI.通道波形 import wave
import pyqtgraph as pg
import numpy as np
from quantum_driver.NS_MCI import Driver


class Tabadd(QtWidgets.QWidget, Ui_addtab):
    def __init__(self, ui_parent):
        super(Tabadd, self).__init__(ui_parent)
        self.i = 0
        self.setupUi(self)
        self.ui_parent = ui_parent

        self.frame_2.hide()
        self.frame_4.hide()
        self.comboBox_2.currentIndexChanged.connect(self.trig_mode)
        self.pushButton_2.clicked.connect(self.externalsign)
        self.Trig_2.clicked.connect(self.manualsign)
        self.trig_2.clicked.connect(self.internalsign)
        self.pushButton_4.clicked.connect(self.createpy)

        self.intrigtimes = self.repeat_times_2.text()
        self.intrigcycle = self.trigger_cycle.text()
        self.manualcycle = self.lineEdit_2.text()
        self.tabadd = self.frame_19
        for i in range(24):
            self.waves()

    def waves(self):
        # self.date1 = value
        waveui = wave(self)
        self.param1 = 12
        self.param2 = 23
        waveui.chnl_0.setText('chnl_0')
        self.plot_win = pg.GraphicsLayoutWidget(self)
        self.p1 = self.plot_win.addPlot()
        self.data1 = np.random.normal(size=300)
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
        self.frame_2.show()
        self.frame_4.hide()
        self.frame_38.hide()

    def internal_trigger(self):
        self.frame_4.show()
        self.frame_2.hide()
        self.frame_38.hide()

    def Manaul_trigger(self):
        self.frame_38.show()
        self.frame_2.hide()
        self.frame_4.hide()

    def manualsign(self):
        pass

    def externalsign(self):
        self.pushButton_3.setEnabled(False)
        for i in range(24):
            Driver.set('Waveform', self.data1, i + 1)

    def internalsign(self):
        pass

    def createpy(self):
        pass
