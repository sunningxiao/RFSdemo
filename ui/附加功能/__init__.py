import pickle

from PyQt5 import QtCore, QtGui, QtWidgets

from ui.附加功能.cail_from_file import Ui_CailFromFile
from ui.附加功能.utils import Custom


class CalibrationConfig:

    def __init__(self):
        self.file_path = ''
        self.frq_num = 0
        self.is_chirp = False
        self.config = []


class CalibrationFromFileUI(QtWidgets.QWidget, Ui_CailFromFile):
    def __init__(self, parent=None):
        super(CalibrationFromFileUI, self).__init__(parent)
        self.setupUi(self)

        self.config = CalibrationConfig()
