# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addtabpage.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_addtab(object):
    def setupUi(self, addtab):
        addtab.setObjectName("addtab")
        addtab.resize(1164, 502)
        self.gridLayout = QtWidgets.QGridLayout(addtab)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(addtab)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.frame_19 = QtWidgets.QFrame(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_19.sizePolicy().hasHeightForWidth())
        self.frame_19.setSizePolicy(sizePolicy)
        self.frame_19.setMinimumSize(QtCore.QSize(946, 500))
        self.frame_19.setStyleSheet("")
        self.frame_19.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_19.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_19.setObjectName("frame_19")
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout(self.frame_19)
        self.horizontalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_17.setSpacing(0)
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.frame_20 = QtWidgets.QFrame(self.frame_19)
        self.frame_20.setMinimumSize(QtCore.QSize(600, 0))
        self.frame_20.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_20.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_20.setObjectName("frame_20")
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout(self.frame_20)
        self.horizontalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_18.setSpacing(0)
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.scrollArea_2 = QtWidgets.QScrollArea(self.frame_20)
        self.scrollArea_2.setMinimumSize(QtCore.QSize(650, 0))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 656, 494))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.horizontalLayout_18.addWidget(self.scrollArea_2)
        self.horizontalLayout_17.addWidget(self.frame_20)
        self.frame_34 = QtWidgets.QFrame(self.frame_19)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_34.sizePolicy().hasHeightForWidth())
        self.frame_34.setSizePolicy(sizePolicy)
        self.frame_34.setMinimumSize(QtCore.QSize(500, 499))
        self.frame_34.setMaximumSize(QtCore.QSize(500, 16777215))
        self.frame_34.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_34.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_34.setObjectName("frame_34")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frame_34)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 2)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.frame_35 = QtWidgets.QFrame(self.frame_34)
        self.frame_35.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_35.setStyleSheet("")
        self.frame_35.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_35.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_35.setObjectName("frame_35")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_35)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 2)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.textEditpy = QtWebEngineWidgets.QWebEngineView(self.frame_35)
        self.textEditpy.setUrl(QtCore.QUrl("about:blank"))
        self.textEditpy.setObjectName("textEditpy")
        self.verticalLayout_5.addWidget(self.textEditpy)
        self.changepy = QtWidgets.QPushButton(self.frame_35)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.changepy.sizePolicy().hasHeightForWidth())
        self.changepy.setSizePolicy(sizePolicy)
        self.changepy.setMinimumSize(QtCore.QSize(0, 25))
        self.changepy.setStyleSheet("margin-right:50px;\n"
"margin-left:50px;\n"
"margin-top:3px;")
        self.changepy.setObjectName("changepy")
        self.verticalLayout_5.addWidget(self.changepy)
        self.verticalLayout_7.addWidget(self.frame_35)
        self.frame_36 = QtWidgets.QFrame(self.frame_34)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_36.sizePolicy().hasHeightForWidth())
        self.frame_36.setSizePolicy(sizePolicy)
        self.frame_36.setMinimumSize(QtCore.QSize(200, 129))
        self.frame_36.setMaximumSize(QtCore.QSize(16777215, 129))
        self.frame_36.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_36.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_36.setObjectName("frame_36")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.frame_36)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.frame_37 = QtWidgets.QFrame(self.frame_36)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_37.sizePolicy().hasHeightForWidth())
        self.frame_37.setSizePolicy(sizePolicy)
        self.frame_37.setMinimumSize(QtCore.QSize(0, 30))
        self.frame_37.setMaximumSize(QtCore.QSize(16777215, 30))
        self.frame_37.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_37.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_37.setObjectName("frame_37")
        self.horizontalLayout_27 = QtWidgets.QHBoxLayout(self.frame_37)
        self.horizontalLayout_27.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_27.setSpacing(0)
        self.horizontalLayout_27.setObjectName("horizontalLayout_27")
        self.label_12 = QtWidgets.QLabel(self.frame_37)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_27.addWidget(self.label_12, 0, QtCore.Qt.AlignHCenter)
        self.comboBox_2 = QtWidgets.QComboBox(self.frame_37)
        self.comboBox_2.setMinimumSize(QtCore.QSize(160, 0))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.horizontalLayout_27.addWidget(self.comboBox_2)
        self.verticalLayout_8.addWidget(self.frame_37)
        self.widget = QtWidgets.QWidget(self.frame_36)
        self.widget.setObjectName("widget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame_manual = QtWidgets.QFrame(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_manual.sizePolicy().hasHeightForWidth())
        self.frame_manual.setSizePolicy(sizePolicy)
        self.frame_manual.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_manual.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_manual.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_manual.setObjectName("frame_manual")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.frame_manual)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.manual_config = QtWidgets.QPushButton(self.frame_manual)
        self.manual_config.setMinimumSize(QtCore.QSize(0, 25))
        self.manual_config.setStyleSheet("margin-left:5px;\n"
"margin-right:5px;")
        self.manual_config.setObjectName("manual_config")
        self.gridLayout_7.addWidget(self.manual_config, 1, 1, 1, 1)
        self.manual_trig = QtWidgets.QPushButton(self.frame_manual)
        self.manual_trig.setMinimumSize(QtCore.QSize(0, 25))
        self.manual_trig.setStyleSheet("margin-left:5px;\n"
"margin-right:5px;")
        self.manual_trig.setObjectName("manual_trig")
        self.gridLayout_7.addWidget(self.manual_trig, 1, 2, 1, 1)
        self.Manual_2 = QtWidgets.QPushButton(self.frame_manual)
        self.Manual_2.setMinimumSize(QtCore.QSize(0, 25))
        self.Manual_2.setStyleSheet("margin-right:5px;\n"
"margin-left:5px;")
        self.Manual_2.setObjectName("Manual_2")
        self.gridLayout_7.addWidget(self.Manual_2, 1, 0, 1, 1)
        self.manual_trigge_cycle = QtWidgets.QLineEdit(self.frame_manual)
        self.manual_trigge_cycle.setStyleSheet("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
"<ui version=\"4.0\">\n"
" <widget name=\"__qt_fake_top_level\">\n"
"  <widget class=\"QLineEdit\" name=\"lineEdit\">\n"
"   <property name=\"geometry\">\n"
"    <rect>\n"
"     <x>99</x>\n"
"     <y>1</y>\n"
"     <width>186</width>\n"
"     <height>19</height>\n"
"    </rect>\n"
"   </property>\n"
"   <property name=\"styleSheet\">\n"
"    <string notr=\"true\">margin-right:10px;</string>\n"
"   </property>\n"
"  </widget>\n"
" </widget>\n"
" <resources/>\n"
"</ui>\n"
"")
        self.manual_trigge_cycle.setObjectName("manual_trigge_cycle")
        self.gridLayout_7.addWidget(self.manual_trigge_cycle, 0, 1, 1, 2)
        self.label_13 = QtWidgets.QLabel(self.frame_manual)
        self.label_13.setMinimumSize(QtCore.QSize(76, 0))
        self.label_13.setStyleSheet("font: 9pt \"Arial\";")
        self.label_13.setObjectName("label_13")
        self.gridLayout_7.addWidget(self.label_13, 0, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.frame_manual)
        self.frame_external = QtWidgets.QFrame(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_external.sizePolicy().hasHeightForWidth())
        self.frame_external.setSizePolicy(sizePolicy)
        self.frame_external.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_external.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_external.setStyleSheet("")
        self.frame_external.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_external.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_external.setObjectName("frame_external")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_external)
        self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.external_trig = QtWidgets.QPushButton(self.frame_external)
        self.external_trig.setMinimumSize(QtCore.QSize(0, 25))
        self.external_trig.setStyleSheet("margin-left:5px;\n"
"margin-right:5px;")
        self.external_trig.setObjectName("external_trig")
        self.gridLayout_2.addWidget(self.external_trig, 0, 2, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.frame_external)
        self.pushButton.setMinimumSize(QtCore.QSize(152, 25))
        self.pushButton.setMaximumSize(QtCore.QSize(152, 16777215))
        self.pushButton.setStyleSheet("margin-right:5px;\n"
"")
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 0, 0, 1, 1)
        self.external_config = QtWidgets.QPushButton(self.frame_external)
        self.external_config.setMinimumSize(QtCore.QSize(0, 25))
        self.external_config.setStyleSheet("margin-left:10px;\n"
"margin-right:5px;")
        self.external_config.setObjectName("external_config")
        self.gridLayout_2.addWidget(self.external_config, 0, 1, 1, 1)
        self.verticalLayout_3.addWidget(self.frame_external)
        self.frame_internal = QtWidgets.QFrame(self.widget)
        self.frame_internal.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_internal.sizePolicy().hasHeightForWidth())
        self.frame_internal.setSizePolicy(sizePolicy)
        self.frame_internal.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_internal.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_internal.setStyleSheet("")
        self.frame_internal.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_internal.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_internal.setObjectName("frame_internal")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_internal)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_11 = QtWidgets.QLabel(self.frame_internal)
        self.label_11.setStyleSheet("font: 9pt \"Arial\";")
        self.label_11.setObjectName("label_11")
        self.gridLayout_3.addWidget(self.label_11, 1, 0, 1, 1)
        self.internal_config = QtWidgets.QPushButton(self.frame_internal)
        self.internal_config.setMinimumSize(QtCore.QSize(0, 25))
        self.internal_config.setStyleSheet("margin-left:5px;\n"
"margin-right:5px;")
        self.internal_config.setObjectName("internal_config")
        self.gridLayout_3.addWidget(self.internal_config, 2, 1, 1, 1)
        self.trigger_cycle = QtWidgets.QLineEdit(self.frame_internal)
        self.trigger_cycle.setObjectName("trigger_cycle")
        self.gridLayout_3.addWidget(self.trigger_cycle, 1, 1, 1, 2)
        self.internal = QtWidgets.QPushButton(self.frame_internal)
        self.internal.setMinimumSize(QtCore.QSize(0, 25))
        self.internal.setStyleSheet("margin-right:5px;")
        self.internal.setObjectName("internal")
        self.gridLayout_3.addWidget(self.internal, 2, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.frame_internal)
        self.label_10.setStyleSheet("font: 9pt \"Arial\";")
        self.label_10.setObjectName("label_10")
        self.gridLayout_3.addWidget(self.label_10, 0, 0, 1, 1)
        self.internal_trig = QtWidgets.QPushButton(self.frame_internal)
        self.internal_trig.setMinimumSize(QtCore.QSize(0, 25))
        self.internal_trig.setStyleSheet("margin-left:5px;\n"
"margin-right:5px;")
        self.internal_trig.setObjectName("internal_trig")
        self.gridLayout_3.addWidget(self.internal_trig, 2, 2, 1, 1)
        self.repeat_times_2 = QtWidgets.QLineEdit(self.frame_internal)
        self.repeat_times_2.setObjectName("repeat_times_2")
        self.gridLayout_3.addWidget(self.repeat_times_2, 0, 1, 1, 2)
        self.verticalLayout_3.addWidget(self.frame_internal)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.verticalLayout_8.addWidget(self.widget)
        self.verticalLayout_7.addWidget(self.frame_36)
        self.horizontalLayout_17.addWidget(self.frame_34)
        self.gridLayout_4.addWidget(self.frame_19, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.retranslateUi(addtab)
        QtCore.QMetaObject.connectSlotsByName(addtab)

    def retranslateUi(self, addtab):
        _translate = QtCore.QCoreApplication.translate
        addtab.setWindowTitle(_translate("addtab", "Form"))
        self.changepy.setText(_translate("addtab", "Connect"))
        self.label_12.setText(_translate("addtab", "Trig Mode"))
        self.comboBox_2.setItemText(0, _translate("addtab", "Manual Trigger"))
        self.comboBox_2.setItemText(1, _translate("addtab", "Internl Trigger"))
        self.comboBox_2.setItemText(2, _translate("addtab", "Externl Trigger"))
        self.manual_config.setText(_translate("addtab", "config"))
        self.manual_trig.setText(_translate("addtab", "Trig"))
        self.Manual_2.setText(_translate("addtab", "Manual"))
        self.label_13.setText(_translate("addtab", "trigger cycle"))
        self.external_trig.setText(_translate("addtab", "Trig"))
        self.pushButton.setText(_translate("addtab", "External"))
        self.external_config.setText(_translate("addtab", "config"))
        self.label_11.setText(_translate("addtab", "trigger cycle"))
        self.internal_config.setText(_translate("addtab", "config"))
        self.internal.setText(_translate("addtab", "Internal"))
        self.label_10.setText(_translate("addtab", "repeat times"))
        self.internal_trig.setText(_translate("addtab", "Trig"))
from PyQt5 import QtWebEngineWidgets
