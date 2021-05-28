#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Tony
date:19.02.16
description: 
进度条配辅助线程
将待执行函数，函数参数，进度条显示内容及显示模式作为参数输入；
ui:操作界面
args:函数参数使用tuple型输入；
label:显示内容使用string型输入；
mode:显示形式0为不显示执行百分比，1为显示执行百分比,2为不显示百分比不加入td中间运行中不叫停
"""


from PyQt5 import QtCore
from PyQt5.QtWidgets import QProgressDialog
import threading
from printLog import *


class pgdialog(QProgressDialog):
    def __init__(self, ui, func, args=(), label="正在操作...", mode=0, withcancel=True):
        try:
            super(pgdialog, self).__init__(ui)
            self.setWindowTitle("请等待")
            self.setLabelText(label)
            if withcancel:
                self.setCancelButtonText("取消")
            else:
                self.setCancelButton(None)
            self.setMinimumDuration(5)
            self.setWindowModality(QtCore.Qt.WindowModal)
            self.setMinimumWidth(300)
            self.mode = mode
            self.cnt = 0
            # 设置线程参数
            self.td = pthread()
            if mode == 0:
                self.setRange(0, 0)
                self.setValue(0)
            elif mode == 1:
                self.setAutoClose(False)  # 带100自动关闭
                self.setAutoReset(False)  # 到100自动复位0
                self.setRange(0, 100)
            else:
                self.setRange(0, 0)
                self.setValue(0)

            self.td.setup(target=func, args=args, mode=mode)
        except Exception as e:
            printException(e)

    def perform(self):
        flag = 2  # mode为1时，进度条打印一次100
        self.td.start()
        while self.td.is_alive():
            if self.wasCanceled():
                self.cancel_run()
                return False
            if self.mode == 1:
                value = self.td.getPGvalue()
                if flag and value >= 100:
                    flag -= 1

                if flag:
                    self.setValue(value)
            else:
                self.setValue(self.getcnt())
            if self.td.checkTextFlag():
                self.setLabelText(self.td.getText())
                self.td.clearTextFlag()
        self.cancel()
        return self.td.getstate()

    def join(self):
        print("here")
        self.td.join()

    def cancel_run(self):
        self.setMaximum(100)
        self.setValue(100)
        self.setLabelText("正在取消")
        self.setMinimumDuration(20)
        self.setCancelButton(None)
        self.setRange(0, 0)
        self.td.stop()
        while self.td.is_alive():
            self.setValue(self.getcnt())
        self.cancel()

    # 产生递增数，用于空白进度条
    def getcnt(self):
        self.cnt += 1
        return self.cnt

    def get_err_msg(self):
        return self.td.err_msg


class pthread(threading.Thread):

    def __init__(self):
        self._stop_event = threading.Event()
        self._text_event = threading.Event()
        self.pgvalue = 0
        self.text = ""
        self.state = False
        self.err_msg = ""

    def setup(self, target=None, args=(), mode=0):
        if mode == 0 or mode == 1:
            kwargs = {"pthread": self}
        else:
            kwargs = {}
        super(pthread, self).__init__(target=target, args=args, kwargs=kwargs)

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def updatePGvalue(self, value):
        self.pgvalue = value

    def getPGvalue(self):
        return self.pgvalue

    def updateText(self, text):
        self.text = text
        self._text_event.set()

    def getText(self):
        return self.text

    def checkTextFlag(self):
        return self._text_event.is_set()

    def clearTextFlag(self):
        return self._text_event.clear()

    def getstate(self):
        return self.state

    def update_state(self, state):
        if isinstance(state, str):
            self.state = False
            self.err_msg = state
        else:
            self.state = state
