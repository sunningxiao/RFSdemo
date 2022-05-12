import sys
import pyqtgraph as pg
from PyQt5 import QtWidgets
import qdarkstyle
from PyQt5.QtWidgets import QApplication
import numpy as np

import MCIUI
from MCIUI.tabpage import Tabadd, Ui_addtab
from MCIUI.IP_load import IPloading
from MCIUI.main_widget.frame import Ui_Form
from MCIUI.通道波形 import wave


class MAIN(QtWidgets.QWidget, Ui_Form):
    def __init__(self, ui_parent):
        super(MAIN, self).__init__()
        self.setupUi(self)
        self.ui_parent = ui_parent
        self.repeat_times = 1
        self.frame_2.hide()
        self.frame_4.hide()


        # 控制信号连接

        self.comboBox_2.currentIndexChanged.connect(self.trig_mode)
        self.pushButton_2.clicked.connect(self.externalsign)
        self.Trig_2.clicked.connect(self.manualsign)
        self.pushButton_4.clicked.connect(self.createpy)

        self.intrigtimes = self.repeat_times_2.text()
        self.intrigcycle = self.trigger_cycle.text()
        self.manualcycle = self.lineEdit_2.text()

        self.tabadd = self.frame_19

    def externalsign(self):
        self.addawg(2, 2)

    def manualsign(self):
        pass

    def internalsign(self):
        pass

    def createpy(self):
        pass

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

    def connectawg(self):
        pass

    def manual(self):
        pass

    def internal(self):
        pass

    def external(self):
        pass



    def addawg(self, tabname, chnlnum):
        self.awgname = tabname
        self.chnlnum = chnlnum
        self.pagea = Tabadd(MCIUI.tabpage.Ui_addtab)
        self.AWGADD = QtWidgets.QWidget(self.pagea)
        self.AWGADD.setObjectName("AWGADD")
        self.tab.addTab(self.AWGADD, "name".format(tabname))



        if self.chnlnum != 0:
            self.verticalLayout_6.addWidget(wave.waves(chnlnum))
            self.chnlnum = self.chnlnum - 1



if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = MAIN(Ui_Form)

    child = IPloading(MCIUI.IP_load.Ui_Form)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    btn = main.Connect_AWG  # 主窗体按钮事件绑定
    btn.clicked.connect(child.show)

    main.show()
    sys.exit(app.exec_())

'''

    class wave:

        def plotdate(self):
            pass

        def chnl_num(self):
            pass

        def wavenum(self):
            pass

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
    '''
