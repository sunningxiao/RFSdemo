import sys
import re

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

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_ui = MAIN()
        self.main_ui.Connect_AWG.clicked.connect(self.add_awg)

    # 判断IP地址是否合法

    def check_ip(self, ip):
        compile_ip = re.compile(
            '^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
        return isinstance(compile_ip.match(ip), re.Match)

    def add_awg(self):
        self.main_ui.ip1.exec()
        if not self.main_ui.ip1.click_ok:
            return
        addr = self.main_ui.ip1.IPlineEdit.text()
        print(addr)
        if not self.check_ip(addr):
            return
        self.main_ui.add_awg(addr)

    def run_ui(self):
        self.app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.main_ui.show()
        sys.exit(self.app.exec())
