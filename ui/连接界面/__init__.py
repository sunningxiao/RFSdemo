import socket
from serial.tools import list_ports
import threading
import re
from typing import TYPE_CHECKING

from PyQt5 import QtCore, QtGui, QtWidgets

from core.config import global_desktop_center
from core.interface import DataTCPInterface, CommandTCPInterface, CommandSerialInterface
from ui.连接界面.link_system import Ui_Form
from ui.utils import center_move2_point
from tools.printLog import *

if TYPE_CHECKING:
    from ui import RFSControl


ip_match = r'^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$'


class LinkSystemUI(QtWidgets.QDialog, Ui_Form):
    def __init__(self, parent=None):
        super(LinkSystemUI, self).__init__(None)

        self.__parent: "RFSControl" = parent

        self.setupUi(self)
        self.setWindowTitle('连接RFS')

        pix = QtGui.QPixmap("static/logo.png")
        self.label_logo.setPixmap(pix)
        self.label_logo.setScaledContents(True)

        ico = QtGui.QIcon()
        ico.addPixmap(QtGui.QPixmap('static/logo.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(ico)

        self.chk_udp_cmd.setDisabled(True)
        self.widget_serial.setHidden(True)
        self.chk_follow.setChecked(True)
        self.txt_tcp_port.setDisabled(True)
        geo = self.geometry()
        geo.setHeight(10)
        self.setGeometry(geo)
        center_move2_point(self, global_desktop_center)

        # self.widget_tcp.setHidden(True)
        self.chk_serial_cmd.clicked.connect(self.action_change_cmd_type)
        self.chk_tcp_cmd.clicked.connect(self.action_change_cmd_type)

        self.chk_follow.stateChanged.connect(self.action_port_state)
        self.select_tcp_addr.currentTextChanged.connect(self.action_port_state)
        self.chk_serial_cmd.setDisabled(True)
        # self.chk_use_serial.stateChanged.connect(self.action_port_state)
        self.btn_open.clicked.connect(self.action_click_open)

        self.scanning_board()

    def action_click_open(self):
        if self.chk_serial_cmd.isChecked():
            CommandSerialInterface._target_id = self.select_serial_addr.currentText()
            CommandSerialInterface._target_baud_rate = int(self.txt_baud.text())
            CommandSerialInterface._timeout = 5
            self.__parent.init_system(CommandSerialInterface, DataTCPInterface)
        elif self.chk_tcp_cmd.isChecked():
            CommandTCPInterface._target_id = self.select_tcp_addr.currentText()
            CommandTCPInterface._timeout = 10
            DataTCPInterface._local_port = int(self.txt_tcp_port.text())

            addrs = []
            for i in range(self.select_tcp_addr.count()):
                ip = self.select_tcp_addr.itemText(i)
                if ip != CommandTCPInterface._target_id:
                    addrs.append(ip)
            self.__parent.init_system(CommandTCPInterface, DataTCPInterface, addrs=addrs)
        self.close()

    def action_change_cmd_type(self):
        _serial = self.chk_serial_cmd.isChecked()
        self.widget_serial.setVisible(_serial)
        _tcp = self.chk_tcp_cmd.isChecked()
        self.widget_tcp.setVisible(_tcp)
        QtWidgets.QApplication.instance().processEvents()
        geo = self.geometry()
        geo.setHeight(10)
        self.setGeometry(geo)

    def action_port_state(self, *args):
        checked = self.chk_follow.isChecked()
        self.txt_tcp_port.setDisabled(checked)
        if checked:
            ip = self.select_tcp_addr.currentText()
            if len(ip) >= 12 and re.match(ip_match, ip):
                _port = ip.split('.')[3][-2:]
                _port = _port[0] + '00' + _port[1]
                self.txt_tcp_port.setText(_port)

    def scanning_board(self):
        """
        扫描板卡

        :return:
        """
        dest = ('<broadcast>', 5003)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        addrs = socket.getaddrinfo(socket.gethostname(), None)
        addr = [addr[4][0] for addr in addrs if addr[4][0].startswith('192.168.1.')]
        if not addr:
            printWarning('本机没有192.168.1.0网段的ip地址，不能完成扫描')
            return
        printInfo(f'本机IP：{addr[0]}')
        try:
            s.bind((addr[0], 15000))
        except:
            printWarning('扫描端口15000绑定失败，不能完成扫描')
            return
        s.sendto(b"____\x10\x00\x002\x00\x00\x00\x00\x14\x00\x00\x00\x00\x00\x00\x00", dest)
        s.settimeout(3)

        def udp_func():
            try:
                while True:
                    (_, addr) = s.recvfrom(2048)
                    self.select_tcp_addr.addItem(addr[0])
            except:
                s.close()
                # self.ui.select_link_addr.setCurrentIndex(0)
                printInfo('板卡扫描完成')

        def serial_func():
            for serial in list_ports.comports():
                self.select_serial_addr.addItem(serial.device)

        _thread = threading.Thread(target=udp_func, daemon=True)
        _thread.start()

        _thread = threading.Thread(target=serial_func, daemon=True)
        _thread.start()
