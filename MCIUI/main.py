import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg

from IP_load import IPloading
from 内部触发 import in_trig
from 外部触发 import ex_trig
from main_widget import Ui_Form
import qdarkstyle


class MCIcontrol(QtWidgets.QWidget, Ui_Form):
    def __init__(self, parent):
        super(MCIcontrol, self).__init__()
        self.Connect_AWG_2.clicked().connect(self.connect_awg)
        #self.Connect_Probe_2.clicked().connect(self.connect_probe)
        app = QtWidgets.QApplication(sys.argv)
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        From = QtWidgets.QWidget()
        ui = Ui_Form()
        ui.setupUi(From)
        From.show()
        sys.exit(app.exec_())


# class control_ip(QtWidgets.QWidget,IPloading):
#     def connect_awg(self):
#         app = QtWidgets.QApplication(sys.argv)
#         app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
#         From = QtWidgets.QWidget()
#         ui = Ui_Form()
#         ui.setupUi(From)
#         From.show()
#         sys.exit(app.exec_())
