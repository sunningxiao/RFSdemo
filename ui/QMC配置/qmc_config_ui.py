# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qmc_config_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1304, 473)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.gridFrame_2 = QtWidgets.QFrame(Dialog)
        self.gridFrame_2.setMinimumSize(QtCore.QSize(0, 150))
        self.gridFrame_2.setObjectName("gridFrame_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridFrame_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setSpacing(7)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.txt_dac_gain_7 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_dac_gain_7.setMinimumSize(QtCore.QSize(130, 0))
        self.txt_dac_gain_7.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.txt_dac_gain_7.setObjectName("txt_dac_gain_7")
        self.gridLayout_5.addWidget(self.txt_dac_gain_7, 19, 6, 1, 1)
        self.line_21 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_21.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_21.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_21.setObjectName("line_21")
        self.gridLayout_5.addWidget(self.line_21, 17, 5, 1, 1)
        self.line_16 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_16.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_16.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_16.setObjectName("line_16")
        self.gridLayout_5.addWidget(self.line_16, 7, 5, 1, 1)
        self.label_37 = QtWidgets.QLabel(self.gridFrame_2)
        self.label_37.setMinimumSize(QtCore.QSize(130, 0))
        self.label_37.setMaximumSize(QtCore.QSize(130, 16777215))
        self.label_37.setObjectName("label_37")
        self.gridLayout_5.addWidget(self.label_37, 15, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridFrame_2)
        self.label_4.setMinimumSize(QtCore.QSize(130, 0))
        self.label_4.setMaximumSize(QtCore.QSize(130, 16777215))
        self.label_4.setObjectName("label_4")
        self.gridLayout_5.addWidget(self.label_4, 11, 0, 1, 1)
        self.line_4 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridLayout_5.addWidget(self.line_4, 10, 0, 1, 1)
        self.line_33 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_33.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_33.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_33.setObjectName("line_33")
        self.gridLayout_5.addWidget(self.line_33, 14, 2, 1, 10)
        self.line = QtWidgets.QFrame(self.gridFrame_2)
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setObjectName("line")
        self.gridLayout_5.addWidget(self.line, 3, 1, 17, 1)
        self.txt_adc_gain_5 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_adc_gain_5.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.txt_adc_gain_5.setObjectName("txt_adc_gain_5")
        self.gridLayout_5.addWidget(self.txt_adc_gain_5, 15, 2, 1, 1)
        self.line_18 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_18.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_18.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_18.setObjectName("line_18")
        self.gridLayout_5.addWidget(self.line_18, 11, 5, 1, 1)
        self.txt_dac_gain_6 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_dac_gain_6.setMinimumSize(QtCore.QSize(130, 0))
        self.txt_dac_gain_6.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.txt_dac_gain_6.setObjectName("txt_dac_gain_6")
        self.gridLayout_5.addWidget(self.txt_dac_gain_6, 17, 6, 1, 1)
        self.txt_adc_gain_6 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_adc_gain_6.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.txt_adc_gain_6.setObjectName("txt_adc_gain_6")
        self.gridLayout_5.addWidget(self.txt_adc_gain_6, 17, 2, 1, 1)
        self.btn_config = QtWidgets.QPushButton(self.gridFrame_2)
        self.btn_config.setObjectName("btn_config")
        self.gridLayout_5.addWidget(self.btn_config, 21, 11, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.gridFrame_2)
        self.label_15.setMinimumSize(QtCore.QSize(0, 30))
        self.label_15.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.label_15.setObjectName("label_15")
        self.gridLayout_5.addWidget(self.label_15, 3, 3, 1, 1)
        self.txt_dac_gain_0 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_dac_gain_0.setMinimumSize(QtCore.QSize(130, 0))
        self.txt_dac_gain_0.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.txt_dac_gain_0.setObjectName("txt_dac_gain_0")
        self.gridLayout_5.addWidget(self.txt_dac_gain_0, 5, 6, 1, 1)
        self.line_31 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_31.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_31.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_31.setObjectName("line_31")
        self.gridLayout_5.addWidget(self.line_31, 10, 2, 1, 10)
        self.label_2 = QtWidgets.QLabel(self.gridFrame_2)
        self.label_2.setMinimumSize(QtCore.QSize(130, 0))
        self.label_2.setMaximumSize(QtCore.QSize(130, 16777215))
        self.label_2.setObjectName("label_2")
        self.gridLayout_5.addWidget(self.label_2, 7, 0, 1, 1)
        self.label_45 = QtWidgets.QLabel(self.gridFrame_2)
        self.label_45.setMinimumSize(QtCore.QSize(130, 0))
        self.label_45.setMaximumSize(QtCore.QSize(130, 16777215))
        self.label_45.setObjectName("label_45")
        self.gridLayout_5.addWidget(self.label_45, 19, 0, 1, 1)
        self.line_14 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_14.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_14.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_14.setObjectName("line_14")
        self.gridLayout_5.addWidget(self.line_14, 3, 5, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.gridFrame_2)
        self.label_14.setMinimumSize(QtCore.QSize(0, 30))
        self.label_14.setMaximumSize(QtCore.QSize(1000, 30))
        self.label_14.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.gridLayout_5.addWidget(self.label_14, 3, 2, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.gridFrame_2)
        self.label_16.setMinimumSize(QtCore.QSize(0, 30))
        self.label_16.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setObjectName("label_16")
        self.gridLayout_5.addWidget(self.label_16, 3, 4, 1, 1)
        self.line_10 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_10.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_10.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_10.setObjectName("line_10")
        self.gridLayout_5.addWidget(self.line_10, 8, 2, 1, 10)
        self.line_34 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_34.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_34.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_34.setObjectName("line_34")
        self.gridLayout_5.addWidget(self.line_34, 16, 2, 1, 10)
        self.line_11 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_11.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_11.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_11.setObjectName("line_11")
        self.gridLayout_5.addWidget(self.line_11, 4, 2, 1, 10)
        self.line_15 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_15.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_15.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_15.setObjectName("line_15")
        self.gridLayout_5.addWidget(self.line_15, 5, 5, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.gridFrame_2)
        self.label_18.setMinimumSize(QtCore.QSize(0, 30))
        self.label_18.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_18.setAlignment(QtCore.Qt.AlignCenter)
        self.label_18.setObjectName("label_18")
        self.gridLayout_5.addWidget(self.label_18, 3, 10, 1, 1)
        self.txt_dac_gain_3 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_dac_gain_3.setMinimumSize(QtCore.QSize(130, 0))
        self.txt_dac_gain_3.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.txt_dac_gain_3.setObjectName("txt_dac_gain_3")
        self.gridLayout_5.addWidget(self.txt_dac_gain_3, 11, 6, 1, 1)
        self.line_9 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_9.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.gridLayout_5.addWidget(self.line_9, 6, 2, 1, 10)
        self.label_41 = QtWidgets.QLabel(self.gridFrame_2)
        self.label_41.setMinimumSize(QtCore.QSize(130, 0))
        self.label_41.setMaximumSize(QtCore.QSize(130, 16777215))
        self.label_41.setObjectName("label_41")
        self.gridLayout_5.addWidget(self.label_41, 17, 0, 1, 1)
        self.line_17 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_17.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_17.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_17.setObjectName("line_17")
        self.gridLayout_5.addWidget(self.line_17, 9, 5, 1, 1)
        self.txt_adc_gain_7 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_adc_gain_7.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.txt_adc_gain_7.setObjectName("txt_adc_gain_7")
        self.gridLayout_5.addWidget(self.txt_adc_gain_7, 19, 2, 1, 1)
        self.txt_adc_gain_0 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_adc_gain_0.setMinimumSize(QtCore.QSize(130, 0))
        self.txt_adc_gain_0.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.txt_adc_gain_0.setObjectName("txt_adc_gain_0")
        self.gridLayout_5.addWidget(self.txt_adc_gain_0, 5, 2, 1, 1)
        self.line_20 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_20.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_20.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_20.setObjectName("line_20")
        self.gridLayout_5.addWidget(self.line_20, 15, 5, 1, 1)
        self.label_33 = QtWidgets.QLabel(self.gridFrame_2)
        self.label_33.setMinimumSize(QtCore.QSize(130, 0))
        self.label_33.setMaximumSize(QtCore.QSize(130, 16777215))
        self.label_33.setObjectName("label_33")
        self.gridLayout_5.addWidget(self.label_33, 13, 0, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.gridFrame_2)
        self.label_20.setMinimumSize(QtCore.QSize(0, 30))
        self.label_20.setMaximumSize(QtCore.QSize(1000, 30))
        self.label_20.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_20.setAlignment(QtCore.Qt.AlignCenter)
        self.label_20.setObjectName("label_20")
        self.gridLayout_5.addWidget(self.label_20, 3, 7, 1, 1)
        self.txt_adc_gain_2 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_adc_gain_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.txt_adc_gain_2.setObjectName("txt_adc_gain_2")
        self.gridLayout_5.addWidget(self.txt_adc_gain_2, 9, 2, 1, 1)
        self.txt_adc_gain_4 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_adc_gain_4.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.txt_adc_gain_4.setObjectName("txt_adc_gain_4")
        self.gridLayout_5.addWidget(self.txt_adc_gain_4, 13, 2, 1, 1)
        self.txt_adc_gain_3 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_adc_gain_3.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.txt_adc_gain_3.setObjectName("txt_adc_gain_3")
        self.gridLayout_5.addWidget(self.txt_adc_gain_3, 11, 2, 1, 1)
        self.label_19 = QtWidgets.QLabel(self.gridFrame_2)
        self.label_19.setMinimumSize(QtCore.QSize(0, 30))
        self.label_19.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_19.setAlignment(QtCore.Qt.AlignCenter)
        self.label_19.setObjectName("label_19")
        self.gridLayout_5.addWidget(self.label_19, 3, 11, 1, 1)
        self.txt_adc_gain_1 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_adc_gain_1.setMinimumSize(QtCore.QSize(130, 0))
        self.txt_adc_gain_1.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.txt_adc_gain_1.setObjectName("txt_adc_gain_1")
        self.gridLayout_5.addWidget(self.txt_adc_gain_1, 7, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridFrame_2)
        self.label_3.setMinimumSize(QtCore.QSize(130, 0))
        self.label_3.setMaximumSize(QtCore.QSize(130, 16777215))
        self.label_3.setObjectName("label_3")
        self.gridLayout_5.addWidget(self.label_3, 9, 0, 1, 1)
        self.btn_cancel = QtWidgets.QPushButton(self.gridFrame_2)
        self.btn_cancel.setObjectName("btn_cancel")
        self.gridLayout_5.addWidget(self.btn_cancel, 21, 0, 1, 1)
        self.line_22 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_22.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_22.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_22.setObjectName("line_22")
        self.gridLayout_5.addWidget(self.line_22, 19, 5, 1, 1)
        self.line_3 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout_5.addWidget(self.line_3, 8, 0, 1, 1)
        self.line_35 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_35.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_35.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_35.setObjectName("line_35")
        self.gridLayout_5.addWidget(self.line_35, 18, 2, 1, 10)
        self.txt_dac_gain_4 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_dac_gain_4.setMinimumSize(QtCore.QSize(130, 0))
        self.txt_dac_gain_4.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.txt_dac_gain_4.setObjectName("txt_dac_gain_4")
        self.gridLayout_5.addWidget(self.txt_dac_gain_4, 13, 6, 1, 1)
        self.line_12 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_12.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_12.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_12.setObjectName("line_12")
        self.gridLayout_5.addWidget(self.line_12, 4, 0, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.gridFrame_2)
        self.label_21.setMinimumSize(QtCore.QSize(0, 30))
        self.label_21.setMaximumSize(QtCore.QSize(1000, 30))
        self.label_21.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_21.setAlignment(QtCore.Qt.AlignCenter)
        self.label_21.setObjectName("label_21")
        self.gridLayout_5.addWidget(self.label_21, 3, 8, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.gridFrame_2)
        self.label_17.setMinimumSize(QtCore.QSize(0, 30))
        self.label_17.setMaximumSize(QtCore.QSize(1000, 30))
        self.label_17.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_17.setAlignment(QtCore.Qt.AlignCenter)
        self.label_17.setObjectName("label_17")
        self.gridLayout_5.addWidget(self.label_17, 3, 6, 1, 1)
        self.line_6 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.gridLayout_5.addWidget(self.line_6, 14, 0, 1, 1)
        self.txt_dac_gain_1 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_dac_gain_1.setMinimumSize(QtCore.QSize(130, 0))
        self.txt_dac_gain_1.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.txt_dac_gain_1.setObjectName("txt_dac_gain_1")
        self.gridLayout_5.addWidget(self.txt_dac_gain_1, 7, 6, 1, 1)
        self.line_19 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_19.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_19.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_19.setObjectName("line_19")
        self.gridLayout_5.addWidget(self.line_19, 13, 5, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout_5.addWidget(self.line_2, 6, 0, 1, 1)
        self.txt_dac_gain_2 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_dac_gain_2.setMinimumSize(QtCore.QSize(130, 0))
        self.txt_dac_gain_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.txt_dac_gain_2.setObjectName("txt_dac_gain_2")
        self.gridLayout_5.addWidget(self.txt_dac_gain_2, 9, 6, 1, 1)
        self.line_8 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.gridLayout_5.addWidget(self.line_8, 18, 0, 1, 1)
        self.txt_dac_gain_5 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_dac_gain_5.setMinimumSize(QtCore.QSize(130, 0))
        self.txt_dac_gain_5.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.txt_dac_gain_5.setObjectName("txt_dac_gain_5")
        self.gridLayout_5.addWidget(self.txt_dac_gain_5, 15, 6, 1, 1)
        self.label = QtWidgets.QLabel(self.gridFrame_2)
        self.label.setMinimumSize(QtCore.QSize(130, 0))
        self.label.setMaximumSize(QtCore.QSize(130, 16777215))
        self.label.setObjectName("label")
        self.gridLayout_5.addWidget(self.label, 5, 0, 1, 1)
        self.line_32 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_32.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_32.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_32.setObjectName("line_32")
        self.gridLayout_5.addWidget(self.line_32, 12, 2, 1, 10)
        self.line_7 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.gridLayout_5.addWidget(self.line_7, 16, 0, 1, 1)
        self.line_13 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_13.setMinimumSize(QtCore.QSize(0, 5))
        self.line_13.setMouseTracking(False)
        self.line_13.setFocusPolicy(QtCore.Qt.NoFocus)
        self.line_13.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_13.setLineWidth(5)
        self.line_13.setMidLineWidth(0)
        self.line_13.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_13.setObjectName("line_13")
        self.gridLayout_5.addWidget(self.line_13, 20, 0, 1, 12)
        self.line_5 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.gridLayout_5.addWidget(self.line_5, 12, 0, 1, 1)
        self.line_23 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_23.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_23.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_23.setObjectName("line_23")
        self.gridLayout_5.addWidget(self.line_23, 3, 9, 1, 1)
        self.line_24 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_24.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_24.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_24.setObjectName("line_24")
        self.gridLayout_5.addWidget(self.line_24, 5, 9, 1, 1)
        self.line_25 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_25.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_25.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_25.setObjectName("line_25")
        self.gridLayout_5.addWidget(self.line_25, 7, 9, 1, 1)
        self.line_26 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_26.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_26.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_26.setObjectName("line_26")
        self.gridLayout_5.addWidget(self.line_26, 9, 9, 1, 1)
        self.line_27 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_27.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_27.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_27.setObjectName("line_27")
        self.gridLayout_5.addWidget(self.line_27, 11, 9, 1, 1)
        self.line_28 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_28.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_28.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_28.setObjectName("line_28")
        self.gridLayout_5.addWidget(self.line_28, 13, 9, 1, 1)
        self.line_29 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_29.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_29.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_29.setObjectName("line_29")
        self.gridLayout_5.addWidget(self.line_29, 15, 9, 1, 1)
        self.line_30 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_30.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_30.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_30.setObjectName("line_30")
        self.gridLayout_5.addWidget(self.line_30, 17, 9, 1, 1)
        self.line_36 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_36.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_36.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_36.setObjectName("line_36")
        self.gridLayout_5.addWidget(self.line_36, 19, 9, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout_5, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.gridFrame_2, 0, 0, 1, 2)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_37.setText(_translate("Dialog", "通道6"))
        self.label_4.setText(_translate("Dialog", "通道4"))
        self.btn_config.setText(_translate("Dialog", "确定"))
        self.label_2.setText(_translate("Dialog", "通道2"))
        self.label_45.setText(_translate("Dialog", "通道8"))
        self.label_14.setText(_translate("Dialog", "ADC增益(dB)"))
        self.label_41.setText(_translate("Dialog", "通道7"))
        self.label_33.setText(_translate("Dialog", "通道5"))
        self.label_3.setText(_translate("Dialog", "通道3"))
        self.btn_cancel.setText(_translate("Dialog", "取消"))
        self.label_17.setText(_translate("Dialog", "DAC衰减(dB)"))
        self.label.setText(_translate("Dialog", "通道1"))
