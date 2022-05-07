# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'internal.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(266, 127)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(266, 127))
        Form.setMaximumSize(QtCore.QSize(266, 127))
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(266, 127))
        self.frame.setMaximumSize(QtCore.QSize(266, 127))
        self.frame.setStyleSheet("border:0.5px solid #626262")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setStyleSheet("font: 9pt \"Arial\";")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.repeat_times = QtWidgets.QLineEdit(self.frame)
        self.repeat_times.setObjectName("repeat_times")
        self.gridLayout.addWidget(self.repeat_times, 0, 1, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setStyleSheet("font: 9pt \"Arial\";")
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.trigger_cycle = QtWidgets.QLineEdit(self.frame)
        self.trigger_cycle.setObjectName("trigger_cycle")
        self.gridLayout.addWidget(self.trigger_cycle, 1, 1, 1, 2)
        self.internal = QtWidgets.QPushButton(self.frame)
        self.internal.setMinimumSize(QtCore.QSize(0, 16))
        self.internal.setStyleSheet("background-color: rgb(85, 170, 255);\n"
"margin-right:5px;")
        self.internal.setObjectName("internal")
        self.gridLayout.addWidget(self.internal, 2, 0, 1, 1)
        self.trig = QtWidgets.QPushButton(self.frame)
        self.trig.setMinimumSize(QtCore.QSize(0, 20))
        self.trig.setStyleSheet("margin-left:5px;\n"
"margin-right:5px;")
        self.trig.setObjectName("trig")
        self.gridLayout.addWidget(self.trig, 2, 2, 1, 1)
        self.config = QtWidgets.QPushButton(self.frame)
        self.config.setMinimumSize(QtCore.QSize(0, 20))
        self.config.setStyleSheet("margin-left:5px;\n"
"margin-right:5px;")
        self.config.setObjectName("config")
        self.gridLayout.addWidget(self.config, 2, 1, 1, 1)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "repeat times"))
        self.label_2.setText(_translate("Form", "trigger cycle"))
        self.internal.setText(_translate("Form", "Internal"))
        self.trig.setText(_translate("Form", "Trig"))
        self.config.setText(_translate("Form", "config"))

