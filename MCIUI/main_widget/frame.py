# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frame.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'framebvTzLX.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(952, 621)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setMaximumSize(QSize(16777215, 40))
        self.frame.setStyleSheet(u"")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_5 = QFrame(self.frame)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_5)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.frame_5)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"font: 25 14pt \"Bahnschrift Light\";")

        self.verticalLayout_2.addWidget(self.label)

        self.horizontalLayout.addWidget(self.frame_5)

        self.frame_6 = QFrame(self.frame)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMaximumSize(QSize(100, 16777215))
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.btn_min = QPushButton(self.frame_6)
        self.btn_min.setObjectName(u"btn_min")
        self.btn_min.setMinimumSize(QSize(20, 20))
        self.btn_min.setMaximumSize(QSize(20, 20))
        self.btn_min.setStyleSheet(u"boder:none;\n"
                                   "background-color: rgb(218, 218, 0);\n"
                                   "border-radius:10px;")

        self.horizontalLayout_2.addWidget(self.btn_min)

        self.btn_max = QPushButton(self.frame_6)
        self.btn_max.setObjectName(u"btn_max")
        self.btn_max.setMinimumSize(QSize(20, 20))
        self.btn_max.setMaximumSize(QSize(20, 20))
        self.btn_max.setStyleSheet(u"boder:none;\n"
                                   "border-radius:10px;\n"
                                   "background-color: rgb(0, 79, 239);")

        self.horizontalLayout_2.addWidget(self.btn_max)

        self.btn_close = QPushButton(self.frame_6)
        self.btn_close.setObjectName(u"btn_close")
        self.btn_close.setMinimumSize(QSize(20, 20))
        self.btn_close.setMaximumSize(QSize(20, 20))
        self.btn_close.setStyleSheet(u"border:none;\n"
                                     "border-radius:10px;\n"
                                     "background-color: rgb(255, 0, 0);")

        self.horizontalLayout_2.addWidget(self.btn_close)

        self.horizontalLayout.addWidget(self.frame_6)

        self.verticalLayout.addWidget(self.frame)

        self.frame_3 = QFrame(Form)
        self.frame_3.setObjectName(u"frame_3")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setMinimumSize(QSize(0, 40))
        self.frame_3.setMaximumSize(QSize(16777215, 45))
        self.frame_3.setStyleSheet(u"")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.Connect_AWG = QPushButton(self.frame_3)
        self.Connect_AWG.setObjectName(u"Connect_AWG")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.Connect_AWG.sizePolicy().hasHeightForWidth())
        self.Connect_AWG.setSizePolicy(sizePolicy1)
        self.Connect_AWG.setMinimumSize(QSize(157, 0))
        self.Connect_AWG.setStyleSheet(u"\n"
                                       "font: 12pt \"Arial\";border-radius:10px;")

        self.horizontalLayout_6.addWidget(self.Connect_AWG)

        self.Connect_Probe_2 = QPushButton(self.frame_3)
        self.Connect_Probe_2.setObjectName(u"Connect_Probe_2")
        sizePolicy1.setHeightForWidth(self.Connect_Probe_2.sizePolicy().hasHeightForWidth())
        self.Connect_Probe_2.setSizePolicy(sizePolicy1)
        self.Connect_Probe_2.setMinimumSize(QSize(157, 0))
        self.Connect_Probe_2.setStyleSheet(u"\n"
                                           "font: 12pt \"Arial\";border-radius:10px;")

        self.horizontalLayout_6.addWidget(self.Connect_Probe_2)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_2)

        self.frame_25 = QFrame(self.frame_3)
        self.frame_25.setObjectName(u"frame_25")
        self.frame_25.setMinimumSize(QSize(150, 0))
        self.frame_25.setFrameShape(QFrame.StyledPanel)
        self.frame_25.setFrameShadow(QFrame.Raised)
        self.label_15 = QLabel(self.frame_25)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(30, 10, 54, 12))

        self.horizontalLayout_6.addWidget(self.frame_25)

        self.verticalLayout.addWidget(self.frame_3)

        self.tab = QTabWidget(Form)
        self.tab.setObjectName(u"tab")
        self.tab.setStyleSheet(u"QTabBar::tab{width:150px;}\n"
                               "QTabBar::tab{height:35px;}\n"
                               "border-radius:10px;\n"
                               "font: 12pt \"Arial\";")
        self.tab.setIconSize(QSize(16, 16))
        self.tab.setElideMode(Qt.ElideLeft)
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.gridLayout_8 = QGridLayout(self.tab_3)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setHorizontalSpacing(0)
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.frame_19 = QFrame(self.tab_3)
        self.frame_19.setObjectName(u"frame_19")
        sizePolicy.setHeightForWidth(self.frame_19.sizePolicy().hasHeightForWidth())
        self.frame_19.setSizePolicy(sizePolicy)
        self.frame_19.setMinimumSize(QSize(946, 500))
        self.frame_19.setStyleSheet(u"")
        self.frame_19.setFrameShape(QFrame.StyledPanel)
        self.frame_19.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_17 = QHBoxLayout(self.frame_19)
        self.horizontalLayout_17.setSpacing(0)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.frame_20 = QFrame(self.frame_19)
        self.frame_20.setObjectName(u"frame_20")
        self.frame_20.setMinimumSize(QSize(600, 0))
        self.frame_20.setFrameShape(QFrame.StyledPanel)
        self.frame_20.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_18 = QHBoxLayout(self.frame_20)
        self.horizontalLayout_18.setSpacing(0)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.scrollArea_2 = QScrollArea(self.frame_20)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setMinimumSize(QSize(650, 0))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 648, 495))
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.horizontalLayout_18.addWidget(self.scrollArea_2)

        self.horizontalLayout_17.addWidget(self.frame_20)

        self.frame_34 = QFrame(self.frame_19)
        self.frame_34.setObjectName(u"frame_34")
        sizePolicy.setHeightForWidth(self.frame_34.sizePolicy().hasHeightForWidth())
        self.frame_34.setSizePolicy(sizePolicy)
        self.frame_34.setMinimumSize(QSize(232, 0))
        self.frame_34.setFrameShape(QFrame.StyledPanel)
        self.frame_34.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame_34)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 2)
        self.frame_35 = QFrame(self.frame_34)
        self.frame_35.setObjectName(u"frame_35")
        self.frame_35.setMinimumSize(QSize(0, 0))
        self.frame_35.setStyleSheet(u"")
        self.frame_35.setFrameShape(QFrame.StyledPanel)
        self.frame_35.setFrameShadow(QFrame.Raised)
        self.gridLayout_9 = QGridLayout(self.frame_35)
        self.gridLayout_9.setSpacing(0)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.textEdit = QTextEdit(self.frame_35)
        self.textEdit.setObjectName(u"textEdit")

        self.gridLayout_9.addWidget(self.textEdit, 0, 0, 1, 1)

        self.verticalLayout_7.addWidget(self.frame_35)

        self.frame_36 = QFrame(self.frame_34)
        self.frame_36.setObjectName(u"frame_36")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frame_36.sizePolicy().hasHeightForWidth())
        self.frame_36.setSizePolicy(sizePolicy2)
        self.frame_36.setMinimumSize(QSize(200, 129))
        self.frame_36.setMaximumSize(QSize(16777215, 129))
        self.frame_36.setFrameShape(QFrame.StyledPanel)
        self.frame_36.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frame_36)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.frame_37 = QFrame(self.frame_36)
        self.frame_37.setObjectName(u"frame_37")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.frame_37.sizePolicy().hasHeightForWidth())
        self.frame_37.setSizePolicy(sizePolicy3)
        self.frame_37.setMinimumSize(QSize(0, 30))
        self.frame_37.setMaximumSize(QSize(16777215, 30))
        self.frame_37.setFrameShape(QFrame.StyledPanel)
        self.frame_37.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_27 = QHBoxLayout(self.frame_37)
        self.horizontalLayout_27.setSpacing(0)
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.horizontalLayout_27.setContentsMargins(0, 0, 0, 0)
        self.label_12 = QLabel(self.frame_37)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_27.addWidget(self.label_12, 0, Qt.AlignHCenter)

        self.comboBox_2 = QComboBox(self.frame_37)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")
        self.comboBox_2.setMinimumSize(QSize(160, 0))

        self.horizontalLayout_27.addWidget(self.comboBox_2)

        self.verticalLayout_8.addWidget(self.frame_37)

        self.widget = QWidget(self.frame_36)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_4 = QVBoxLayout(self.widget)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.frame_4 = QFrame(self.widget)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setEnabled(True)
        sizePolicy.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy)
        self.frame_4.setMinimumSize(QSize(0, 0))
        self.frame_4.setMaximumSize(QSize(16777215, 16777215))
        self.frame_4.setStyleSheet(u"")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.repeat_times_2 = QLineEdit(self.frame_4)
        self.repeat_times_2.setObjectName(u"repeat_times_2")

        self.gridLayout_3.addWidget(self.repeat_times_2, 0, 1, 1, 2)

        self.trig_2 = QPushButton(self.frame_4)
        self.trig_2.setObjectName(u"trig_2")
        self.trig_2.setMinimumSize(QSize(0, 20))
        self.trig_2.setStyleSheet(u"margin-left:5px;\n"
                                  "margin-right:5px;")

        self.gridLayout_3.addWidget(self.trig_2, 2, 2, 1, 1)

        self.label_11 = QLabel(self.frame_4)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setStyleSheet(u"font: 9pt \"Arial\";")

        self.gridLayout_3.addWidget(self.label_11, 1, 0, 1, 1)

        self.internal = QPushButton(self.frame_4)
        self.internal.setObjectName(u"internal")
        self.internal.setMinimumSize(QSize(0, 16))
        self.internal.setStyleSheet(u"background-color: rgb(85, 170, 255);\n"
                                    "margin-right:5px;")

        self.gridLayout_3.addWidget(self.internal, 2, 0, 1, 1)

        self.trigger_cycle = QLineEdit(self.frame_4)
        self.trigger_cycle.setObjectName(u"trigger_cycle")

        self.gridLayout_3.addWidget(self.trigger_cycle, 1, 1, 1, 2)

        self.config = QPushButton(self.frame_4)
        self.config.setObjectName(u"config")
        self.config.setMinimumSize(QSize(0, 20))
        self.config.setStyleSheet(u"margin-left:5px;\n"
                                  "margin-right:5px;")

        self.gridLayout_3.addWidget(self.config, 2, 1, 1, 1)

        self.label_10 = QLabel(self.frame_4)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setStyleSheet(u"font: 9pt \"Arial\";")

        self.gridLayout_3.addWidget(self.label_10, 0, 0, 1, 1)

        self.verticalLayout_3.addWidget(self.frame_4)

        self.frame_2 = QFrame(self.widget)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setMinimumSize(QSize(0, 0))
        self.frame_2.setMaximumSize(QSize(16777215, 16777215))
        self.frame_2.setStyleSheet(u"")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_2)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pushButton_3 = QPushButton(self.frame_2)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setMinimumSize(QSize(0, 20))
        self.pushButton_3.setStyleSheet(u"margin-left:5px;\n"
                                        "margin-right:5px;")

        self.gridLayout_2.addWidget(self.pushButton_3, 1, 2, 1, 1)

        self.lineEdit = QLineEdit(self.frame_2)
        self.lineEdit.setObjectName(u"lineEdit")

        self.gridLayout_2.addWidget(self.lineEdit, 0, 1, 1, 2)

        self.pushButton_2 = QPushButton(self.frame_2)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(0, 20))
        self.pushButton_2.setStyleSheet(u"margin-left:5px;\n"
                                        "margin-right:5px;")

        self.gridLayout_2.addWidget(self.pushButton_2, 1, 1, 1, 1)

        self.pushButton = QPushButton(self.frame_2)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setStyleSheet(u"background-color: rgb(85, 170, 255);\n"
                                      "margin-right:5px;\n"
                                      "margin-left:5px;\n"
                                      "")

        self.gridLayout_2.addWidget(self.pushButton, 1, 0, 1, 1)

        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"font: 9pt \"Arial\";\n"
                                   "margin-right:5px;\n"
                                   "margin-left:5px;")

        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)

        self.verticalLayout_3.addWidget(self.frame_2)

        self.frame_38 = QFrame(self.widget)
        self.frame_38.setObjectName(u"frame_38")
        sizePolicy3.setHeightForWidth(self.frame_38.sizePolicy().hasHeightForWidth())
        self.frame_38.setSizePolicy(sizePolicy3)
        self.frame_38.setMinimumSize(QSize(0, 0))
        self.frame_38.setFrameShape(QFrame.StyledPanel)
        self.frame_38.setFrameShadow(QFrame.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_38)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.config_2 = QPushButton(self.frame_38)
        self.config_2.setObjectName(u"config_2")
        self.config_2.setMinimumSize(QSize(0, 20))
        self.config_2.setStyleSheet(u"margin-left:5px;\n"
                                    "margin-right:5px;")

        self.gridLayout_7.addWidget(self.config_2, 1, 1, 1, 1)

        self.Manual_2 = QPushButton(self.frame_38)
        self.Manual_2.setObjectName(u"Manual_2")
        self.Manual_2.setMinimumSize(QSize(0, 16))
        self.Manual_2.setStyleSheet(u"background-color: rgb(216, 216, 162);\n"
                                    "margin-right:5px;\n"
                                    "margin-left:5px;")

        self.gridLayout_7.addWidget(self.Manual_2, 1, 0, 1, 1)

        self.label_13 = QLabel(self.frame_38)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(76, 0))
        self.label_13.setStyleSheet(u"font: 9pt \"Arial\";")

        self.gridLayout_7.addWidget(self.label_13, 0, 0, 1, 1)

        self.lineEdit_2 = QLineEdit(self.frame_38)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.gridLayout_7.addWidget(self.lineEdit_2, 0, 1, 1, 2)

        self.Trig_2 = QPushButton(self.frame_38)
        self.Trig_2.setObjectName(u"Trig_2")
        self.Trig_2.setMinimumSize(QSize(0, 20))
        self.Trig_2.setStyleSheet(u"margin-left:5px;\n"
                                  "margin-right:5px;")

        self.gridLayout_7.addWidget(self.Trig_2, 1, 2, 1, 1)

        self.verticalLayout_3.addWidget(self.frame_38)

        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.verticalLayout_8.addWidget(self.widget)

        self.verticalLayout_7.addWidget(self.frame_36)

        self.horizontalLayout_17.addWidget(self.frame_34)

        self.gridLayout_8.addWidget(self.frame_19, 0, 0, 1, 1)

        self.tab.addTab(self.tab_3, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.formLayout_2 = QFormLayout(self.tab_2)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setHorizontalSpacing(0)
        self.formLayout_2.setVerticalSpacing(0)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_39 = QFrame(self.tab_2)
        self.frame_39.setObjectName(u"frame_39")
        sizePolicy.setHeightForWidth(self.frame_39.sizePolicy().hasHeightForWidth())
        self.frame_39.setSizePolicy(sizePolicy)
        self.frame_39.setMinimumSize(QSize(946, 500))
        self.frame_39.setFrameShape(QFrame.StyledPanel)
        self.frame_39.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_28 = QHBoxLayout(self.frame_39)
        self.horizontalLayout_28.setSpacing(0)
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.horizontalLayout_28.setContentsMargins(0, 0, 0, 0)
        self.frame_40 = QFrame(self.frame_39)
        self.frame_40.setObjectName(u"frame_40")
        self.frame_40.setMinimumSize(QSize(650, 0))
        self.frame_40.setFrameShape(QFrame.StyledPanel)
        self.frame_40.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_40)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.page10 = QWidget(self.frame_40)
        self.page10.setObjectName(u"page10")

        self.gridLayout_4.addWidget(self.page10, 2, 2, 1, 1)

        self.page1 = QWidget(self.frame_40)
        self.page1.setObjectName(u"page1")
        self.page1.setMinimumSize(QSize(120, 0))

        self.gridLayout_4.addWidget(self.page1, 0, 1, 1, 1)

        self.page2 = QWidget(self.frame_40)
        self.page2.setObjectName(u"page2")
        self.page2.setMinimumSize(QSize(120, 0))

        self.gridLayout_4.addWidget(self.page2, 0, 2, 1, 1)

        self.page9 = QWidget(self.frame_40)
        self.page9.setObjectName(u"page9")

        self.gridLayout_4.addWidget(self.page9, 2, 1, 1, 1)

        self.page0 = QWidget(self.frame_40)
        self.page0.setObjectName(u"page0")
        self.page0.setMinimumSize(QSize(120, 0))

        self.gridLayout_4.addWidget(self.page0, 0, 0, 1, 1)

        self.page2_2 = QWidget(self.frame_40)
        self.page2_2.setObjectName(u"page2_2")

        self.gridLayout_4.addWidget(self.page2_2, 1, 0, 1, 1)

        self.page6 = QWidget(self.frame_40)
        self.page6.setObjectName(u"page6")

        self.gridLayout_4.addWidget(self.page6, 1, 1, 1, 1)

        self.page7 = QWidget(self.frame_40)
        self.page7.setObjectName(u"page7")

        self.gridLayout_4.addWidget(self.page7, 1, 3, 1, 1)

        self.page11 = QWidget(self.frame_40)
        self.page11.setObjectName(u"page11")

        self.gridLayout_4.addWidget(self.page11, 2, 3, 1, 1)

        self.page8 = QWidget(self.frame_40)
        self.page8.setObjectName(u"page8")

        self.gridLayout_4.addWidget(self.page8, 2, 0, 1, 1)

        self.page6_2 = QWidget(self.frame_40)
        self.page6_2.setObjectName(u"page6_2")

        self.gridLayout_4.addWidget(self.page6_2, 1, 2, 1, 1)

        self.horizontalLayout_28.addWidget(self.frame_40)

        self.frame_41 = QFrame(self.frame_39)
        self.frame_41.setObjectName(u"frame_41")
        self.frame_41.setMinimumSize(QSize(288, 0))
        self.frame_41.setFrameShape(QFrame.StyledPanel)
        self.frame_41.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.frame_41)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.frame_42 = QFrame(self.frame_41)
        self.frame_42.setObjectName(u"frame_42")
        self.frame_42.setFrameShape(QFrame.StyledPanel)
        self.frame_42.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_42)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_4 = QLabel(self.frame_42)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_5.addWidget(self.label_4, 1, 0, 1, 1, Qt.AlignHCenter)

        self.PointNumber = QLineEdit(self.frame_42)
        self.PointNumber.setObjectName(u"PointNumber")

        self.gridLayout_5.addWidget(self.PointNumber, 1, 1, 1, 1)

        self.comboBox_3 = QComboBox(self.frame_42)
        self.comboBox_3.addItem("")
        self.comboBox_3.setObjectName(u"comboBox_3")

        self.gridLayout_5.addWidget(self.comboBox_3, 4, 1, 1, 1)

        self.teiggerdelay = QLineEdit(self.frame_42)
        self.teiggerdelay.setObjectName(u"teiggerdelay")

        self.gridLayout_5.addWidget(self.teiggerdelay, 3, 1, 1, 1)

        self.label_5 = QLabel(self.frame_42)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_5.addWidget(self.label_5, 4, 0, 1, 1)

        self.label_3 = QLabel(self.frame_42)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_5.addWidget(self.label_3, 0, 0, 1, 1, Qt.AlignHCenter)

        self.shots = QLineEdit(self.frame_42)
        self.shots.setObjectName(u"shots")

        self.gridLayout_5.addWidget(self.shots, 0, 1, 1, 1)

        self.teigger = QLabel(self.frame_42)
        self.teigger.setObjectName(u"teigger")

        self.gridLayout_5.addWidget(self.teigger, 3, 0, 1, 1, Qt.AlignHCenter)

        self.page3 = QWidget(self.frame_42)
        self.page3.setObjectName(u"page3")
        self.page3.setMinimumSize(QSize(120, 0))

        self.gridLayout_5.addWidget(self.page3, 2, 0, 1, 1)

        self.verticalLayout_9.addWidget(self.frame_42)

        self.frame_43 = QFrame(self.frame_41)
        self.frame_43.setObjectName(u"frame_43")
        self.frame_43.setFrameShape(QFrame.StyledPanel)
        self.frame_43.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_43)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label_7 = QLabel(self.frame_43)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_6.addWidget(self.label_7, 1, 0, 1, 1, Qt.AlignHCenter)

        self.label_6 = QLabel(self.frame_43)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_6.addWidget(self.label_6, 0, 0, 1, 1, Qt.AlignHCenter)

        self.label_8 = QLabel(self.frame_43)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_6.addWidget(self.label_8, 3, 0, 1, 2, Qt.AlignHCenter)

        self.FrequencyList = QLineEdit(self.frame_43)
        self.FrequencyList.setObjectName(u"FrequencyList")

        self.gridLayout_6.addWidget(self.FrequencyList, 0, 1, 1, 1)

        self.Phase = QLineEdit(self.frame_43)
        self.Phase.setObjectName(u"Phase")

        self.gridLayout_6.addWidget(self.Phase, 1, 1, 1, 1)

        self.select_file_path = QPushButton(self.frame_43)
        self.select_file_path.setObjectName(u"select_file_path")
        self.select_file_path.setMinimumSize(QSize(200, 0))
        self.select_file_path.setMaximumSize(QSize(200, 16777215))

        self.gridLayout_6.addWidget(self.select_file_path, 2, 0, 1, 2, Qt.AlignHCenter)

        self.verticalLayout_9.addWidget(self.frame_43)

        self.frame_44 = QFrame(self.frame_41)
        self.frame_44.setObjectName(u"frame_44")
        self.frame_44.setFrameShape(QFrame.StyledPanel)
        self.frame_44.setFrameShadow(QFrame.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.frame_44)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.frame_45 = QFrame(self.frame_44)
        self.frame_45.setObjectName(u"frame_45")
        self.frame_45.setMinimumSize(QSize(0, 30))
        self.frame_45.setMaximumSize(QSize(16777215, 30))
        self.frame_45.setFrameShape(QFrame.StyledPanel)
        self.frame_45.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_29 = QHBoxLayout(self.frame_45)
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.horizontalLayout_29.setContentsMargins(0, 0, 0, 0)
        self.label_9 = QLabel(self.frame_45)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_29.addWidget(self.label_9)

        self.Trig_Mode = QComboBox(self.frame_45)
        self.Trig_Mode.addItem("")
        self.Trig_Mode.addItem("")
        self.Trig_Mode.addItem("")
        self.Trig_Mode.setObjectName(u"Trig_Mode")
        self.Trig_Mode.setMinimumSize(QSize(160, 0))

        self.horizontalLayout_29.addWidget(self.Trig_Mode)

        self.verticalLayout_10.addWidget(self.frame_45)

        self.frame_46 = QFrame(self.frame_44)
        self.frame_46.setObjectName(u"frame_46")
        self.frame_46.setFrameShape(QFrame.StyledPanel)
        self.frame_46.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_46)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_14 = QLabel(self.frame_46)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(76, 0))
        self.label_14.setStyleSheet(u"font: 9pt \"Arial\";")

        self.gridLayout.addWidget(self.label_14, 0, 0, 1, 1)

        self.repeat_times = QLineEdit(self.frame_46)
        self.repeat_times.setObjectName(u"repeat_times")

        self.gridLayout.addWidget(self.repeat_times, 0, 1, 1, 2)

        self.manual = QPushButton(self.frame_46)
        self.manual.setObjectName(u"manual")
        self.manual.setMinimumSize(QSize(0, 16))
        self.manual.setStyleSheet(u"background-color: rgb(216, 216, 162);\n"
                                  "margin-right:5px;")

        self.gridLayout.addWidget(self.manual, 1, 0, 1, 1)

        self.config_3 = QPushButton(self.frame_46)
        self.config_3.setObjectName(u"config_3")
        self.config_3.setMinimumSize(QSize(0, 20))
        self.config_3.setStyleSheet(u"margin-left:5px;\n"
                                    "margin-right:5px;")

        self.gridLayout.addWidget(self.config_3, 1, 1, 1, 1)

        self.trig = QPushButton(self.frame_46)
        self.trig.setObjectName(u"trig")
        self.trig.setMinimumSize(QSize(0, 20))
        self.trig.setStyleSheet(u"margin-left:5px;\n"
                                "margin-right:5px;")

        self.gridLayout.addWidget(self.trig, 1, 2, 1, 1)

        self.verticalLayout_10.addWidget(self.frame_46)

        self.verticalLayout_9.addWidget(self.frame_44)

        self.horizontalLayout_28.addWidget(self.frame_41)

        self.formLayout_2.setWidget(0, QFormLayout.SpanningRole, self.frame_39)

        self.tab.addTab(self.tab_2, "")

        self.verticalLayout.addWidget(self.tab)

        self.retranslateUi(Form)

        self.tab.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"        UltraMCI", None))
        # if QT_CONFIG(tooltip)
        self.btn_min.setToolTip(QCoreApplication.translate("Form", u"min", None))
        # endif // QT_CONFIG(tooltip)
        self.btn_min.setText("")
        # if QT_CONFIG(tooltip)
        self.btn_max.setToolTip(QCoreApplication.translate("Form", u"max", None))
        # endif // QT_CONFIG(tooltip)
        self.btn_max.setText("")
        # if QT_CONFIG(tooltip)
        self.btn_close.setToolTip(QCoreApplication.translate("Form", u"close", None))
        # endif // QT_CONFIG(tooltip)
        self.btn_close.setText("")
        self.Connect_AWG.setText(QCoreApplication.translate("Form", u"Connect  AWG", None))
        self.Connect_Probe_2.setText(QCoreApplication.translate("Form", u"Connect  Probe", None))
        self.label_15.setText(QCoreApplication.translate("Form", u"\u9884\u7559logo", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"Trig Mode", None))
        self.comboBox_2.setItemText(0, QCoreApplication.translate("Form", u"Manual Trigger", None))
        self.comboBox_2.setItemText(1, QCoreApplication.translate("Form", u"Internl Trigger", None))
        self.comboBox_2.setItemText(2, QCoreApplication.translate("Form", u"Externl Trigger", None))

        self.trig_2.setText(QCoreApplication.translate("Form", u"Trig", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"trigger cycle", None))
        self.internal.setText(QCoreApplication.translate("Form", u"Internal", None))
        self.config.setText(QCoreApplication.translate("Form", u"config", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"repeat times", None))
        self.pushButton_3.setText(QCoreApplication.translate("Form", u"config", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"config", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"External", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"repaet times", None))
        self.config_2.setText(QCoreApplication.translate("Form", u"config", None))
        self.Manual_2.setText(QCoreApplication.translate("Form", u"Manual", None))
        self.label_13.setText(QCoreApplication.translate("Form", u"repeat times", None))
        self.Trig_2.setText(QCoreApplication.translate("Form", u"Trig", None))
        self.tab.setTabText(self.tab.indexOf(self.tab_3), QCoreApplication.translate("Form", u"AWG-0", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"PointNumber", None))
        self.comboBox_3.setItemText(0, QCoreApplication.translate("Form", u"MODE-1", None))

        self.label_5.setText(QCoreApplication.translate("Form", u"DemodParam from", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"shots", None))
        self.teigger.setText(QCoreApplication.translate("Form", u"TriggerDelay", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"Phase", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"FrequencyList", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"Patn to DemodParam file", None))
        self.select_file_path.setText(QCoreApplication.translate("Form", u"select file path", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"Trig Mode", None))
        self.Trig_Mode.setItemText(0, QCoreApplication.translate("Form", u"Manual Trigger", None))
        self.Trig_Mode.setItemText(1, QCoreApplication.translate("Form", u"Internl Trigger", None))
        self.Trig_Mode.setItemText(2, QCoreApplication.translate("Form", u"Externl Trigger", None))

        self.label_14.setText(QCoreApplication.translate("Form", u"repeat times", None))
        self.manual.setText(QCoreApplication.translate("Form", u"Manual", None))
        self.config_3.setText(QCoreApplication.translate("Form", u"config", None))
        self.trig.setText(QCoreApplication.translate("Form", u"Trig", None))
        self.tab.setTabText(self.tab.indexOf(self.tab_2), QCoreApplication.translate("Form", u"probe-0", None))
    # retranslateUi
