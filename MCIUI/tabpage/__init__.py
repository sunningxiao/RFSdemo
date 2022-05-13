from PyQt5 import QtWidgets
from MCIUI.tabpage.addtabpage import Ui_addtab
from MCIUI.通道波形 import wave
import pyqtgraph as pg
import numpy as np


class Tabadd(QtWidgets.QWidget, Ui_addtab):
    def __init__(self, ui_parent):
        super(Tabadd, self).__init__(ui_parent)
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



        self._layout = QtWidgets.QGridLayout()
        self.plot_win = pg.GraphicsLayoutWidget(self)
        self._layout.addWidget(self.plot_win)
        self.p1 = self.plot_win.addPlot()
        self.data1 = np.random.normal(size=300)
        curve1 = self.p1.plot(self.data1)
        def update1():
            self.data1[:-1] = self.data1[1:]
            self.data1[-1] = np.random.normal()
            curve1.setData(self.data1)

        def update():
            update1()

        timer = pg.QtCore.QTimer()
        timer.timeout.connect(update)
        timer.start(50)
        self.verticalLayout_10.addLayout(self._layout)
        self.verticalLayout_11.addLayout(self._layout)
        self.verticalLayout_33.addLayout(self._layout)
        self.verticalLayout_32.addLayout(self._layout)
        self.verticalLayout_31.addLayout(self._layout)
        self.verticalLayout_30.addLayout(self._layout)
        self.verticalLayout_29.addLayout(self._layout)
        self.verticalLayout_28.addLayout(self._layout)
        self.verticalLayout_27.addLayout(self._layout)
        self.verticalLayout_14.addLayout(self._layout)

        self.verticalLayout_26.addLayout(self._layout)
        self.verticalLayout_25.addLayout(self._layout)
        self.verticalLayout_16.addLayout(self._layout)
        self.verticalLayout_24.addLayout(self._layout)
        self.verticalLayout_15.addLayout(self._layout)
        self.verticalLayout_13.addLayout(self._layout)
        self.verticalLayout_23.addLayout(self._layout)
        self.verticalLayout_12.addLayout(self._layout)
        self.verticalLayout_22.addLayout(self._layout)
        self.verticalLayout_21.addLayout(self._layout)

        self.verticalLayout_20.addLayout(self._layout)
        self.verticalLayout_19.addLayout(self._layout)
        self.verticalLayout_18.addLayout(self._layout)
        self.verticalLayout_17.addLayout(self._layout)


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
        pass

    def internalsign(self):
        pass

    def createpy(self):
        pass


