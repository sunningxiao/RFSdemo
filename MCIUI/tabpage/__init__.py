from PyQt5 import QtWidgets
from MCIUI.tabpage.addtabpage import Ui_addtab


class Tabadd(QtWidgets.QDialog, Ui_addtab):
    def __init__(self, ui_parent):
        super(Tabadd, self).__init__()
        self.setupUi(self)
        self.ui_parent = ui_parent
