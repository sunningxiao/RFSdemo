# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ipload.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(510, 376)
        Form.setMaximumSize(QtCore.QSize(16777215, 16777215))
        Form.setStyleSheet("")
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 40))
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setContentsMargins(11, 3, -1, 3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setStyleSheet("font: 11pt \"Arial\";")
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label, 0, QtCore.Qt.AlignLeft)
        self.verticalLayout_2.addWidget(self.frame_2)
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frame_4 = QtWidgets.QFrame(self.frame_3)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_4)
        self.gridLayout.setObjectName("gridLayout")
        self.MixMode = QtWidgets.QComboBox(self.frame_4)
        self.MixMode.setObjectName("MixMode")
        self.MixMode.addItem("")
        self.MixMode.addItem("")
        self.gridLayout.addWidget(self.MixMode, 3, 1, 1, 1)
        self.KeepAmp = QtWidgets.QComboBox(self.frame_4)
        self.KeepAmp.setObjectName("KeepAmp")
        self.KeepAmp.addItem("")
        self.KeepAmp.addItem("")
        self.gridLayout.addWidget(self.KeepAmp, 2, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.frame_4)
        self.label_6.setStyleSheet("font: 10pt \"Arial\";")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 4, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.frame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setStyleSheet("font: 10pt \"Arial\";")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)
        self.RefClock = QtWidgets.QComboBox(self.frame_4)
        self.RefClock.setObjectName("RefClock")
        self.RefClock.addItem("")
        self.RefClock.addItem("")
        self.gridLayout.addWidget(self.RefClock, 4, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_2.setStyleSheet("font: 10pt \"Arial\";\n"
"")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.IPlineEdit = QtWidgets.QLineEdit(self.frame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.IPlineEdit.sizePolicy().hasHeightForWidth())
        self.IPlineEdit.setSizePolicy(sizePolicy)
        self.IPlineEdit.setMinimumSize(QtCore.QSize(160, 0))
        self.IPlineEdit.setObjectName("IPlineEdit")
        self.gridLayout.addWidget(self.IPlineEdit, 0, 1, 1, 1)
        self.DArate = QtWidgets.QLineEdit(self.frame_4)
        self.DArate.setStyleSheet("")
        self.DArate.setObjectName("DArate")
        self.gridLayout.addWidget(self.DArate, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setStyleSheet("font: 10pt \"Arial\";")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.frame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setStyleSheet("font: 10pt \"Arial\";")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.verticalLayout_4.addWidget(self.frame_4)
        self.frame_5 = QtWidgets.QFrame(self.frame_3)
        self.frame_5.setMaximumSize(QtCore.QSize(16777215, 54))
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Cancel = QtWidgets.QPushButton(self.frame_5)
        self.Cancel.setMinimumSize(QtCore.QSize(0, 30))
        self.Cancel.setStyleSheet("margin-right:20px;\n"
"margin-left:10px;")
        self.Cancel.setObjectName("Cancel")
        self.horizontalLayout.addWidget(self.Cancel)
        self.OK = QtWidgets.QPushButton(self.frame_5)
        self.OK.setMinimumSize(QtCore.QSize(0, 30))
        self.OK.setStyleSheet("margin-left:20px;\n"
"margin-right:10px;")
        self.OK.setObjectName("OK")
        self.horizontalLayout.addWidget(self.OK)
        self.verticalLayout_4.addWidget(self.frame_5)
        self.verticalLayout_2.addWidget(self.frame_3)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.IPlineEdit, self.DArate)
        Form.setTabOrder(self.DArate, self.KeepAmp)
        Form.setTabOrder(self.KeepAmp, self.MixMode)
        Form.setTabOrder(self.MixMode, self.RefClock)
        Form.setTabOrder(self.RefClock, self.Cancel)
        Form.setTabOrder(self.Cancel, self.OK)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Connect AWG"))
        self.MixMode.setItemText(0, _translate("Form", "第一奈奎斯特区"))
        self.MixMode.setItemText(1, _translate("Form", "第二奈奎斯特区"))
        self.KeepAmp.setItemText(0, _translate("Form", "False"))
        self.KeepAmp.setItemText(1, _translate("Form", "True"))
        self.label_6.setText(_translate("Form", "RefClock"))
        self.label_5.setText(_translate("Form", "MixMode"))
        self.RefClock.setItemText(0, _translate("Form", "in"))
        self.RefClock.setItemText(1, _translate("Form", "out"))
        self.label_2.setText(_translate("Form", "device ip"))
        self.label_3.setText(_translate("Form", "DArate"))
        self.label_4.setText(_translate("Form", "KeepAmp"))
        self.Cancel.setText(_translate("Form", "Cancel"))
        self.OK.setText(_translate("Form", "OK"))
