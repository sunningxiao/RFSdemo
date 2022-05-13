import pyqtgraph as pg
import numpy as np
import sys

from PyQt5 import QtWidgets

import MCIUI
from MCIUI.通道波形.chnlwave import Ui_Form


class wave(QtWidgets.QWidget, Ui_Form):
    def __init__(self, ui_parent):
        super(wave, self).__init__(ui_parent)
        self.setupUi(self)
        self.ui_parent = ui_parent

