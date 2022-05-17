import sys
from PyQt5 import QtWidgets
import qdarkstyle
from PyQt5.QtWidgets import QApplication
from MCIUI.tabpage import Tabadd
from MCIUI.IP_load import IPloading
from MCIUI.main_widget.frame import Ui_Form

class MAIN(QtWidgets.QWidget, Ui_Form):
    def __init__(self, ui_parent):
        super(MAIN, self).__init__()
        self.setupUi(self)
        self.ui_parent = ui_parent
        # self.repeat_times = 1
        self.tab.removeTab(0)
        self.tab.removeTab(0)
        self.page_list = []
        self.i = 0

        # 控制信号连接

    def addawg(self):

        self.tabname = 'AWG-' + str(self.i)
        self.i = self.i + 1
        self.pagea = Tabadd(self)

        self.page_list.append(self.pagea)
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
