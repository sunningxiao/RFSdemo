import pyqtgraph as pg
import numpy as np
import sys
from PyQt5 import QtWidgets

from PyQt5 import QtWidgets
from chnlwave import Ui_Form


class wave(QtWidgets.QDialog, Ui_Form):
    def __init__(self, ui_parent):
        super(wave, self).__init__()
        self.setupUi(self)
        self.ui_parent = ui_parent


class SpectrumScreen(QtWidgets.QDialog):
    def __init__(self, ui_parent, p1=None):
        super(SpectrumScreen, self).__init__()
        self.data1 = None
        self.data2 = None
        self.setWindowTitle('显示')
        self.resize(600, 150)
        self.ui_parent = ui_parent
        self._layout = QtWidgets.QGridLayout(self)
        self.plot_win = pg.GraphicsLayoutWidget(self)
        self._layout.addWidget(self.plot_win)
        self.p1 = self.plot_win.addPlot()
        self.in_data(66, 65)
        """
        text = pg.TextItem("输入数据{}：".format(self.data2))
        p1.addItem(text)
        """
        self.data1 = np.random.normal(size=300)
        # self.data1 = self.wave_data()
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

    def wave_data(self, data1, axis=None):
        self.data1 = data1

    def in_data(self, dataz, data0):
        self.data2 = '参数1：{}，参数2：{}'.format(dataz, data0)
        self.p1.setLabel('top', self.data2)


