from 内部触发 import in_trig
from 外部触发 import ex_trig
import qdarkstyle
from MCIUI.main_widget import *
from MCIUI.IP_load import *
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog


# mainWindow
class MyMainWindow(QMainWindow, main_widget.Ui_Form):
    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('main window')

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()


class ChildWindow(QDialog, IP_load.Ui_Form):
    def __init__(self):
        super(ChildWindow, self).__init__()
        self.setupUi(self)

        self.setWindowTitle('child window')
        self.pushButton.clicked.connect(self.btnClick)  # 按钮事件绑定

    def btnClick(self):  # 子窗体自定义事件
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = MyMainWindow()

    child = ChildWindow()

    btn = main.Connect_AWG  # 主窗体按钮事件绑定
    btn.clicked.connect(child.show)

    main.show()
    sys.exit(app.exec_())













