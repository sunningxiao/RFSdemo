from PyQt5 import QtCore, QtGui, QtWidgets

from ui.连接界面.link_system import Ui_Form


class LinkSystemUI(QtWidgets.QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(LinkSystemUI, self).__init__(None)

        self.__parent = parent

        self.setupUi(self)
        self.setWindowTitle('连接RFS')
        self.chk_follow.stateChanged.connect(self.action_port_state)
        self.chk_use_serial.stateChanged.connect(self.action_port_state)
        self.btn_open.clicked.connect(self.__parent.show)

    def action_port_state(self, *args):
        self.txt_port.setDisabled(self.chk_follow.isChecked() or self.chk_use_serial.isChecked())
