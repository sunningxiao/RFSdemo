from PyQt5 import QtWidgets
import qdarkstyle
from frame import Ui_Form


class MAIN(QtWidgets.QWidget, Ui_Form):
    def __init__(self, ui_parent):
        super(MAIN, self).__init__()
        self.setupUi(self)
        self.ui_parent = ui_parent





















'''
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    From = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(From)
    From.show()
    sys.exit(app.exec_())
'''