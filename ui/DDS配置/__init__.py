from PyQt5 import QtCore, QtGui, QtWidgets

from ui.DDS配置 import dds_config_ui


class DDSConfig(QtWidgets.QDialog, dds_config_ui.Ui_Dialog):
    def __init__(self, ui_parent):
        super(DDSConfig, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('DDS设置_参数检查')
        self.btn_cancel.clicked.connect(self.close)
        self.ui_parent = ui_parent

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.ui_parent.show_param()

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        self.ui_parent.show_dds_config_ui()
