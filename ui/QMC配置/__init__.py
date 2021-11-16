from PyQt5 import QtCore, QtGui, QtWidgets

from ui.QMC配置.qmc_config_ui import Ui_Dialog


class QMCConfig(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, ui_parent):
        super(QMCConfig, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('QMC配置')
        self.btn_cancel.clicked.connect(self.close)
        self.ui_parent = ui_parent

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        self.ui_parent.show_qmc_config_ui()
