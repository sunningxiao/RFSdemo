# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(650, 100)
        Form.setMinimumSize(QtCore.QSize(650, 0))
        Form.setMaximumSize(QtCore.QSize(650, 16777215))
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_25 = QtWidgets.QFrame(Form)
        self.frame_25.setMinimumSize(QtCore.QSize(0, 100))
        self.frame_25.setMaximumSize(QtCore.QSize(16777215, 100))
        self.frame_25.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_25.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_25.setObjectName("frame_25")
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout(self.frame_25)
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.chnl_8 = QtWidgets.QLabel(self.frame_25)
        self.chnl_8.setMinimumSize(QtCore.QSize(40, 0))
        self.chnl_8.setMaximumSize(QtCore.QSize(20, 16777215))
        self.chnl_8.setObjectName("chnl_8")
        self.horizontalLayout_19.addWidget(self.chnl_8)
        self.chnl_wave_6 = QtWidgets.QFrame(self.frame_25)
        self.chnl_wave_6.setMinimumSize(QtCore.QSize(0, 0))
        self.chnl_wave_6.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.chnl_wave_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.chnl_wave_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.chnl_wave_6.setObjectName("chnl_wave_6")
        self.horizontalLayout_19.addWidget(self.chnl_wave_6)
        self.verticalLayout.addWidget(self.frame_25)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.chnl_8.setText(_translate("Form", "chnl-0"))

