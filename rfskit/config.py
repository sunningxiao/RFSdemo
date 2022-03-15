import sys
import asyncio

from PyQt5.QtWidgets import QApplication
# 必须要在这里导入一下QtWebEngineWidgets, 此Qt模块要求在QApplication实例化之前必须被导入
# from PyQt5 import QtWebEngineWidgets
import pyqtgraph as pg
import qdarkstyle
from qasync import QEventLoop

from tools.printLog import set_print_enable


# 全局修改pyqtgraph的背景色
pg.setConfigOption('background', '#19232D')

global_application = QApplication(sys.argv)

# 应用全局主题
global_application.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

# 应用Qt异步事件循环
try:
    global_event_loop = QEventLoop(global_application)
except AttributeError as e:
    # 兼容rfsoc demo
    from quamash import QEventLoop
    global_event_loop = QEventLoop(global_application)
asyncio.set_event_loop(global_event_loop)
global_desktop_center = global_application.desktop().availableGeometry().center()

# 是否使用Qt print循环
# set_print_enable({'QT': False, 'debug': True, 'info': True, 'error': True, 'exception': True})
