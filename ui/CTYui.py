# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CTYui.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowModality(QtCore.Qt.NonModal)
        Form.resize(1073, 969)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(800, 900))
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.select_command = QtWidgets.QComboBox(Form)
        self.select_command.setObjectName("select_command")
        self.gridLayout.addWidget(self.select_command, 3, 4, 1, 1)
        self.btn_framwork_up = QtWidgets.QPushButton(Form)
        self.btn_framwork_up.setObjectName("btn_framwork_up")
        self.gridLayout.addWidget(self.btn_framwork_up, 3, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 2, 1, 1)
        self.frame_2 = QtWidgets.QFrame(Form)
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 70))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_connect = QtWidgets.QPushButton(self.frame_2)
        self.btn_connect.setMinimumSize(QtCore.QSize(150, 0))
        self.btn_connect.setMaximumSize(QtCore.QSize(150, 16777215))
        self.btn_connect.setObjectName("btn_connect")
        self.horizontalLayout.addWidget(self.btn_connect)
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setMinimumSize(QtCore.QSize(100, 0))
        self.label_2.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.label_status = QtWidgets.QLabel(self.frame_2)
        self.label_status.setObjectName("label_status")
        self.horizontalLayout.addWidget(self.label_status)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setText("")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.label_3 = QtWidgets.QLabel(self.frame_2)
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.lab_logo = QtWidgets.QLabel(self.frame_2)
        self.lab_logo.setMinimumSize(QtCore.QSize(60, 50))
        self.lab_logo.setMaximumSize(QtCore.QSize(60, 50))
        self.lab_logo.setText("")
        self.lab_logo.setObjectName("lab_logo")
        self.horizontalLayout_2.addWidget(self.lab_logo)
        self.gridLayout.addWidget(self.frame_2, 0, 0, 1, 7)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 6, 1, 1)
        self.btn_auto_command = QtWidgets.QPushButton(Form)
        self.btn_auto_command.setObjectName("btn_auto_command")
        self.gridLayout.addWidget(self.btn_auto_command, 3, 3, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 3, 5, 1, 1)
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 3, 1, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setMaximumSize(QtCore.QSize(16777215, 150))
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 2, 0, 1, 7)
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setIconSize(QtCore.QSize(16, 16))
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.frame_5 = QtWidgets.QFrame(self.tab_2)
        self.frame_5.setMinimumSize(QtCore.QSize(0, 300))
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.grid_graph = QtWidgets.QGridLayout()
        self.grid_graph.setContentsMargins(10, 10, 10, 10)
        self.grid_graph.setObjectName("grid_graph")
        self.horizontalLayout_8.addLayout(self.grid_graph)
        self.gridLayout_3.addWidget(self.frame_5, 1, 0, 1, 1)
        self.frame = QtWidgets.QFrame(self.tab_2)
        self.frame.setMinimumSize(QtCore.QSize(0, 7))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.chk1 = QtWidgets.QCheckBox(self.frame)
        self.chk1.setChecked(True)
        self.chk1.setObjectName("chk1")
        self.horizontalLayout_5.addWidget(self.chk1)
        self.chk2 = QtWidgets.QCheckBox(self.frame)
        self.chk2.setObjectName("chk2")
        self.horizontalLayout_5.addWidget(self.chk2)
        self.chk3 = QtWidgets.QCheckBox(self.frame)
        self.chk3.setObjectName("chk3")
        self.horizontalLayout_5.addWidget(self.chk3)
        self.chk4 = QtWidgets.QCheckBox(self.frame)
        self.chk4.setObjectName("chk4")
        self.horizontalLayout_5.addWidget(self.chk4)
        self.chk5 = QtWidgets.QCheckBox(self.frame)
        self.chk5.setObjectName("chk5")
        self.horizontalLayout_5.addWidget(self.chk5)
        self.chk6 = QtWidgets.QCheckBox(self.frame)
        self.chk6.setObjectName("chk6")
        self.horizontalLayout_5.addWidget(self.chk6)
        self.chk7 = QtWidgets.QCheckBox(self.frame)
        self.chk7.setObjectName("chk7")
        self.horizontalLayout_5.addWidget(self.chk7)
        self.chk8 = QtWidgets.QCheckBox(self.frame)
        self.chk8.setObjectName("chk8")
        self.horizontalLayout_5.addWidget(self.chk8)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_5)
        self.gridLayout_3.addWidget(self.frame, 2, 0, 1, 1)
        self.frame_4 = QtWidgets.QFrame(self.tab_2)
        self.frame_4.setMinimumSize(QtCore.QSize(0, 120))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_3.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setSpacing(7)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_20 = QtWidgets.QLabel(self.frame_4)
        self.label_20.setMinimumSize(QtCore.QSize(0, 0))
        self.label_20.setMaximumSize(QtCore.QSize(1000, 16777215))
        self.label_20.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_20.setObjectName("label_20")
        self.gridLayout_5.addWidget(self.label_20, 0, 3, 1, 1)
        self.txt_gate_delay = QtWidgets.QLineEdit(self.frame_4)
        self.txt_gate_delay.setMaximumSize(QtCore.QSize(100, 16777215))
        self.txt_gate_delay.setObjectName("txt_gate_delay")
        self.gridLayout_5.addWidget(self.txt_gate_delay, 4, 4, 1, 1)
        self.txt_sampling_points = QtWidgets.QLineEdit(self.frame_4)
        self.txt_sampling_points.setMaximumSize(QtCore.QSize(100, 16777215))
        self.txt_sampling_points.setObjectName("txt_sampling_points")
        self.gridLayout_5.addWidget(self.txt_sampling_points, 5, 6, 1, 1)
        self.txt_adc_nyq = QtWidgets.QLineEdit(self.frame_4)
        self.txt_adc_nyq.setMinimumSize(QtCore.QSize(80, 0))
        self.txt_adc_nyq.setMaximumSize(QtCore.QSize(100, 16777215))
        self.txt_adc_nyq.setObjectName("txt_adc_nyq")
        self.gridLayout_5.addWidget(self.txt_adc_nyq, 0, 8, 1, 1)
        self.dds_chose = QtWidgets.QComboBox(self.frame_4)
        self.dds_chose.setMaximumSize(QtCore.QSize(100, 16777215))
        self.dds_chose.setObjectName("dds_chose")
        self.dds_chose.addItem("")
        self.dds_chose.addItem("")
        self.dds_chose.addItem("")
        self.dds_chose.addItem("")
        self.dds_chose.addItem("")
        self.dds_chose.addItem("")
        self.dds_chose.addItem("")
        self.dds_chose.addItem("")
        self.gridLayout_5.addWidget(self.dds_chose, 3, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.frame_4)
        self.label_9.setMaximumSize(QtCore.QSize(1000, 16777215))
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout_5.addWidget(self.label_9, 1, 5, 1, 1)
        self.lab_clock = QtWidgets.QLabel(self.frame_4)
        self.lab_clock.setMinimumSize(QtCore.QSize(0, 0))
        self.lab_clock.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lab_clock.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lab_clock.setObjectName("lab_clock")
        self.gridLayout_5.addWidget(self.lab_clock, 0, 1, 1, 1)
        self.txt_gate_width = QtWidgets.QLineEdit(self.frame_4)
        self.txt_gate_width.setMaximumSize(QtCore.QSize(100, 16777215))
        self.txt_gate_width.setObjectName("txt_gate_width")
        self.gridLayout_5.addWidget(self.txt_gate_width, 4, 6, 1, 1)
        self.txt_adc_noc_f = QtWidgets.QLineEdit(self.frame_4)
        self.txt_adc_noc_f.setMinimumSize(QtCore.QSize(80, 0))
        self.txt_adc_noc_f.setMaximumSize(QtCore.QSize(100, 16777215))
        self.txt_adc_noc_f.setObjectName("txt_adc_noc_f")
        self.gridLayout_5.addWidget(self.txt_adc_noc_f, 0, 6, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.frame_4)
        self.label_11.setMaximumSize(QtCore.QSize(1000, 16777215))
        self.label_11.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName("label_11")
        self.gridLayout_5.addWidget(self.label_11, 4, 1, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.frame_4)
        self.label_15.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_15.setObjectName("label_15")
        self.gridLayout_5.addWidget(self.label_15, 5, 5, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.frame_4)
        self.label_14.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_14.setObjectName("label_14")
        self.gridLayout_5.addWidget(self.label_14, 5, 3, 1, 1)
        self.btn_wave = QtWidgets.QPushButton(self.frame_4)
        self.btn_wave.setMinimumSize(QtCore.QSize(100, 0))
        self.btn_wave.setMaximumSize(QtCore.QSize(100, 16777215))
        self.btn_wave.setObjectName("btn_wave")
        self.gridLayout_5.addWidget(self.btn_wave, 4, 8, 1, 1)
        self.txt_prf_cnt = QtWidgets.QLineEdit(self.frame_4)
        self.txt_prf_cnt.setMaximumSize(QtCore.QSize(100, 16777215))
        self.txt_prf_cnt.setObjectName("txt_prf_cnt")
        self.gridLayout_5.addWidget(self.txt_prf_cnt, 2, 2, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.frame_4)
        self.label_16.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_16.setObjectName("label_16")
        self.gridLayout_5.addWidget(self.label_16, 1, 1, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.frame_4)
        self.label_17.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_17.setObjectName("label_17")
        self.gridLayout_5.addWidget(self.label_17, 2, 1, 1, 1)
        self.select_adc_sample = QtWidgets.QComboBox(self.frame_4)
        self.select_adc_sample.setMaximumSize(QtCore.QSize(100, 16777215))
        self.select_adc_sample.setObjectName("select_adc_sample")
        self.select_adc_sample.addItem("")
        self.select_adc_sample.addItem("")
        self.select_adc_sample.addItem("")
        self.gridLayout_5.addWidget(self.select_adc_sample, 0, 4, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.frame_4)
        self.label_6.setTextFormat(QtCore.Qt.AutoText)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout_5.addWidget(self.label_6, 3, 3, 1, 1)
        self.txt_sampling_delay = QtWidgets.QLineEdit(self.frame_4)
        self.txt_sampling_delay.setMaximumSize(QtCore.QSize(100, 16777215))
        self.txt_sampling_delay.setObjectName("txt_sampling_delay")
        self.gridLayout_5.addWidget(self.txt_sampling_delay, 5, 4, 1, 1)
        self.label_22 = QtWidgets.QLabel(self.frame_4)
        self.label_22.setMinimumSize(QtCore.QSize(0, 0))
        self.label_22.setMaximumSize(QtCore.QSize(1000, 16777215))
        self.label_22.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_22.setObjectName("label_22")
        self.gridLayout_5.addWidget(self.label_22, 0, 7, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.frame_4)
        self.label_12.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName("label_12")
        self.gridLayout_5.addWidget(self.label_12, 4, 3, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.frame_4)
        self.label_21.setMinimumSize(QtCore.QSize(0, 0))
        self.label_21.setMaximumSize(QtCore.QSize(1000, 16777215))
        self.label_21.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_21.setObjectName("label_21")
        self.gridLayout_5.addWidget(self.label_21, 0, 5, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.frame_4)
        self.label_13.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName("label_13")
        self.gridLayout_5.addWidget(self.label_13, 4, 5, 1, 1)
        self.select_source = QtWidgets.QComboBox(self.frame_4)
        self.select_source.setObjectName("select_source")
        self.select_source.addItem("")
        self.select_source.addItem("")
        self.gridLayout_5.addWidget(self.select_source, 4, 2, 1, 1)
        self.label_23 = QtWidgets.QLabel(self.frame_4)
        self.label_23.setMinimumSize(QtCore.QSize(0, 0))
        self.label_23.setMaximumSize(QtCore.QSize(10000, 16777215))
        self.label_23.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_23.setObjectName("label_23")
        self.gridLayout_5.addWidget(self.label_23, 3, 1, 1, 1)
        self.txt_dds_pulse = QtWidgets.QLineEdit(self.frame_4)
        self.txt_dds_pulse.setMaximumSize(QtCore.QSize(100, 16777215))
        self.txt_dds_pulse.setObjectName("txt_dds_pulse")
        self.gridLayout_5.addWidget(self.txt_dds_pulse, 3, 6, 1, 1)
        self.txt_dds_fc = QtWidgets.QLineEdit(self.frame_4)
        self.txt_dds_fc.setMaximumSize(QtCore.QSize(100, 16777215))
        self.txt_dds_fc.setObjectName("txt_dds_fc")
        self.gridLayout_5.addWidget(self.txt_dds_fc, 3, 2, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.frame_4)
        self.label_8.setMaximumSize(QtCore.QSize(1000, 16777215))
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout_5.addWidget(self.label_8, 1, 3, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.frame_4)
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout_5.addWidget(self.label_7, 3, 5, 1, 1)
        self.txt_dac_nyq = QtWidgets.QLineEdit(self.frame_4)
        self.txt_dac_nyq.setMaximumSize(QtCore.QSize(100, 16777215))
        self.txt_dac_nyq.setObjectName("txt_dac_nyq")
        self.gridLayout_5.addWidget(self.txt_dac_nyq, 1, 8, 1, 1)
        self.txt_dds_band = QtWidgets.QLineEdit(self.frame_4)
        self.txt_dds_band.setMaximumSize(QtCore.QSize(100, 16777215))
        self.txt_dds_band.setObjectName("txt_dds_band")
        self.gridLayout_5.addWidget(self.txt_dds_band, 3, 4, 1, 1)
        self.select_dac_sample = QtWidgets.QComboBox(self.frame_4)
        self.select_dac_sample.setMaximumSize(QtCore.QSize(100, 16777215))
        self.select_dac_sample.setObjectName("select_dac_sample")
        self.select_dac_sample.addItem("")
        self.select_dac_sample.addItem("")
        self.select_dac_sample.addItem("")
        self.gridLayout_5.addWidget(self.select_dac_sample, 1, 4, 1, 1)
        self.txt_dac_noc_f = QtWidgets.QLineEdit(self.frame_4)
        self.txt_dac_noc_f.setMaximumSize(QtCore.QSize(100, 16777215))
        self.txt_dac_noc_f.setObjectName("txt_dac_noc_f")
        self.gridLayout_5.addWidget(self.txt_dac_noc_f, 1, 6, 1, 1)
        self.txt_prf_cyc = QtWidgets.QLineEdit(self.frame_4)
        self.txt_prf_cyc.setMaximumSize(QtCore.QSize(100, 16777215))
        self.txt_prf_cyc.setObjectName("txt_prf_cyc")
        self.gridLayout_5.addWidget(self.txt_prf_cyc, 1, 2, 1, 1)
        self.select_clock = QtWidgets.QComboBox(self.frame_4)
        self.select_clock.setMaximumSize(QtCore.QSize(100, 16777215))
        self.select_clock.setObjectName("select_clock")
        self.select_clock.addItem("")
        self.select_clock.addItem("")
        self.gridLayout_5.addWidget(self.select_clock, 0, 2, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.frame_4)
        self.label_10.setMaximumSize(QtCore.QSize(1000, 16777215))
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.gridLayout_5.addWidget(self.label_10, 1, 7, 1, 1)
        self.btn_rf_cfg = QtWidgets.QPushButton(self.frame_4)
        self.btn_rf_cfg.setMaximumSize(QtCore.QSize(100, 16777215))
        self.btn_rf_cfg.setObjectName("btn_rf_cfg")
        self.gridLayout_5.addWidget(self.btn_rf_cfg, 0, 0, 1, 1)
        self.btn_dss_cfg = QtWidgets.QPushButton(self.frame_4)
        self.btn_dss_cfg.setMaximumSize(QtCore.QSize(100, 16777215))
        self.btn_dss_cfg.setObjectName("btn_dss_cfg")
        self.gridLayout_5.addWidget(self.btn_dss_cfg, 3, 8, 1, 1)
        self.btn_start = QtWidgets.QPushButton(self.frame_4)
        self.btn_start.setMaximumSize(QtCore.QSize(100, 16777215))
        self.btn_start.setObjectName("btn_start")
        self.gridLayout_5.addWidget(self.btn_start, 1, 0, 1, 1)
        self.btn_stop = QtWidgets.QPushButton(self.frame_4)
        self.btn_stop.setMinimumSize(QtCore.QSize(0, 0))
        self.btn_stop.setMaximumSize(QtCore.QSize(100, 16777215))
        self.btn_stop.setObjectName("btn_stop")
        self.gridLayout_5.addWidget(self.btn_stop, 2, 0, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_5)
        self.gridLayout_3.addWidget(self.frame_4, 0, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setEnabled(False)
        self.tab.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tab.setObjectName("tab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidget.addTab(self.tab, "")
        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 7)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Control"))
        self.btn_framwork_up.setText(_translate("Form", "固件更新"))
        self.btn_connect.setText(_translate("Form", "系统连接"))
        self.label_2.setText(_translate("Form", "状态："))
        self.label_status.setText(_translate("Form", "系统未连接"))
        self.label_4.setText(_translate("Form", "V1.0"))
        self.btn_auto_command.setText(_translate("Form", "自定义指令"))
        self.label_5.setText(_translate("Form", "文件名"))
        self.chk1.setText(_translate("Form", "通道1"))
        self.chk2.setText(_translate("Form", "通道2"))
        self.chk3.setText(_translate("Form", "通道3"))
        self.chk4.setText(_translate("Form", "通道4"))
        self.chk5.setText(_translate("Form", "通道5"))
        self.chk6.setText(_translate("Form", "通道6"))
        self.chk7.setText(_translate("Form", "通道7"))
        self.chk8.setText(_translate("Form", "通道8"))
        self.label_20.setText(_translate("Form", "ADC采样率(MHz)"))
        self.txt_adc_nyq.setText(_translate("Form", "1"))
        self.dds_chose.setItemText(0, _translate("Form", "通道1"))
        self.dds_chose.setItemText(1, _translate("Form", "通道2"))
        self.dds_chose.setItemText(2, _translate("Form", "通道3"))
        self.dds_chose.setItemText(3, _translate("Form", "通道4"))
        self.dds_chose.setItemText(4, _translate("Form", "通道5"))
        self.dds_chose.setItemText(5, _translate("Form", "通道6"))
        self.dds_chose.setItemText(6, _translate("Form", "通道7"))
        self.dds_chose.setItemText(7, _translate("Form", "通道8"))
        self.label_9.setText(_translate("Form", "DAC NCO频率"))
        self.lab_clock.setText(_translate("Form", "参考时钟"))
        self.txt_adc_noc_f.setText(_translate("Form", "100"))
        self.label_11.setText(_translate("Form", "播放数据来源"))
        self.label_15.setText(_translate("Form", "采样点数"))
        self.label_14.setText(_translate("Form", "采样延迟"))
        self.btn_wave.setText(_translate("Form", "波形装载"))
        self.label_16.setText(_translate("Form", "基准PRF周期"))
        self.label_17.setText(_translate("Form", "基准PRF数量"))
        self.select_adc_sample.setItemText(0, _translate("Form", "1000"))
        self.select_adc_sample.setItemText(1, _translate("Form", "2000"))
        self.select_adc_sample.setItemText(2, _translate("Form", "4000"))
        self.label_6.setText(_translate("Form", "带宽"))
        self.label_22.setText(_translate("Form", "ADC奈奎斯特区"))
        self.label_12.setText(_translate("Form", "播放波门延迟"))
        self.label_21.setText(_translate("Form", "ADC NOC频率"))
        self.label_13.setText(_translate("Form", "播放波门宽度"))
        self.select_source.setItemText(0, _translate("Form", "DDS产生"))
        self.select_source.setItemText(1, _translate("Form", "RAM预置"))
        self.label_23.setText(_translate("Form", "中心频率"))
        self.label_8.setText(_translate("Form", "DAC采样率(MHz)"))
        self.label_7.setText(_translate("Form", "脉宽"))
        self.txt_dac_nyq.setText(_translate("Form", "1"))
        self.select_dac_sample.setItemText(0, _translate("Form", "1000"))
        self.select_dac_sample.setItemText(1, _translate("Form", "2000"))
        self.select_dac_sample.setItemText(2, _translate("Form", "4000"))
        self.txt_dac_noc_f.setText(_translate("Form", "100"))
        self.select_clock.setItemText(0, _translate("Form", "内参考"))
        self.select_clock.setItemText(1, _translate("Form", "外参考"))
        self.label_10.setText(_translate("Form", "DAC奈奎斯特区"))
        self.btn_rf_cfg.setText(_translate("Form", "RF配置"))
        self.btn_dss_cfg.setText(_translate("Form", "DSS设置"))
        self.btn_start.setText(_translate("Form", "系统开启"))
        self.btn_stop.setText(_translate("Form", "系统停止"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "系统控制"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "通用控制"))
