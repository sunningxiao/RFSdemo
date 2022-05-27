from PyQt5 import QtWidgets

from MCIUI.chnl_mode_list.mode_tab import Ui_Form


class chnls_list(QtWidgets.QWidget, Ui_Form):
    def __init__(self, ui_parent):
        super(chnls_list, self).__init__()
        self.setupUi(self)
        self.ui_parent = ui_parent
