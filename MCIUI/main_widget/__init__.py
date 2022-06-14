from PyQt5 import QtWidgets, QtGui

from MCIUI.IP_probe import IPprobe
from MCIUI.IP_load import IPloading
from MCIUI.main_widget.frame import Ui_Form


class MAIN(QtWidgets.QWidget, Ui_Form):
    def __init__(self, ui_parent=None):
        super(MAIN, self).__init__()
        self.setupUi(self)
        self.ui_parent = ui_parent
        self.tab.removeTab(0)
        self.tab.removeTab(0)
        # 插入logo
        self.frame_25.hide()  # 暂时隐藏logo
        pixmap = QtGui.QPixmap("MCIUI/static/img.png").scaled(self.picture.width(), self.picture.height())
        self.picture.setPixmap(pixmap)
        self.picture.setScaledContents(True)
        self.ip1 = IPloading(self)
        self.ip2 = IPprobe(self)

        self.btn_close.clicked.connect(self.close)
        self.btn_min.clicked.connect(self.showMinimized)
        self.btn_max.clicked.connect(self.max_func)

    # 点击按钮尺寸缩放
    def max_func(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
