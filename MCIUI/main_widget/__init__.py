import sys

from PyQt5 import QtWidgets
import qdarkstyle
from PyQt5.QtWidgets import QApplication

import MCIUI.IP_load
from MCIUI.IP_load import IPloading
from MCIUI.main_widget.frame import Ui_Form


class MAIN(QtWidgets.QWidget, Ui_Form):
    def __init__(self, ui_parent):
        super(MAIN, self).__init__()
        self.setupUi(self)
        self.ui_parent = ui_parent




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
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    From = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(From)
    From.show()
    sys.exit(app.exec_())
'''