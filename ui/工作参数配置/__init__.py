from PyQt5 import QtCore, QtGui, QtWidgets

from ui.工作参数配置.work_config import Ui_Form


class TestWidget(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(TestWidget, self).__init__(None)
        self.setupUi(self)
