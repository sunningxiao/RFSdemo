from PyQt5 import QtCore, QtGui, QtWidgets

from ui.开启工作 import start_ui


class StartConfig(QtWidgets.QDialog, start_ui.Ui_Dialog):
    def __init__(self, ui_parent):
        super(StartConfig, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('系统开启_参数检查')
        self.btn_cancel.clicked.connect(self.close)
        self.ui_parent = ui_parent

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.ui_parent.show_param()

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        self.ui_parent.show_start_ui()
