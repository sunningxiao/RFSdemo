# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'start_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(859, 467)
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
        self.txt_sampling_delay_4 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_sampling_delay_4.setMaximumSize(QtCore.QSize(130, 16777215))
        self.txt_sampling_delay_4.setObjectName("txt_sampling_delay_4")
        self.gridLayout_5.addWidget(self.txt_sampling_delay_4, 12, 5, 1, 1)
        self.txt_prf_cyc = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_prf_cyc.setMaximumSize(QtCore.QSize(130, 16777215))
        self.txt_prf_cyc.setObjectName("txt_prf_cyc")
        self.gridLayout_5.addWidget(self.txt_prf_cyc, 0, 6, 1, 1)
        self.txt_gate_width_2 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_gate_width_2.setMaximumSize(QtCore.QSize(130, 16777215))
        self.txt_gate_width_2.setObjectName("txt_gate_width_2")
        self.gridLayout_5.addWidget(self.txt_gate_width_2, 8, 4, 1, 1)
        self.txt_gate_width_5 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_gate_width_5.setMaximumSize(QtCore.QSize(130, 16777215))
        self.txt_gate_width_5.setObjectName("txt_gate_width_5")
        self.gridLayout_5.addWidget(self.txt_gate_width_5, 14, 4, 1, 1)
        self.select_source_3 = QtWidgets.QComboBox(self.gridFrame_2)
        self.select_source_3.setMaximumSize(QtCore.QSize(130, 16777215))
        self.select_source_3.setObjectName("select_source_3")
        self.select_source_3.addItem("")
        self.select_source_3.addItem("")
        self.gridLayout_5.addWidget(self.select_source_3, 10, 2, 1, 1)
        self.txt_gate_width_0 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_gate_width_0.setMaximumSize(QtCore.QSize(130, 16777215))
        self.txt_gate_width_0.setObjectName("txt_gate_width_0")
        self.gridLayout_5.addWidget(self.txt_gate_width_0, 4, 4, 1, 1)
        self.txt_gate_delay_5 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_gate_delay_5.setMaximumSize(QtCore.QSize(130, 16777215))
        self.txt_gate_delay_5.setObjectName("txt_gate_delay_5")
        self.gridLayout_5.addWidget(self.txt_gate_delay_5, 14, 3, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.gridFrame_2)
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setObjectName("label_16")
        self.gridLayout_5.addWidget(self.label_16, 2, 4, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.gridFrame_2)
        self.label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.label_15.setObjectName("label_15")
        self.gridLayout_5.addWidget(self.label_15, 2, 3, 1, 1)
        self.label_45 = QtWidgets.QLabel(self.gridFrame_2)
        self.label_45.setObjectName("label_45")
        self.gridLayout_5.addWidget(self.label_45, 18, 0, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.gridFrame_2)
        self.label_18.setAlignment(QtCore.Qt.AlignCenter)
        self.label_18.setObjectName("label_18")
        self.gridLayout_5.addWidget(self.label_18, 2, 6, 1, 1)
        self.line_3 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout_5.addWidget(self.line_3, 7, 0, 1, 1)
        self.txt_sampling_points_2 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_sampling_points_2.setMaximumSize(QtCore.QSize(130, 16777215))
        self.txt_sampling_points_2.setObjectName("txt_sampling_points_2")
        self.gridLayout_5.addWidget(self.txt_sampling_points_2, 8, 6, 1, 1)
        self.line_10 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_10.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_10.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_10.setObjectName("line_10")
        self.gridLayout_5.addWidget(self.line_10, 7, 2, 1, 5)
        self.select_source_2 = QtWidgets.QComboBox(self.gridFrame_2)
        self.select_source_2.setMaximumSize(QtCore.QSize(130, 16777215))
        self.select_source_2.setObjectName("select_source_2")
        self.select_source_2.addItem("")
        self.select_source_2.addItem("")
        self.gridLayout_5.addWidget(self.select_source_2, 8, 2, 1, 1)
        self.txt_sampling_points_1 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_sampling_points_1.setMaximumSize(QtCore.QSize(130, 16777215))
        self.txt_sampling_points_1.setObjectName("txt_sampling_points_1")
        self.gridLayout_5.addWidget(self.txt_sampling_points_1, 6, 6, 1, 1)
        self.line_32 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_32.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_32.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_32.setObjectName("line_32")
        self.gridLayout_5.addWidget(self.line_32, 11, 2, 1, 5)
        self.line_33 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_33.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_33.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_33.setObjectName("line_33")
        self.gridLayout_5.addWidget(self.line_33, 13, 2, 1, 5)
        self.label_4 = QtWidgets.QLabel(self.gridFrame_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout_5.addWidget(self.label_4, 10, 0, 1, 1)
        self.select_source_1 = QtWidgets.QComboBox(self.gridFrame_2)
        self.select_source_1.setMaximumSize(QtCore.QSize(130, 16777215))
        self.select_source_1.setObjectName("select_source_1")
        self.select_source_1.addItem("")
        self.select_source_1.addItem("")
        self.gridLayout_5.addWidget(self.select_source_1, 6, 2, 1, 1)
        self.txt_sampling_delay_1 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_sampling_delay_1.setMaximumSize(QtCore.QSize(130, 16777215))
        self.txt_sampling_delay_1.setObjectName("txt_sampling_delay_1")
        self.gridLayout_5.addWidget(self.txt_sampling_delay_1, 6, 5, 1, 1)
        self.line_8 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.gridLayout_5.addWidget(self.line_8, 17, 0, 1, 1)
        self.txt_sampling_points_0 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_sampling_points_0.setMaximumSize(QtCore.QSize(130, 16777215))
        self.txt_sampling_points_0.setObjectName("txt_sampling_points_0")
        self.gridLayout_5.addWidget(self.txt_sampling_points_0, 4, 6, 1, 1)
        self.txt_gate_delay_3 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_gate_delay_3.setMaximumSize(QtCore.QSize(130, 16777215))
        self.txt_gate_delay_3.setObjectName("txt_gate_delay_3")
        self.gridLayout_5.addWidget(self.txt_gate_delay_3, 10, 3, 1, 1)
        self.txt_sampling_delay_3 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_sampling_delay_3.setMaximumSize(QtCore.QSize(130, 16777215))
        self.txt_sampling_delay_3.setObjectName("txt_sampling_delay_3")
        self.gridLayout_5.addWidget(self.txt_sampling_delay_3, 10, 5, 1, 1)
        self.txt_gate_delay_2 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_gate_delay_2.setMaximumSize(QtCore.QSize(130, 16777215))
        self.txt_gate_delay_2.setObjectName("txt_gate_delay_2")
        self.gridLayout_5.addWidget(self.txt_gate_delay_2, 8, 3, 1, 1)
        self.label = QtWidgets.QLabel(self.gridFrame_2)
        self.label.setObjectName("label")
        self.gridLayout_5.addWidget(self.label, 4, 0, 1, 1)
        self.label_41 = QtWidgets.QLabel(self.gridFrame_2)
        self.label_41.setObjectName("label_41")
        self.gridLayout_5.addWidget(self.label_41, 16, 0, 1, 1)
        self.txt_sampling_delay_6 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_sampling_delay_6.setMaximumSize(QtCore.QSize(130, 16777215))
        self.txt_sampling_delay_6.setObjectName("txt_sampling_delay_6")
        self.gridLayout_5.addWidget(self.txt_sampling_delay_6, 16, 5, 1, 1)
        self.line_34 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_34.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_34.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_34.setObjectName("line_34")
        self.gridLayout_5.addWidget(self.line_34, 15, 2, 1, 5)
        self.txt_gate_delay_1 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_gate_delay_1.setMaximumSize(QtCore.QSize(130, 16777215))
        self.txt_gate_delay_1.setObjectName("txt_gate_delay_1")
        self.gridLayout_5.addWidget(self.txt_gate_delay_1, 6, 3, 1, 1)
        self.btn_cancel = QtWidgets.QPushButton(self.gridFrame_2)
        self.btn_cancel.setObjectName("btn_cancel")
        self.gridLayout_5.addWidget(self.btn_cancel, 19, 5, 1, 1)
        self.line_4 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridLayout_5.addWidget(self.line_4, 9, 0, 1, 1)
        self.txt_gate_delay_0 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_gate_delay_0.setMaximumSize(QtCore.QSize(130, 16777215))
        self.txt_gate_delay_0.setObjectName("txt_gate_delay_0")
        self.gridLayout_5.addWidget(self.txt_gate_delay_0, 4, 3, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.gridFrame_2)
        self.label_21.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_21.setObjectName("label_21")
        self.gridLayout_5.addWidget(self.label_21, 0, 5, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridFrame_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout_5.addWidget(self.label_3, 8, 0, 1, 1)
        self.label_33 = QtWidgets.QLabel(self.gridFrame_2)
        self.label_33.setObjectName("label_33")
        self.gridLayout_5.addWidget(self.label_33, 12, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.gridFrame_2)
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setObjectName("line")
        self.gridLayout_5.addWidget(self.line, 2, 1, 17, 1)
        self.select_prf_src = QtWidgets.QComboBox(self.gridFrame_2)
        self.select_prf_src.setMaximumSize(QtCore.QSize(130, 16777215))
        self.select_prf_src.setObjectName("select_prf_src")
        self.select_prf_src.addItem("")
        self.select_prf_src.addItem("")
        self.gridLayout_5.addWidget(self.select_prf_src, 0, 2, 1, 1)
        self.txt_sampling_points_5 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_sampling_points_5.setMaximumSize(QtCore.QSize(130, 16777215))
        self.txt_sampling_points_5.setObjectName("txt_sampling_points_5")
        self.gridLayout_5.addWidget(self.txt_sampling_points_5, 14, 6, 1, 1)
        self.line_5 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.gridLayout_5.addWidget(self.line_5, 11, 0, 1, 1)
        self.line_12 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_12.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_12.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_12.setObjectName("line_12")
        self.gridLayout_5.addWidget(self.line_12, 3, 0, 1, 1)
        self.label_19 = QtWidgets.QLabel(self.gridFrame_2)
        self.label_19.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_19.setObjectName("label_19")
        self.gridLayout_5.addWidget(self.label_19, 0, 3, 1, 1)
        self.txt_sampling_delay_7 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_sampling_delay_7.setMaximumSize(QtCore.QSize(130, 16777215))
        self.txt_sampling_delay_7.setObjectName("txt_sampling_delay_7")
        self.gridLayout_5.addWidget(self.txt_sampling_delay_7, 18, 5, 1, 1)
        self.txt_gate_width_7 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_gate_width_7.setMaximumSize(QtCore.QSize(130, 16777215))
        self.txt_gate_width_7.setObjectName("txt_gate_width_7")
        self.gridLayout_5.addWidget(self.txt_gate_width_7, 18, 4, 1, 1)
        self.select_source_6 = QtWidgets.QComboBox(self.gridFrame_2)
        self.select_source_6.setMaximumSize(QtCore.QSize(130, 16777215))
        self.select_source_6.setObjectName("select_source_6")
        self.select_source_6.addItem("")
        self.select_source_6.addItem("")
        self.gridLayout_5.addWidget(self.select_source_6, 16, 2, 1, 1)
        self.txt_prf_cnt = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_prf_cnt.setMaximumSize(QtCore.QSize(130, 16777215))
        self.txt_prf_cnt.setObjectName("txt_prf_cnt")
        self.gridLayout_5.addWidget(self.txt_prf_cnt, 0, 4, 1, 1)
        self.line_13 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_13.setMinimumSize(QtCore.QSize(0, 5))
        self.line_13.setMouseTracking(False)
        self.line_13.setFocusPolicy(QtCore.Qt.NoFocus)
        self.line_13.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_13.setLineWidth(5)
        self.line_13.setMidLineWidth(0)
        self.line_13.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_13.setObjectName("line_13")
        self.gridLayout_5.addWidget(self.line_13, 1, 0, 1, 7)
        self.txt_sampling_points_4 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_sampling_points_4.setMaximumSize(QtCore.QSize(130, 16777215))
        self.txt_sampling_points_4.setObjectName("txt_sampling_points_4")
        self.gridLayout_5.addWidget(self.txt_sampling_points_4, 12, 6, 1, 1)
        self.select_source_5 = QtWidgets.QComboBox(self.gridFrame_2)
        self.select_source_5.setMaximumSize(QtCore.QSize(130, 16777215))
        self.select_source_5.setObjectName("select_source_5")
        self.select_source_5.addItem("")
        self.select_source_5.addItem("")
        self.gridLayout_5.addWidget(self.select_source_5, 14, 2, 1, 1)
        self.label_37 = QtWidgets.QLabel(self.gridFrame_2)
        self.label_37.setObjectName("label_37")
        self.gridLayout_5.addWidget(self.label_37, 14, 0, 1, 1)
        self.line_31 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_31.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_31.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_31.setObjectName("line_31")
        self.gridLayout_5.addWidget(self.line_31, 9, 2, 1, 5)
        self.txt_gate_width_4 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_gate_width_4.setMaximumSize(QtCore.QSize(130, 16777215))
        self.txt_gate_width_4.setObjectName("txt_gate_width_4")
        self.gridLayout_5.addWidget(self.txt_gate_width_4, 12, 4, 1, 1)
        self.txt_gate_delay_7 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_gate_delay_7.setMaximumSize(QtCore.QSize(130, 16777215))
        self.txt_gate_delay_7.setObjectName("txt_gate_delay_7")
        self.gridLayout_5.addWidget(self.txt_gate_delay_7, 18, 3, 1, 1)
        self.select_source_4 = QtWidgets.QComboBox(self.gridFrame_2)
        self.select_source_4.setMaximumSize(QtCore.QSize(130, 16777215))
        self.select_source_4.setObjectName("select_source_4")
        self.select_source_4.addItem("")
        self.select_source_4.addItem("")
        self.gridLayout_5.addWidget(self.select_source_4, 12, 2, 1, 1)
        self.btn_config = QtWidgets.QPushButton(self.gridFrame_2)
        self.btn_config.setObjectName("btn_config")
        self.gridLayout_5.addWidget(self.btn_config, 19, 6, 1, 1)
        self.txt_gate_width_3 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_gate_width_3.setMaximumSize(QtCore.QSize(130, 16777215))
        self.txt_gate_width_3.setObjectName("txt_gate_width_3")
        self.gridLayout_5.addWidget(self.txt_gate_width_3, 10, 4, 1, 1)
        self.select_source_7 = QtWidgets.QComboBox(self.gridFrame_2)
        self.select_source_7.setMaximumSize(QtCore.QSize(130, 16777215))
        self.select_source_7.setObjectName("select_source_7")
        self.select_source_7.addItem("")
        self.select_source_7.addItem("")
        self.gridLayout_5.addWidget(self.select_source_7, 18, 2, 1, 1)
        self.line_6 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.gridLayout_5.addWidget(self.line_6, 13, 0, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout_5.addWidget(self.line_2, 5, 0, 1, 1)
        self.txt_sampling_delay_2 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_sampling_delay_2.setMaximumSize(QtCore.QSize(130, 16777215))
        self.txt_sampling_delay_2.setObjectName("txt_sampling_delay_2")
        self.gridLayout_5.addWidget(self.txt_sampling_delay_2, 8, 5, 1, 1)
        self.select_source_0 = QtWidgets.QComboBox(self.gridFrame_2)
        self.select_source_0.setMaximumSize(QtCore.QSize(130, 16777215))
        self.select_source_0.setObjectName("select_source_0")
        self.select_source_0.addItem("")
        self.select_source_0.addItem("")
        self.gridLayout_5.addWidget(self.select_source_0, 4, 2, 1, 1)
        self.txt_sampling_delay_5 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_sampling_delay_5.setMaximumSize(QtCore.QSize(130, 16777215))
        self.txt_sampling_delay_5.setObjectName("txt_sampling_delay_5")
        self.gridLayout_5.addWidget(self.txt_sampling_delay_5, 14, 5, 1, 1)
        self.txt_sampling_delay_0 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_sampling_delay_0.setMaximumSize(QtCore.QSize(130, 16777215))
        self.txt_sampling_delay_0.setObjectName("txt_sampling_delay_0")
        self.gridLayout_5.addWidget(self.txt_sampling_delay_0, 4, 5, 1, 1)
        self.line_7 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.gridLayout_5.addWidget(self.line_7, 15, 0, 1, 1)
        self.line_9 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_9.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.gridLayout_5.addWidget(self.line_9, 5, 2, 1, 5)
        self.txt_gate_width_6 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_gate_width_6.setMaximumSize(QtCore.QSize(130, 16777215))
        self.txt_gate_width_6.setObjectName("txt_gate_width_6")
        self.gridLayout_5.addWidget(self.txt_gate_width_6, 16, 4, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridFrame_2)
        self.label_2.setObjectName("label_2")
        self.gridLayout_5.addWidget(self.label_2, 6, 0, 1, 1)
        self.line_35 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_35.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_35.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_35.setObjectName("line_35")
        self.gridLayout_5.addWidget(self.line_35, 17, 2, 1, 5)
        self.txt_sampling_points_6 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_sampling_points_6.setMaximumSize(QtCore.QSize(130, 16777215))
        self.txt_sampling_points_6.setObjectName("txt_sampling_points_6")
        self.gridLayout_5.addWidget(self.txt_sampling_points_6, 16, 6, 1, 1)
        self.txt_gate_width_1 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_gate_width_1.setMaximumSize(QtCore.QSize(130, 16777215))
        self.txt_gate_width_1.setObjectName("txt_gate_width_1")
        self.gridLayout_5.addWidget(self.txt_gate_width_1, 6, 4, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.gridFrame_2)
        self.label_17.setAlignment(QtCore.Qt.AlignCenter)
        self.label_17.setObjectName("label_17")
        self.gridLayout_5.addWidget(self.label_17, 2, 5, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.gridFrame_2)
        self.label_20.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_20.setObjectName("label_20")
        self.gridLayout_5.addWidget(self.label_20, 0, 0, 1, 1)
        self.txt_gate_delay_6 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_gate_delay_6.setMaximumSize(QtCore.QSize(130, 16777215))
        self.txt_gate_delay_6.setObjectName("txt_gate_delay_6")
        self.gridLayout_5.addWidget(self.txt_gate_delay_6, 16, 3, 1, 1)
        self.line_11 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_11.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_11.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_11.setObjectName("line_11")
        self.gridLayout_5.addWidget(self.line_11, 3, 2, 1, 5)
        self.txt_sampling_points_3 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_sampling_points_3.setMaximumSize(QtCore.QSize(130, 16777215))
        self.txt_sampling_points_3.setObjectName("txt_sampling_points_3")
        self.gridLayout_5.addWidget(self.txt_sampling_points_3, 10, 6, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.gridFrame_2)
        self.label_14.setMaximumSize(QtCore.QSize(1000, 16777215))
        self.label_14.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.gridLayout_5.addWidget(self.label_14, 2, 2, 1, 1)
        self.txt_sampling_points_7 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_sampling_points_7.setMaximumSize(QtCore.QSize(130, 16777215))
        self.txt_sampling_points_7.setObjectName("txt_sampling_points_7")
        self.gridLayout_5.addWidget(self.txt_sampling_points_7, 18, 6, 1, 1)
        self.txt_gate_delay_4 = QtWidgets.QLineEdit(self.gridFrame_2)
        self.txt_gate_delay_4.setMaximumSize(QtCore.QSize(130, 16777215))
        self.txt_gate_delay_4.setObjectName("txt_gate_delay_4")
        self.gridLayout_5.addWidget(self.txt_gate_delay_4, 12, 3, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout_5, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.gridFrame_2, 0, 0, 1, 2)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.select_source_3.setItemText(0, _translate("Dialog", "DDS产生"))
        self.select_source_3.setItemText(1, _translate("Dialog", "RAM预置"))
        self.label_16.setText(_translate("Dialog", "播放波门宽度(ns)"))
        self.label_15.setText(_translate("Dialog", "播放波门延迟(ns)"))
        self.label_45.setText(_translate("Dialog", "通道8"))
        self.label_18.setText(_translate("Dialog", "采样点数(k)"))
        self.select_source_2.setItemText(0, _translate("Dialog", "DDS产生"))
        self.select_source_2.setItemText(1, _translate("Dialog", "RAM预置"))
        self.label_4.setText(_translate("Dialog", "通道4"))
        self.select_source_1.setItemText(0, _translate("Dialog", "DDS产生"))
        self.select_source_1.setItemText(1, _translate("Dialog", "RAM预置"))
        self.label.setText(_translate("Dialog", "通道1"))
        self.label_41.setText(_translate("Dialog", "通道7"))
        self.btn_cancel.setText(_translate("Dialog", "取消"))
        self.label_21.setText(_translate("Dialog", "基准PRF周期(ns)"))
        self.label_3.setText(_translate("Dialog", "通道3"))
        self.label_33.setText(_translate("Dialog", "通道5"))
        self.select_prf_src.setItemText(0, _translate("Dialog", "内部产生"))
        self.select_prf_src.setItemText(1, _translate("Dialog", "外部输入"))
        self.label_19.setText(_translate("Dialog", "基准PRF数量"))
        self.select_source_6.setItemText(0, _translate("Dialog", "DDS产生"))
        self.select_source_6.setItemText(1, _translate("Dialog", "RAM预置"))
        self.select_source_5.setItemText(0, _translate("Dialog", "DDS产生"))
        self.select_source_5.setItemText(1, _translate("Dialog", "RAM预置"))
        self.label_37.setText(_translate("Dialog", "通道6"))
        self.select_source_4.setItemText(0, _translate("Dialog", "DDS产生"))
        self.select_source_4.setItemText(1, _translate("Dialog", "RAM预置"))
        self.btn_config.setText(_translate("Dialog", "确定"))
        self.select_source_7.setItemText(0, _translate("Dialog", "DDS产生"))
        self.select_source_7.setItemText(1, _translate("Dialog", "RAM预置"))
        self.select_source_0.setItemText(0, _translate("Dialog", "DDS产生"))
        self.select_source_0.setItemText(1, _translate("Dialog", "RAM预置"))
        self.label_2.setText(_translate("Dialog", "通道2"))
        self.label_17.setText(_translate("Dialog", "采样延迟(ns)"))
        self.label_20.setText(_translate("Dialog", "基准PRF选择"))
        self.label_14.setText(_translate("Dialog", "播放数据来源"))