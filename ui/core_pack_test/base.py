import locale
from typing import List, Dict, Any
from PyQt5 import QtCore, QtWidgets, QtGui

from ui.core_pack_test.core_pack_test import Ui_CorePackTest
from tools.printLog import *


class CorePackTestUI(QtWidgets.QWidget, Ui_CorePackTest):
    def __init__(self, parent):
        super(CorePackTestUI, self).__init__()
        self.ui_parent = parent
        self.setupUi(self)

        self.trans = QtCore.QTranslator()

        self.select_language.currentTextChanged.connect(self._trigger_language)
        self.auto_language()

    def auto_language(self):
        language_num = self.select_language.count()
        _locale = locale.getdefaultlocale()[0]
        if _locale in [self.select_language.itemText(i) for i in range(language_num)]:
            self._trigger_language(_locale)
            self.select_language.setCurrentText(_locale)
        else:
            self._trigger_language(self.select_language.currentText())

    def _trigger_language(self, language):
        self.trans.load(f'language/core_pack_{language}')
        _app = QtWidgets.QApplication.instance()  # 获取app实例
        _app.installTranslator(self.trans)
        # 重新翻译界面
        self.retranslateUi(self)
