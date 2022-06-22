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
        try:
            self.progress_bar()
        except Exception as e:
            self.main_ui.ip3.error_handles.tips_text.setText(str(e))
            self.main_ui.ip3.error_handles.show()
            return False

    def progress_bar(self):
        from Realization.real_base import ConfigWidget
        _pg = pgdialog(self, ConfigWidget.config_QSYNC_ip, label="QSYNC连接", withcancel=False, mode=0)
        # if _pg.perform():
        #     print("记录系统连接成功")
        #     self.QSYNC_flag = False
        # else:
        #     print(f"记录系统连接失败（{_pg.get_err_msg()}）")





