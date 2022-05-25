import sys
from PyQt5 import QtWidgets
import qdarkstyle
from PyQt5.QtWidgets import QApplication

from MCIUI.IP_probe import IPprobe
from MCIUI.IP_load import IPloading
from MCIUI.main_widget import MAIN
from MCIUI.tab_probe import probe_wave


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MAIN(ui_parent=None)
    child = IPloading(ui_parent=main)
    child1 = IPprobe(ui_parent=main)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    btn = main.Connect_AWG # 主窗体按钮事件绑定
    btn2 = main.Connect_Probe_2
    btn.clicked.connect(main.addawg)
    btn2.clicked.connect(main.addprobe)
    main.show()
    child2 = probe_wave(ui_parent=main)
    sys.exit(app.exec_())
