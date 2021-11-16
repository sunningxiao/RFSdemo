from PyQt5 import QtCore, QtGui, QtWidgets

from ui.波形预置 import wave_file_ui


class WaveFileConfig(QtWidgets.QDialog, wave_file_ui.Ui_Dialog):
    def __init__(self, ui_parent):
        super(WaveFileConfig, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('波形装载--双击文件名清除选择')
        self.btn_cancel.clicked.connect(self.close)
        self.ui_parent = ui_parent

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        self.ui_parent.show_wave_file_ui()
