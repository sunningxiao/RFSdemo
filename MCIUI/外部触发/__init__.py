from PyQt5 import QtWidgets
from MCIUI.外部触发.external import Ui_Form


class ex_trig(QtWidgets.QDialog, Ui_Form):
    def __init__(self, ui_parent):
        super(ex_trig, self).__init__()
        self.setupUi(self)
        self.ui_parent = ui_parent
