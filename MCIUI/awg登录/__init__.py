from PyQt5 import QtWidgets, QtCore

from MCIUI.awg登录.ipload import Ui_Form

class IPloading(QtWidgets.QDialog, Ui_Form):
    def __init__(self, ui_parent):
        super(IPloading, self).__init__()
        self.MixMode_param = None
        self.setupUi(self)
        self.ui_parent = ui_parent
        self.Cancel.clicked.connect(self.close)
        # self.OK.clicked.connect(self.addawg)
        self.OK.clicked.connect(self.action_click_ok)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.click_ok = False
        self.MixMode_param = 1
        self.RefClock_param = 'in'
        self.Keep_Amp_param = False
        self.MixMode.currentIndexChanged.connect(self.Mix_Mode)
        self.RefClock.currentIndexChanged.connect(self.Ref_Clock)
        self.KeepAmp.currentIndexChanged.connect(self.Keep_Amp)


    def action_click_ok(self):
        self.click_ok = True
        self.close()

    def Mix_Mode(self, i):
        if i == 0:
            self.MixMode_param = 1
        else:
            self.MixMode_param = 2

    def Ref_Clock(self, i):
        if i == 0:
            self.RefClock_param = 'in'
        else:
            self.RefClock_param = 'out'

    def Keep_Amp(self, i):
        if i == 0:
            self.Keep_Amp_param = False
        else:
            self.Keep_Amp_param = True
