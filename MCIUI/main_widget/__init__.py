import sys
import pyqtgraph as pg
from PyQt5 import QtWidgets
import qdarkstyle
from PyQt5.QtWidgets import QApplication
import numpy as np

import MCIUI
from MCIUI.tabpage import Tabadd
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
        self.tab.removeTab(0)
        self.tab.removeTab(0)


        # 控制信号连接

        self.comboBox_2.currentIndexChanged.connect(self.trig_mode)
        self.pushButton_2.clicked.connect(self.externalsign)
        self.Trig_2.clicked.connect(self.manualsign)
        self.trig_2.clicked.connect(self.internalsign)
        self.pushButton_4.clicked.connect(self.createpy)

        self.intrigtimes = self.repeat_times_2.text()
        self.intrigcycle = self.trigger_cycle.text()
        self.manualcycle = self.lineEdit_2.text()


        self.tabadd = self.frame_19


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

    def addawg(self, tabname):
        ip1 = IPloading(self)
        ip1.exec()
        ip = ip1.IPlineEdit.text()

        self.tabname = "second"
        self.pagea = Tabadd(self)
        self.AWGADD = QtWidgets.QWidget(self)
        awg_layout = QtWidgets.QGridLayout(self.AWGADD)
        awg_layout.addWidget(self.pagea)
        awg_layout.setContentsMargins(0, 0, 0, 0)
        self.AWGADD.setObjectName("AWGADD")
        self.tab.addTab(self.AWGADD, '{}'.format(self.tabname))





if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = MAIN(ui_parent=None)
    child = IPloading(ui_parent=main)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    btn = main.Connect_AWG  # 主窗体按钮事件绑定
    btn.clicked.connect(main.addawg)
    # main.tab.removeTab(0)
    main.show()
    sys.exit(app.exec_())
