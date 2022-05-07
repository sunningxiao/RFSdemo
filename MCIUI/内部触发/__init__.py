from PyQt5 import QtWidgets
from internal import Ui_Form


class in_trig(QtWidgets.QDialog, Ui_Form):
    def __init__(self, ui_parent):
        super(in_trig, self).__init__()
        self.setupUi(self)
        self.ui_parent = ui_parent

