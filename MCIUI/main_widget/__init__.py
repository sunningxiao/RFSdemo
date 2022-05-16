import sys
import pyqtgraph as pg
from PyQt5 import QtWidgets
import qdarkstyle
from PyQt5.QtWidgets import QApplication
import numpy as np
from MCIUI.tabpage import Tabadd
from MCIUI.IP_load import IPloading
from MCIUI.main_widget.frame import Ui_Form


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


    def addawg(self, tabname):
        ip1 = IPloading(self)
        ip1.exec()
        ip = ip1.IPlineEdit.text()

        """
        driver = Driver(ip)

        sysparam = {
            'MixMode': 2, 'RefClock': 'out', 'DAC抽取倍数': 1, 'DAC本振频率': 0  # , 'DArate': 4e9
        }
       
        driver.open(system_parameter=sysparam)
        """
        self.tabname = "second"
        self.pagea = Tabadd(self)
        self.AWGADD = QtWidgets.QWidget(self)
        awg_layout = QtWidgets.QGridLayout(self.AWGADD)
        awg_layout.addWidget(self.pagea)
        awg_layout.setContentsMargins(0, 0, 0, 0)
        self.AWGADD.setObjectName("AWGADD")
        self.tab.addTab(self.AWGADD, '{}'.format(self.tabname))

        self.tab.setCurrentIndex(0)





if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = MAIN(ui_parent=None)
    child = IPloading(ui_parent=main)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    btn = main.Connect_AWG  # 主窗体按钮事件绑定
    btn.clicked.connect(main.addawg)
    main.show()
    sys.exit(app.exec_())
