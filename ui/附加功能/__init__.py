import pickle

from PyQt5 import QtCore, QtGui, QtWidgets

from ui.附加功能.cail_from_file import Ui_CailFromFile
from ui.附加功能.rcm_config import Ui_RCMConfig
from ui.附加功能.utils import Custom

from tools.printLog import *


class CalibrationConfig:

    def __init__(self):
        self.file_path = ''
        self.frq_num = 0
        self.is_chirp = False
        self.config = []


class CalibrationFromFileUI(QtWidgets.QWidget, Ui_CailFromFile):
    def __init__(self, parent=None):
        super(CalibrationFromFileUI, self).__init__(None)
        self.setupUi(self)

        self.config = CalibrationConfig()


class RCMConfigUI(QtWidgets.QWidget, Ui_RCMConfig):
    def __init__(self, parent=None):
        super(RCMConfigUI, self).__init__(None)
        self.setupUi(self)

        self.ui_parent = parent
        self.setWindowTitle('RCM配置')
        self.btn_config.clicked.connect(
            self.ui_parent.linking_button('RCM配置', need_feedback=True, need_file=False,
                                          callback=lambda: self.ui_parent.status_trigger.emit((1, 3, self.close)))
        )

    def link_rcm_config_ui(self):
        self.select_chnl.currentIndexChanged.connect(self.action_select_chnl)

        self.txt_mode_code.editingFinished.connect(
            self.ui_parent.change_param("模式码", self.txt_mode_code)
        )
        self.txt_transmit_atte.editingFinished.connect(
            self.ui_parent.change_param("发送衰减", self.txt_transmit_atte, float)
        )
        self.txt_recv_atte.editingFinished.connect(
            self.ui_parent.change_param("接收衰减_1", self.txt_recv_atte)
        )
        self.txt_recv_atte.editingFinished.connect(
            self.ui_parent.change_param("接收衰减_2", self.txt_recv_atte)
        )

    def action_select_chnl(self, *args):
        chnl = self.select_chnl.currentText()
        chnl = 8 if chnl == '全部' else int(chnl)-1
        self.ui_parent.rfs_kit.set_param_value("RCM槽位号", chnl, int)
        self.ui_parent.rfs_kit.set_param_value("通道掩码", min(1 << chnl, 0xFF), int)

    def show_rcm_config_ui(self):
        self.select_chnl.setCurrentIndex(self.ui_parent.rfs_kit.get_param_value("RCM槽位号", 0, int))
        self.txt_mode_code.setText(
            self.ui_parent.rfs_kit.get_param_value('模式码', 0, str)
        )
        self.txt_transmit_atte.setText(
            self.ui_parent.rfs_kit.get_param_value("发送衰减", 0, str)
        )
        self.txt_recv_atte.setText(
            self.ui_parent.rfs_kit.get_param_value("接收衰减_1", 0, str)
        )

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        self.show_rcm_config_ui()
        super(RCMConfigUI, self).showEvent(a0)
