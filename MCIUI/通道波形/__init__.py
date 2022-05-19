import pyqtgraph as pg
import numpy as np
from PyQt5 import QtWidgets
from MCIUI.通道波形.chnlwave import Ui_Form


class wave(QtWidgets.QWidget, Ui_Form):
    def __init__(self, ui_parent):
        super(wave, self).__init__(ui_parent)
        self.setupUi(self)
        self.ui_parent = ui_parent
        pg.setConfigOption('background', '#19232D')
        self.plot_win = pg.GraphicsLayoutWidget(self)
        self.p1 = self.plot_win.addPlot()
        self.param1 = 12
        self.param2 = 23
        self.data2 = '参数1：{}，参数2：{}'.format(self.param1, self.param2)
        self.p1.setLabel('top', self.data2)
        self.verticalLayout.addWidget(self.plot_win)
