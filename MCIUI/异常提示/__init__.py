from PyQt5 import QtWidgets, QtCore

from MCIUI.异常提示.exception_handles import Ui_Form


class Tips(QtWidgets.QWidget, Ui_Form):
    def __init__(self, ui_parent=None):
        super(Tips, self).__init__()
        self.setupUi(self)
        self.ui_parent = ui_parent
        self.setWindowModality(QtCore.Qt.ApplicationModal)