import qdarkstyle
from MCIUI.main_widget import *
from MCIUI.IP_load import *
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog




class SpectrumScreen(QtWidgets.QDialog):
    def __init__(self, ui_parent, data1, data2):
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
        self.data2 = 'wavefrom width:{}，Sampling Rate:{}'.format(dataz, data0)
        self.p1.setLabel('top', self.data2)




    def addwave(self, chnl_num):
        self.chnl_num = chnl_num
        self.chnl_8.setText("chnlnum".format(chnl_num))
        self.chnl_wave_6.addWidget(SpectrumScreen())













