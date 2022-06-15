from PyQt5 import QtWidgets, QtCore

from MCIUI.QSYNC配置.device_driver_ip import Ui_Form


class Device_ip(QtWidgets.QDialog, Ui_Form):
    def __init__(self, ui_parent):
        super(Device_ip, self).__init__()
        self.setupUi(self)
        self.ui_parent = ui_parent
        self.Cancel.clicked.connect(self.close)
        self.OK.clicked.connect(self.action_click_ok)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.click_ok = False

    def action_click_ok(self):
        self.click_ok = True
        self.close()
