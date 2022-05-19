import sys
from PyQt5 import QtWidgets
import qdarkstyle
from PyQt5.QtWidgets import QApplication
from MCIUI.tabpage import Tabadd
from MCIUI.IP_load import IPloading
from MCIUI.main_widget import MAIN


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MAIN(ui_parent=None)
    child = IPloading(ui_parent=main)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    btn = main.Connect_AWG  # 主窗体按钮事件绑定
    btn.clicked.connect(main.addawg)
    main.show()
    sys.exit(app.exec_())
