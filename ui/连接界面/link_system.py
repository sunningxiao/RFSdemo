# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'link_system.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(405, 240)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(7, 7, 7, 7)
        self.gridLayout.setObjectName("gridLayout")
        self.chk_tcp_cmd = QtWidgets.QRadioButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chk_tcp_cmd.sizePolicy().hasHeightForWidth())
        self.chk_tcp_cmd.setSizePolicy(sizePolicy)
        self.chk_tcp_cmd.setChecked(True)
        self.chk_tcp_cmd.setObjectName("chk_tcp_cmd")
        self.buttonGroup = QtWidgets.QButtonGroup(Form)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.chk_tcp_cmd)
        self.gridLayout.addWidget(self.chk_tcp_cmd, 0, 2, 1, 1)
        self.chk_serial_cmd = QtWidgets.QRadioButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chk_serial_cmd.sizePolicy().hasHeightForWidth())
        self.chk_serial_cmd.setSizePolicy(sizePolicy)
        self.chk_serial_cmd.setObjectName("chk_serial_cmd")
        self.buttonGroup.addButton(self.chk_serial_cmd)
        self.gridLayout.addWidget(self.chk_serial_cmd, 0, 1, 1, 1)
        self.label_logo = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_logo.sizePolicy().hasHeightForWidth())
        self.label_logo.setSizePolicy(sizePolicy)
        self.label_logo.setMaximumSize(QtCore.QSize(100, 78))
        self.label_logo.setText("")
        self.label_logo.setObjectName("label_logo")
        self.gridLayout.addWidget(self.label_logo, 0, 0, 4, 1)
        self.chk_udp_cmd = QtWidgets.QRadioButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chk_udp_cmd.sizePolicy().hasHeightForWidth())
        self.chk_udp_cmd.setSizePolicy(sizePolicy)
        self.chk_udp_cmd.setObjectName("chk_udp_cmd")
        self.buttonGroup.addButton(self.chk_udp_cmd)
        self.gridLayout.addWidget(self.chk_udp_cmd, 0, 3, 1, 1)
        self.btn_open = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_open.sizePolicy().hasHeightForWidth())
        self.btn_open.setSizePolicy(sizePolicy)
        self.btn_open.setMinimumSize(QtCore.QSize(0, 35))
        self.btn_open.setMaximumSize(QtCore.QSize(16777215, 35))
        self.btn_open.setObjectName("btn_open")
        self.gridLayout.addWidget(self.btn_open, 3, 3, 1, 1)
        self.widget_serial = QtWidgets.QWidget(Form)
        self.widget_serial.setObjectName("widget_serial")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.widget_serial)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.select_serial_addr = QtWidgets.QComboBox(self.widget_serial)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.select_serial_addr.sizePolicy().hasHeightForWidth())
        self.select_serial_addr.setSizePolicy(sizePolicy)
        self.select_serial_addr.setMinimumSize(QtCore.QSize(0, 35))
        self.select_serial_addr.setEditable(True)
        self.select_serial_addr.setObjectName("select_serial_addr")
        self.gridLayout_4.addWidget(self.select_serial_addr, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.widget_serial)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout_4.addWidget(self.label_4, 0, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.widget_serial)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout_4.addWidget(self.label_5, 1, 0, 1, 1)
        self.txt_baud = QtWidgets.QLineEdit(self.widget_serial)
        self.txt_baud.setMinimumSize(QtCore.QSize(0, 35))
        self.txt_baud.setMaximumSize(QtCore.QSize(16777215, 35))
        self.txt_baud.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.txt_baud.setObjectName("txt_baud")
        self.gridLayout_4.addWidget(self.txt_baud, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.widget_serial, 2, 1, 1, 3)
        self.widget_tcp = QtWidgets.QWidget(Form)
        self.widget_tcp.setObjectName("widget_tcp")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.widget_tcp)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_7 = QtWidgets.QLabel(self.widget_tcp)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout_5.addWidget(self.label_7, 1, 0, 1, 1)
        self.txt_tcp_port = QtWidgets.QLineEdit(self.widget_tcp)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txt_tcp_port.sizePolicy().hasHeightForWidth())
        self.txt_tcp_port.setSizePolicy(sizePolicy)
        self.txt_tcp_port.setMinimumSize(QtCore.QSize(0, 35))
        self.txt_tcp_port.setMaximumSize(QtCore.QSize(16777215, 35))
        self.txt_tcp_port.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.txt_tcp_port.setObjectName("txt_tcp_port")
        self.gridLayout_5.addWidget(self.txt_tcp_port, 1, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.widget_tcp)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout_5.addWidget(self.label_6, 0, 0, 1, 1)
        self.chk_follow = QtWidgets.QCheckBox(self.widget_tcp)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chk_follow.sizePolicy().hasHeightForWidth())
        self.chk_follow.setSizePolicy(sizePolicy)
        self.chk_follow.setChecked(False)
        self.chk_follow.setObjectName("chk_follow")
        self.gridLayout_5.addWidget(self.chk_follow, 1, 2, 1, 1)
        self.select_tcp_addr = QtWidgets.QComboBox(self.widget_tcp)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.select_tcp_addr.sizePolicy().hasHeightForWidth())
        self.select_tcp_addr.setSizePolicy(sizePolicy)
        self.select_tcp_addr.setMinimumSize(QtCore.QSize(0, 35))
        self.select_tcp_addr.setEditable(True)
        self.select_tcp_addr.setObjectName("select_tcp_addr")
        self.gridLayout_5.addWidget(self.select_tcp_addr, 0, 1, 1, 2)
        self.gridLayout.addWidget(self.widget_tcp, 1, 1, 1, 3)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.chk_tcp_cmd.setText(_translate("Form", "TCP指令"))
        self.chk_serial_cmd.setText(_translate("Form", "串口指令"))
        self.chk_udp_cmd.setText(_translate("Form", "UDP指令"))
        self.btn_open.setText(_translate("Form", "打开"))
        self.label_4.setText(_translate("Form", "目标地址"))
        self.label_5.setText(_translate("Form", "波特率"))
        self.txt_baud.setText(_translate("Form", "115200"))
        self.label_7.setText(_translate("Form", "数据端口"))
        self.txt_tcp_port.setText(_translate("Form", "5002"))
        self.label_6.setText(_translate("Form", "目标地址"))
        self.chk_follow.setText(_translate("Form", "跟随ip"))
