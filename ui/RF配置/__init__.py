from PyQt5 import QtCore, QtGui, QtWidgets

from ui.RF配置 import rf_config


class RFConfig(QtWidgets.QDialog, rf_config.Ui_Form):
    def __init__(self, ui_parent):
        super(RFConfig, self).__init__()
        self.setupUi(self)
        self.ui_parent = ui_parent

    def check_mode(self, event=None):
        self.widget_master.setVisible(self.ui_parent.ui.select_is_master.currentText() == '主机')
        self.widget_slave.setVisible(self.ui_parent.ui.select_is_master.currentText() == '从机')
        self.setWindowTitle('主端配置' if self.ui_parent.ui.select_is_master.currentText() == '主机' else '从端配置')

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        self.check_mode(a0)
        super(RFConfig, self).showEvent(a0)
