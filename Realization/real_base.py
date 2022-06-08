import sys

import qdarkstyle
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

from MCIUI.main_widget import MAIN
from MCIUI.tabpage import Addawg
from MCIUI.tab_probe import Probe_wave
from MCIUI.IP_probe import IPprobe
from MCIUI.IP_load import IPloading
from MCIUI.通道波形 import Wave


class ConfigWidget:

    def __int__(self):
        self.main_ui = MAIN(self)
        self.awg_ui = Addawg(self)
        # self.probe_ui = Probe_wave(self)
        # self.ip_probe_ui = IPprobe(self)
        self.ip_awg_ui = IPloading(self)
        self.chnl_ui = Wave(self)








if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MAIN(ui_parent=None)
    child = IPloading(ui_parent=main)
    child1 = IPprobe(ui_parent=main)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    btn = main.Connect_AWG # 主窗体按钮事件绑定
    btn2 = main.Connect_Probe_2
    btn.clicked.connect(lambda: child.show())
    btn2.clicked.connect(lambda: child1.show())
    main.show()
    sys.exit(app.exec_())


