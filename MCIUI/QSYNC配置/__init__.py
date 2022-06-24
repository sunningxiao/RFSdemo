from PyQt5 import QtWidgets, QtCore
from widgets.pgdialog import pgdialog

from MCIUI.QSYNC配置.device_driver_ip import Ui_Form
from MCIUI.异常提示 import Tips


class Device_ip(QtWidgets.QDialog, Ui_Form):
    def __init__(self, ui_parent):
        super(Device_ip, self).__init__()
        self.setupUi(self)
        self.ui_parent = ui_parent
        self.Cancel.clicked.connect(self.close)
        self.OK.clicked.connect(self.action_click_ok)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.click_ok = False
        self.QSYNC_flag = False
        self.error_handles = Tips(self)

    def action_click_ok(self):
        self.click_ok = True
        self.close()

    def progress_bar(self, bar_function, QSYNC_status):
        _pg = pgdialog(self, bar_function, label="QSYNC连接", withcancel=False, mode=0)
        if _pg.perform():
            print("记录系统连接成功")
            QSYNC_status()
            self.QSYNC_flag = True
        else:
            print(f"记录系统连接失败（{_pg.get_err_msg()}）")




