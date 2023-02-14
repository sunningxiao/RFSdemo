# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'core_pack_test.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CorePackTest(object):
    bar_process_value = 0

    def setupUi(self, CorePackTest):
        CorePackTest.setObjectName("CorePackTest")
        CorePackTest.resize(960, 850)
        self.gridLayout_2 = QtWidgets.QGridLayout(CorePackTest)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.list_test_history = QtWidgets.QListWidget(CorePackTest)
        self.list_test_history.setMaximumSize(QtCore.QSize(150, 16777215))
        self.list_test_history.setObjectName("list_test_history")
        self.gridLayout_4.addWidget(self.list_test_history, 1, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(CorePackTest)
        self.label_3.setObjectName("label_3")
        self.gridLayout_4.addWidget(self.label_3, 0, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(CorePackTest)
        self.label_9.setObjectName("label_9")
        self.gridLayout_4.addWidget(self.label_9, 0, 1, 1, 1)
        self.btn_output = QtWidgets.QPushButton(CorePackTest)
        self.btn_output.setObjectName("btn_output")
        self.gridLayout_4.addWidget(self.btn_output, 2, 2, 1, 1)
        self.label_10 = QtWidgets.QLabel(CorePackTest)
        self.label_10.setObjectName("label_10")
        self.gridLayout_4.addWidget(self.label_10, 0, 2, 1, 1)
        self.text_serial_print = QtWidgets.QTextBrowser(CorePackTest)
        self.text_serial_print.setMinimumSize(QtCore.QSize(0, 0))
        self.text_serial_print.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.text_serial_print.setObjectName("text_serial_print")
        self.gridLayout_4.addWidget(self.text_serial_print, 1, 0, 2, 1)
        self.text_log_print = QtWidgets.QTextBrowser(CorePackTest)
        self.text_log_print.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.text_log_print.setObjectName("text_log_print")
        self.gridLayout_4.addWidget(self.text_log_print, 1, 1, 2, 1)
        self.gridLayout_2.addLayout(self.gridLayout_4, 2, 0, 1, 1)
        self.line_2 = QtWidgets.QFrame(CorePackTest)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout_2.addWidget(self.line_2, 1, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_5 = QtWidgets.QLabel(CorePackTest)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 11, 0, 1, 1)
        self.label_status_ddr = QtWidgets.QLabel(CorePackTest)
        self.label_status_ddr.setMinimumSize(QtCore.QSize(0, 35))
        self.label_status_ddr.setText("")
        self.label_status_ddr.setObjectName("label_status_ddr")
        self.gridLayout.addWidget(self.label_status_ddr, 11, 1, 1, 2)
        self.line_5 = QtWidgets.QFrame(CorePackTest)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.gridLayout.addWidget(self.line_5, 12, 1, 1, 2)
        self.label_6 = QtWidgets.QLabel(CorePackTest)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 13, 0, 1, 1)
        self.label_status_gty = QtWidgets.QLabel(CorePackTest)
        self.label_status_gty.setMinimumSize(QtCore.QSize(0, 35))
        self.label_status_gty.setText("")
        self.label_status_gty.setObjectName("label_status_gty")
        self.gridLayout.addWidget(self.label_status_gty, 13, 1, 1, 2)
        self.btn_ddr_detial = QtWidgets.QPushButton(CorePackTest)
        self.btn_ddr_detial.setObjectName("btn_ddr_detial")
        self.gridLayout.addWidget(self.btn_ddr_detial, 11, 3, 1, 1)
        self.btn_gty_detial = QtWidgets.QPushButton(CorePackTest)
        self.btn_gty_detial.setObjectName("btn_gty_detial")
        self.gridLayout.addWidget(self.btn_gty_detial, 13, 3, 1, 1)
        self.line_4 = QtWidgets.QFrame(CorePackTest)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridLayout.addWidget(self.line_4, 14, 1, 1, 2)
        self.label_7 = QtWidgets.QLabel(CorePackTest)
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 15, 0, 1, 1)
        self.line_6 = QtWidgets.QFrame(CorePackTest)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.gridLayout.addWidget(self.line_6, 10, 1, 1, 2)
        self.line_3 = QtWidgets.QFrame(CorePackTest)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout.addWidget(self.line_3, 16, 1, 1, 2)
        self.label_8 = QtWidgets.QLabel(CorePackTest)
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 17, 0, 1, 1)
        self.btn_emmc_detial = QtWidgets.QPushButton(CorePackTest)
        self.btn_emmc_detial.setObjectName("btn_emmc_detial")
        self.gridLayout.addWidget(self.btn_emmc_detial, 17, 3, 1, 1)
        self.btn_gpio_detial = QtWidgets.QPushButton(CorePackTest)
        self.btn_gpio_detial.setObjectName("btn_gpio_detial")
        self.gridLayout.addWidget(self.btn_gpio_detial, 15, 3, 1, 1)
        self.line = QtWidgets.QFrame(CorePackTest)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 0, 1, 4)
        self.btn_start = QtWidgets.QPushButton(CorePackTest)
        self.btn_start.setObjectName("btn_start")
        self.gridLayout.addWidget(self.btn_start, 0, 2, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.bar_process = QtWidgets.QProgressBar(CorePackTest)
        self.bar_process.setMaximumSize(QtCore.QSize(570, 16777215))
        self.bar_process.setProperty("value", self.bar_process_value)
        self.bar_process.setObjectName("bar_process")
        self.gridLayout_3.addWidget(self.bar_process, 0, 2, 1, 1)
        self.select_comm = QtWidgets.QComboBox(CorePackTest)
        self.select_comm.setObjectName("select_comm")
        self.gridLayout_3.addWidget(self.select_comm, 0, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(CorePackTest)
        self.label_11.setMaximumSize(QtCore.QSize(70, 16777215))
        self.label_11.setObjectName("label_11")
        self.gridLayout_3.addWidget(self.label_11, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_3, 2, 0, 2, 4)
        self.btn_serial_detial = QtWidgets.QPushButton(CorePackTest)
        self.btn_serial_detial.setObjectName("btn_serial_detial")
        self.gridLayout.addWidget(self.btn_serial_detial, 5, 3, 1, 1)
        self.label_status_rf = QtWidgets.QLabel(CorePackTest)
        self.label_status_rf.setMinimumSize(QtCore.QSize(0, 35))
        self.label_status_rf.setText("")
        self.label_status_rf.setObjectName("label_status_rf")
        self.gridLayout.addWidget(self.label_status_rf, 7, 1, 1, 2)
        self.btn_rf_detial = QtWidgets.QPushButton(CorePackTest)
        self.btn_rf_detial.setObjectName("btn_rf_detial")
        self.gridLayout.addWidget(self.btn_rf_detial, 7, 3, 1, 1)
        self.line_7 = QtWidgets.QFrame(CorePackTest)
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.gridLayout.addWidget(self.line_7, 8, 1, 1, 2)
        self.label_2 = QtWidgets.QLabel(CorePackTest)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 7, 0, 1, 1)
        self.edit_pack_number = QtWidgets.QLineEdit(CorePackTest)
        self.edit_pack_number.setObjectName("edit_pack_number")
        self.gridLayout.addWidget(self.edit_pack_number, 0, 1, 1, 1)
        self.select_language = QtWidgets.QComboBox(CorePackTest)
        self.select_language.setObjectName("select_language")
        self.select_language.addItem("")
        self.select_language.addItem("")
        self.gridLayout.addWidget(self.select_language, 0, 3, 1, 1)
        self.line_9 = QtWidgets.QFrame(CorePackTest)
        self.line_9.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.gridLayout.addWidget(self.line_9, 4, 0, 1, 4)
        self.label = QtWidgets.QLabel(CorePackTest)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_13 = QtWidgets.QLabel(CorePackTest)
        self.label_13.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName("label_13")
        self.gridLayout.addWidget(self.label_13, 5, 0, 1, 1)
        self.label_status_serial = QtWidgets.QLabel(CorePackTest)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_status_serial.sizePolicy().hasHeightForWidth())
        self.label_status_serial.setSizePolicy(sizePolicy)
        self.label_status_serial.setMinimumSize(QtCore.QSize(0, 35))
        self.label_status_serial.setText("")
        self.label_status_serial.setObjectName("label_status_serial")
        self.gridLayout.addWidget(self.label_status_serial, 5, 1, 1, 2)
        self.line_8 = QtWidgets.QFrame(CorePackTest)
        self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.gridLayout.addWidget(self.line_8, 6, 1, 1, 2)
        self.label_4 = QtWidgets.QLabel(CorePackTest)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 9, 0, 1, 1)
        self.table_status_chnl = QtWidgets.QTableWidget(CorePackTest)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.table_status_chnl.sizePolicy().hasHeightForWidth())
        self.table_status_chnl.setSizePolicy(sizePolicy)
        self.table_status_chnl.setMinimumSize(QtCore.QSize(0, 35))
        self.table_status_chnl.setMaximumSize(QtCore.QSize(16777215, 35))
        self.table_status_chnl.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_status_chnl.setRowCount(1)
        self.table_status_chnl.setColumnCount(8)
        self.table_status_chnl.setObjectName("table_status_chnl")
        self.table_status_chnl.horizontalHeader().setVisible(False)
        self.table_status_chnl.horizontalHeader().setDefaultSectionSize(85)
        self.table_status_chnl.horizontalHeader().setMinimumSectionSize(24)
        self.table_status_chnl.verticalHeader().setVisible(False)
        self.table_status_chnl.verticalHeader().setHighlightSections(True)
        self.gridLayout.addWidget(self.table_status_chnl, 9, 1, 1, 2)
        self.btn_chnl_detial = QtWidgets.QPushButton(CorePackTest)
        self.btn_chnl_detial.setObjectName("btn_chnl_detial")
        self.gridLayout.addWidget(self.btn_chnl_detial, 9, 3, 1, 1)
        self.label_status_emmc = QtWidgets.QLabel(CorePackTest)
        self.label_status_emmc.setMinimumSize(QtCore.QSize(0, 35))
        self.label_status_emmc.setText("")
        self.label_status_emmc.setObjectName("label_status_emmc")
        self.gridLayout.addWidget(self.label_status_emmc, 17, 1, 1, 2)
        self.table_status_gpio = QtWidgets.QTableWidget(CorePackTest)
        self.table_status_gpio.setMinimumSize(QtCore.QSize(0, 155))
        self.table_status_gpio.setMaximumSize(QtCore.QSize(16777215, 155))
        self.table_status_gpio.setAutoScrollMargin(16)
        self.table_status_gpio.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_status_gpio.setGridStyle(QtCore.Qt.SolidLine)
        self.table_status_gpio.setRowCount(4)
        self.table_status_gpio.setColumnCount(8)
        self.table_status_gpio.setObjectName("table_status_gpio")
        self.table_status_gpio.horizontalHeader().setVisible(False)
        self.table_status_gpio.horizontalHeader().setCascadingSectionResizes(False)
        self.table_status_gpio.horizontalHeader().setDefaultSectionSize(85)
        self.table_status_gpio.horizontalHeader().setMinimumSectionSize(24)
        self.table_status_gpio.verticalHeader().setVisible(False)
        self.gridLayout.addWidget(self.table_status_gpio, 15, 1, 1, 2)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.label_status_rf.setAlignment(QtCore.Qt.AlignCenter)
        self.label_status_ddr.setAlignment(QtCore.Qt.AlignCenter)
        self.label_status_emmc.setAlignment(QtCore.Qt.AlignCenter)
        self.label_status_serial.setAlignment(QtCore.Qt.AlignCenter)
        self.label_status_gty.setAlignment(QtCore.Qt.AlignCenter)
        # self.table_status_gpio.
        # 192.168.1.152
        self.retranslateUi(CorePackTest)
        QtCore.QMetaObject.connectSlotsByName(CorePackTest)

    def retranslateUi(self, CorePackTest):
        _translate = QtCore.QCoreApplication.translate
        CorePackTest.setWindowTitle(_translate("CorePackTest", "Form"))
        self.label_3.setText(_translate("CorePackTest", "串口打印:"))
        self.label_9.setText(_translate("CorePackTest", "日志打印:"))
        self.btn_output.setText(_translate("CorePackTest", "全部导出"))
        self.label_10.setText(_translate("CorePackTest", "测试记录"))
        self.label_5.setText(_translate("CorePackTest", "DDR状态:"))
        self.label_6.setText(_translate("CorePackTest", "GTY状态:"))
        self.btn_ddr_detial.setText(_translate("CorePackTest", "详情"))
        self.btn_gty_detial.setText(_translate("CorePackTest", "详情"))
        self.label_7.setText(_translate("CorePackTest", "GPIO状态:"))
        self.label_8.setText(_translate("CorePackTest", "EMMC状态:"))
        self.btn_emmc_detial.setText(_translate("CorePackTest", "详情"))
        self.btn_gpio_detial.setText(_translate("CorePackTest", "详情"))
        self.btn_start.setText(_translate("CorePackTest", "开始测试"))
        self.label_11.setText(_translate("CorePackTest", "选择串口"))
        self.btn_serial_detial.setText(_translate("CorePackTest", "详情"))
        self.btn_rf_detial.setText(_translate("CorePackTest", "详情"))
        self.label_2.setText(_translate("CorePackTest", "射频状态:"))
        self.select_language.setItemText(0, _translate("CorePackTest", "zh_TW"))
        self.select_language.setItemText(1, _translate("CorePackTest", "zh_CN"))
        self.label.setText(_translate("CorePackTest", "核心板编号"))
        self.label_13.setText(_translate("CorePackTest", "串口状态"))
        self.label_4.setText(_translate("CorePackTest", "AD/DA回环:"))
        self.btn_chnl_detial.setText(_translate("CorePackTest", "详情"))
