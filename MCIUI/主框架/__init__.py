from PyQt5 import QtWidgets, QtGui
import ctypes

from MCIUI.probe登录 import IPprobe
from MCIUI.awg登录 import IPloading
from MCIUI.QSYNC配置 import Device_ip
from MCIUI.主框架.frame import Ui_Form
from MCIUI.异常提示 import Tips

class MAIN(QtWidgets.QWidget, Ui_Form):
    def __init__(self, ui_parent=None):
        super(MAIN, self).__init__()
        self.setupUi(self)
        self.ui_parent = ui_parent
        self.tab.removeTab(0)
        self.tab.removeTab(0)
        self.ip1 = IPloading(self)
        self.ip2 = IPprobe(self)
        self.ip3 = Device_ip(self)

        ico = QtGui.QIcon()
        ico.addPixmap(QtGui.QPixmap("MCIUI/static/img.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(ico)
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("bg")

        self.btn_close.clicked.connect(self.close)
        self.btn_min.clicked.connect(self.showMinimized)
        self.btn_max.clicked.connect(self.max_func)

    # 点击按钮尺寸缩放
    def max_func(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
