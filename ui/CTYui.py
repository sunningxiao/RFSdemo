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
        Form.resize(1293, 994)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(1200, 992))
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 6, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 1, 1, 1)
        self.select_command = QtWidgets.QComboBox(Form)
        self.select_command.setMinimumSize(QtCore.QSize(0, 0))
        self.select_command.setObjectName("select_command")
        self.gridLayout.addWidget(self.select_command, 3, 3, 1, 1)
        self.btn_framwork_up = QtWidgets.QPushButton(Form)
        self.btn_framwork_up.setMinimumSize(QtCore.QSize(0, 30))
        self.btn_framwork_up.setObjectName("btn_framwork_up")
        self.gridLayout.addWidget(self.btn_framwork_up, 3, 0, 1, 1)
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
        self.btn_connect.setMinimumSize(QtCore.QSize(150, 30))
        self.btn_connect.setMaximumSize(QtCore.QSize(150, 16777215))
        self.btn_connect.setObjectName("btn_connect")
        self.horizontalLayout.addWidget(self.btn_connect)
        self.select_link_addr = QtWidgets.QComboBox(self.frame_2)
        self.select_link_addr.setMinimumSize(QtCore.QSize(160, 0))
        self.select_link_addr.setEditable(True)
        self.select_link_addr.setObjectName("select_link_addr")
        self.horizontalLayout.addWidget(self.select_link_addr)
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
        self.btn_reload_icd = QtWidgets.QPushButton(Form)
        self.btn_reload_icd.setMinimumSize(QtCore.QSize(0, 30))
        self.btn_reload_icd.setObjectName("btn_reload_icd")
        self.gridLayout.addWidget(self.btn_reload_icd, 3, 5, 1, 1)
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
        self.line = QtWidgets.QFrame(self.frame)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_5.addWidget(self.line)
        self.btn_show_spectrum = QtWidgets.QPushButton(self.frame)
        self.btn_show_spectrum.setMinimumSize(QtCore.QSize(100, 30))
        self.btn_show_spectrum.setMaximumSize(QtCore.QSize(100, 16777215))
        self.btn_show_spectrum.setObjectName("btn_show_spectrum")
        self.horizontalLayout_5.addWidget(self.btn_show_spectrum)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_5)
        self.gridLayout_3.addWidget(self.frame, 2, 0, 1, 1)
        self.frame_4 = QtWidgets.QFrame(self.tab_2)
        self.frame_4.setMinimumSize(QtCore.QSize(0, 150))
        self.frame_4.setMaximumSize(QtCore.QSize(16777215, 170))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_3.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label_12 = QtWidgets.QLabel(self.frame_4)
        self.label_12.setMaximumSize(QtCore.QSize(1000, 16777215))
        self.label_12.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName("label_12")
        self.gridLayout_7.addWidget(self.label_12, 2, 7, 1, 1)
        self.label_24 = QtWidgets.QLabel(self.frame_4)
        self.label_24.setMinimumSize(QtCore.QSize(0, 0))
        self.label_24.setMaximumSize(QtCore.QSize(1000, 16777215))
        self.label_24.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_24.setObjectName("label_24")
        self.gridLayout_7.addWidget(self.label_24, 1, 7, 1, 1)
        self.label_23 = QtWidgets.QLabel(self.frame_4)
        self.label_23.setMinimumSize(QtCore.QSize(0, 0))
        self.label_23.setMaximumSize(QtCore.QSize(1000, 16777215))
        self.label_23.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_23.setObjectName("label_23")
        self.gridLayout_7.addWidget(self.label_23, 1, 3, 1, 1)
        self.txt_dac_noc_f = QtWidgets.QLineEdit(self.frame_4)
        self.txt_dac_noc_f.setMaximumSize(QtCore.QSize(130, 16777215))
        self.txt_dac_noc_f.setObjectName("txt_dac_noc_f")
        self.gridLayout_7.addWidget(self.txt_dac_noc_f, 2, 6, 1, 1)
        self.txt_dac_nyq = QtWidgets.QLineEdit(self.frame_4)
        self.txt_dac_nyq.setMaximumSize(QtCore.QSize(130, 16777215))
        self.txt_dac_nyq.setObjectName("txt_dac_nyq")
        self.gridLayout_7.addWidget(self.txt_dac_nyq, 2, 8, 1, 1)
        self.txt_adc_nyq = QtWidgets.QLineEdit(self.frame_4)
        self.txt_adc_nyq.setMinimumSize(QtCore.QSize(80, 0))
        self.txt_adc_nyq.setMaximumSize(QtCore.QSize(130, 16777215))
        self.txt_adc_nyq.setObjectName("txt_adc_nyq")
        self.gridLayout_7.addWidget(self.txt_adc_nyq, 1, 8, 1, 1)
        self.select_dac_sample = QtWidgets.QComboBox(self.frame_4)
        self.select_dac_sample.setMinimumSize(QtCore.QSize(100, 0))
        self.select_dac_sample.setMaximumSize(QtCore.QSize(130, 16777215))
        self.select_dac_sample.setObjectName("select_dac_sample")
        self.select_dac_sample.addItem("")
        self.select_dac_sample.addItem("")
        self.select_dac_sample.addItem("")
        self.select_dac_sample.addItem("")
        self.gridLayout_7.addWidget(self.select_dac_sample, 2, 4, 1, 1)
        self.label_25 = QtWidgets.QLabel(self.frame_4)
        self.label_25.setMinimumSize(QtCore.QSize(0, 0))
        self.label_25.setMaximumSize(QtCore.QSize(1000, 16777215))
        self.label_25.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_25.setObjectName("label_25")
        self.gridLayout_7.addWidget(self.label_25, 1, 5, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.txt_pll_f = QtWidgets.QLineEdit(self.frame_4)
        self.txt_pll_f.setMaximumSize(QtCore.QSize(130, 16777215))
        self.txt_pll_f.setText("")
        self.txt_pll_f.setObjectName("txt_pll_f")
        self.gridLayout_2.addWidget(self.txt_pll_f, 1, 3, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.frame_4)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 1, 2, 1, 1)
        self.line_3 = QtWidgets.QFrame(self.frame_4)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout_2.addWidget(self.line_3, 1, 0, 3, 1)
        self.line_4 = QtWidgets.QFrame(self.frame_4)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridLayout_2.addWidget(self.line_4, 0, 2, 1, 2)
        self.chk_pll_adc = QtWidgets.QCheckBox(self.frame_4)
        self.chk_pll_adc.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.chk_pll_adc.setText("")
        self.chk_pll_adc.setIconSize(QtCore.QSize(20, 20))
        self.chk_pll_adc.setObjectName("chk_pll_adc")
        self.gridLayout_2.addWidget(self.chk_pll_adc, 2, 3, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.frame_4)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 2, 2, 1, 1)
        self.chk_pll_dac = QtWidgets.QCheckBox(self.frame_4)
        self.chk_pll_dac.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.chk_pll_dac.setText("")
        self.chk_pll_dac.setObjectName("chk_pll_dac")
        self.gridLayout_2.addWidget(self.chk_pll_dac, 3, 3, 1, 1)
        self.line_5 = QtWidgets.QFrame(self.frame_4)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.gridLayout_2.addWidget(self.line_5, 4, 2, 1, 2)
        self.label_7 = QtWidgets.QLabel(self.frame_4)
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 3, 2, 1, 1)
        self.gridLayout_7.addLayout(self.gridLayout_2, 1, 10, 2, 2)
        self.txt_adc_noc_f = QtWidgets.QLineEdit(self.frame_4)
        self.txt_adc_noc_f.setMinimumSize(QtCore.QSize(80, 0))
        self.txt_adc_noc_f.setMaximumSize(QtCore.QSize(130, 16777215))
        self.txt_adc_noc_f.setObjectName("txt_adc_noc_f")
        self.gridLayout_7.addWidget(self.txt_adc_noc_f, 1, 6, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.frame_4)
        self.label_11.setMaximumSize(QtCore.QSize(1000, 16777215))
        self.label_11.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName("label_11")
        self.gridLayout_7.addWidget(self.label_11, 2, 5, 1, 1)
        self.select_adc_sample = QtWidgets.QComboBox(self.frame_4)
        self.select_adc_sample.setMinimumSize(QtCore.QSize(100, 0))
        self.select_adc_sample.setMaximumSize(QtCore.QSize(130, 16777215))
        self.select_adc_sample.setObjectName("select_adc_sample")
        self.select_adc_sample.addItem("")
        self.select_adc_sample.addItem("")
        self.select_adc_sample.addItem("")
        self.gridLayout_7.addWidget(self.select_adc_sample, 1, 4, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.frame_4)
        self.label_13.setMaximumSize(QtCore.QSize(1000, 16777215))
        self.label_13.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName("label_13")
        self.gridLayout_7.addWidget(self.label_13, 2, 3, 1, 1)
        self.lab_clock_2 = QtWidgets.QLabel(self.frame_4)
        self.lab_clock_2.setMinimumSize(QtCore.QSize(0, 0))
        self.lab_clock_2.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lab_clock_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lab_clock_2.setObjectName("lab_clock_2")
        self.gridLayout_7.addWidget(self.lab_clock_2, 1, 0, 1, 1)
        self.select_clock = QtWidgets.QComboBox(self.frame_4)
        self.select_clock.setMinimumSize(QtCore.QSize(180, 0))
        self.select_clock.setMaximumSize(QtCore.QSize(200, 16777215))
        self.select_clock.setObjectName("select_clock")
        self.select_clock.addItem("")
        self.select_clock.addItem("")
        self.select_clock.addItem("")
        self.select_clock.addItem("")
        self.gridLayout_7.addWidget(self.select_clock, 1, 1, 1, 2)
        self.btn_rf_cfg = QtWidgets.QPushButton(self.frame_4)
        self.btn_rf_cfg.setMinimumSize(QtCore.QSize(0, 30))
        self.btn_rf_cfg.setMaximumSize(QtCore.QSize(100, 16777215))
        self.btn_rf_cfg.setObjectName("btn_rf_cfg")
        self.gridLayout_7.addWidget(self.btn_rf_cfg, 2, 0, 1, 2)
        self.verticalLayout_3.addLayout(self.gridLayout_7)
        self.line_2 = QtWidgets.QFrame(self.frame_4)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_3.addWidget(self.line_2)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setSpacing(7)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.btn_wave = QtWidgets.QPushButton(self.frame_4)
        self.btn_wave.setMinimumSize(QtCore.QSize(0, 30))
        self.btn_wave.setMaximumSize(QtCore.QSize(100, 16777215))
        self.btn_wave.setObjectName("btn_wave")
        self.gridLayout_5.addWidget(self.btn_wave, 0, 9, 1, 1)
        self.btn_qmc_cfg = QtWidgets.QPushButton(self.frame_4)
        self.btn_qmc_cfg.setMinimumSize(QtCore.QSize(0, 30))
        self.btn_qmc_cfg.setMaximumSize(QtCore.QSize(100, 16777215))
        self.btn_qmc_cfg.setObjectName("btn_qmc_cfg")
        self.gridLayout_5.addWidget(self.btn_qmc_cfg, 0, 5, 1, 1)
        self.btn_dss_cfg = QtWidgets.QPushButton(self.frame_4)
        self.btn_dss_cfg.setMinimumSize(QtCore.QSize(0, 30))
        self.btn_dss_cfg.setMaximumSize(QtCore.QSize(100, 16777215))
        self.btn_dss_cfg.setObjectName("btn_dss_cfg")
        self.gridLayout_5.addWidget(self.btn_dss_cfg, 0, 6, 1, 1)
        self.chk_write_file = QtWidgets.QCheckBox(self.frame_4)
        self.chk_write_file.setChecked(True)
        self.chk_write_file.setObjectName("chk_write_file")
        self.gridLayout_5.addWidget(self.chk_write_file, 0, 2, 1, 1)
        self.btn_stop = QtWidgets.QPushButton(self.frame_4)
        self.btn_stop.setMinimumSize(QtCore.QSize(0, 30))
        self.btn_stop.setMaximumSize(QtCore.QSize(100, 16777215))
        self.btn_stop.setObjectName("btn_stop")
        self.gridLayout_5.addWidget(self.btn_stop, 0, 1, 1, 1)
        self.btn_start = QtWidgets.QPushButton(self.frame_4)
        self.btn_start.setMinimumSize(QtCore.QSize(0, 30))
        self.btn_start.setMaximumSize(QtCore.QSize(100, 16777215))
        self.btn_start.setObjectName("btn_start")
        self.gridLayout_5.addWidget(self.btn_start, 0, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem2, 0, 3, 1, 1)
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
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setMaximumSize(QtCore.QSize(16777215, 180))
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 2, 0, 1, 7)
        self.btn_auto_command = QtWidgets.QPushButton(Form)
        self.btn_auto_command.setMinimumSize(QtCore.QSize(0, 30))
        self.btn_auto_command.setObjectName("btn_auto_command")
        self.gridLayout.addWidget(self.btn_auto_command, 3, 2, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 3, 4, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Control"))
        self.label_4.setText(_translate("Form", "V2.4.3"))
        self.btn_framwork_up.setText(_translate("Form", "固件更新"))
        self.btn_connect.setText(_translate("Form", "系统连接"))
        self.label_2.setText(_translate("Form", "状态："))
        self.label_status.setText(_translate("Form", "系统未连接"))
        self.btn_reload_icd.setText(_translate("Form", "重载ICD"))
        self.chk1.setText(_translate("Form", "通道1"))
        self.chk2.setText(_translate("Form", "通道2"))
        self.chk3.setText(_translate("Form", "通道3"))
        self.chk4.setText(_translate("Form", "通道4"))
        self.chk5.setText(_translate("Form", "通道5"))
        self.chk6.setText(_translate("Form", "通道6"))
        self.chk7.setText(_translate("Form", "通道7"))
        self.chk8.setText(_translate("Form", "通道8"))
        self.btn_show_spectrum.setText(_translate("Form", "显示频谱"))
        self.label_12.setText(_translate("Form", "DAC奈奎斯特区"))
        self.label_24.setText(_translate("Form", "ADC奈奎斯特区"))
        self.label_23.setText(_translate("Form", "ADC采样率(MHz)"))
        self.txt_dac_noc_f.setText(_translate("Form", "100"))
        self.txt_dac_nyq.setText(_translate("Form", "1"))
        self.txt_adc_nyq.setText(_translate("Form", "1"))
        self.select_dac_sample.setItemText(0, _translate("Form", "1000"))
        self.select_dac_sample.setItemText(1, _translate("Form", "2000"))
        self.select_dac_sample.setItemText(2, _translate("Form", "4000"))
        self.select_dac_sample.setItemText(3, _translate("Form", "6000"))
        self.label_25.setText(_translate("Form", "ADC NCO频率(MHz)"))
        self.label_6.setText(_translate("Form", "PLL参考频率(MHz)"))
        self.label_5.setText(_translate("Form", "ADC PLL使能"))
        self.label_7.setText(_translate("Form", "DAC PLL使能"))
        self.txt_adc_noc_f.setText(_translate("Form", "100"))
        self.label_11.setText(_translate("Form", "DAC NCO频率(MHz)"))
        self.select_adc_sample.setItemText(0, _translate("Form", "1000"))
        self.select_adc_sample.setItemText(1, _translate("Form", "2000"))
        self.select_adc_sample.setItemText(2, _translate("Form", "4000"))
        self.label_13.setText(_translate("Form", "DAC采样率(MHz)"))
        self.lab_clock_2.setText(_translate("Form", "参考时钟"))
        self.select_clock.setItemText(0, _translate("Form", "内参考"))
        self.select_clock.setItemText(1, _translate("Form", "外参考"))
        self.select_clock.setItemText(2, _translate("Form", "外输入"))
        self.select_clock.setItemText(3, _translate("Form", "RFSOC外输入参考"))
        self.btn_rf_cfg.setText(_translate("Form", "RF配置"))
        self.btn_wave.setText(_translate("Form", "波形装载"))
        self.btn_qmc_cfg.setText(_translate("Form", "QMC配置"))
        self.btn_dss_cfg.setText(_translate("Form", "DDS设置"))
        self.chk_write_file.setText(_translate("Form", "落盘"))
        self.btn_stop.setText(_translate("Form", "系统停止"))
        self.btn_start.setText(_translate("Form", "系统开启"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "系统控制"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "通用控制"))
        self.btn_auto_command.setText(_translate("Form", "自定义指令"))
