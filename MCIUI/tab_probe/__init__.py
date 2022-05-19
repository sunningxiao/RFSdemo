from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
import sys
from MCIUI.tab_probe.probe_page import Ui_Form
import qdarkstyle


class probe_wave(QtWidgets.QWidget, Ui_Form):
    def __init__(self, ui_parent):
        super(probe_wave, self).__init__(ui_parent)
        self.setupUi(self)
        self.ui_parent = ui_parent
        self.widget_internal.hide()
        self.widget_external.hide()
        self.Trig_Mode.currentIndexChanged.connect(self.trig_mode)
        self.shot_txt = self.shots.text
        self.pointnumber_txt = self.PointNumber.text
        self.triggerdelay_txt = self.triggerdelay.text
        self.frequencylist_txt = self.FrequencyList.text
        self.Phase_txt = self.Phase.text


    def trig_mode(self, i):
        if i == 1:
            self.inter_trig()
        elif i == 2:
            self.exter_trig()
        else:
            self.manual_trig()

    def manual_trig(self):
        self.widget_manual.show()
        self.widget_external.hide()
        self.widget_internal.hide()

    def inter_trig(self):
        self.widget_internal.show()
        self.widget_external.hide()
        self.widget_manual.hide()

    def exter_trig(self):
        self.widget_external.show()
        self.widget_manual.hide()
        self.widget_internal.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    windows = probe_wave(ui_parent=None)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    windows.show()
    app.exec()
