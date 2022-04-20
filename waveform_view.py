import threading
import time

from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
import numpy as np

from core import RFSKit
from core.interface import DataTCPInterface, CommandTCPInterface
from core.config import global_event_loop

from tools.printLog import *
from tools.data_unpacking import UnPackage

from ui.连接界面 import LinkSystemUI
from waveform_view_ui import Ui_WaveformViewUI


class WaveformView(QtWidgets.QWidget, Ui_WaveformViewUI):
    max_channel_count = 8
    sig_show_waveform = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super(WaveformView, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('WaveformView')

        # 连接目标板卡
        self.link_system_ui = LinkSystemUI(self)
        self.link_system_ui.show()

        # 关联信号槽
        self.btn_start.clicked.connect(self.click_start)
        self.sig_show_waveform.connect(self.show_unpack)

    def setupUi(self, WaveformViewUI):
        """
        绘制界面, 继承自Ui_WaveformViewUI

        :param WaveformViewUI:
        :return:
        """
        super(WaveformView, self).setupUi(WaveformViewUI)

        # 初始化波形绘制widget
        self.plot_win = pg.GraphicsLayoutWidget()
        self.wave_layout.addWidget(self.plot_win)

        self.lplt = self.plot_win.addPlot()
        self.lplt.setLabel('top', '回波数据')

        # 全波形总览
        self.plot_win.nextRow()
        self.lplt_all = self.plot_win.addPlot()
        self.lplt_all.setMaximumHeight(60)
        self.lplt_all.setXRange(0, 35000)
        lr = pg.LinearRegionItem([0, 4096])
        lr.setZValue(-10)
        self.lplt_all.addItem(lr)

        def updatePlot():
            self.lplt.setXRange(*lr.getRegion(), padding=0)

        def updateRegion():
            lr.setRegion(self.lplt.getViewBox().viewRange()[0])

        lr.sigRegionChanged.connect(updatePlot)
        self.lplt.sigXRangeChanged.connect(updateRegion)
        updatePlot()

        self.plot_color = ['r', 'g', 'b', 'c', 'm', 'y', (128, 200, 20), 'w']
        self.chk_channels = [getattr(self, f'chk_{i}') for i in range(8)]
        self.channel_plots = {
            self.chk_channels[i]: [self.lplt.plot(name=f'chnl{i}'), self.lplt_all.plot(name=f'chnl{i}'),
                                   self.plot_color[i]]
            for i in range(self.max_channel_count)}
        pg.mkPen()

    def init_system(self, cmd_interface=CommandTCPInterface, data_interface=DataTCPInterface, **kwargs):
        """
        连接目标板卡，由LinkSystemUI.action_click_open方法隐式回调

        :param cmd_interface:
        :param data_interface:
        :param kwargs:
        :return:
        """
        self.rfs_kit = RFSKit(
            cmd_interface=cmd_interface,
            data_interface=data_interface,
            auto_load_icd=True)
        self.show()

    def click_start(self):
        """
        槽函数，开启本机的tcp server
        等待rfs主动连接后，接收数据
        通过RFSKit.view_stream_data抽包显示数据

        :return:
        """
        ip = self.link_system_ui.select_tcp_addr.currentText()
        self.rfs_kit.start_stream(write_file=self.chk_write_file.isChecked(), file_name=ip.split('.')[3])

        def _func():
            while self.rfs_kit._data_solve.upload_stop_event.is_set():
                # 在数据上行队列队尾抽取一包进行显示
                data = self.rfs_kit.view_stream_data()
                # 数据解交织，将8通道交织在一起的数据解开
                data = UnPackage.solve_source_data(data, [True]*16, 16384)
                if data:
                    # 将解包好的数据通过sig_show_waveform信号发送出去
                    # 跨python线程直接操作widget渲染容易发生崩溃
                    self.sig_show_waveform.emit(data)
                    # self.show_unpack(data)
                    time.sleep(1)

        # 在一个独立的线程内做循环
        _thread = threading.Thread(target=_func, daemon=True)
        _thread.start()
        return True

    def show_unpack(self, data):
        """
        将波形绘制在界面上

        :param data: UnPackage.solve_source_data解包后的数据
        :return:
        """
        chk_info = [chk.isChecked() for chk in self.channel_plots]
        for index, (chk, chnl_pen) in enumerate(self.channel_plots.items()):
            if chk_info[index]:
                try:
                    _data = data[data['head'][index]['name']]
                except Exception as e:
                    _data = [0] * 4096
                chnl_pen[0].setData(_data, pen=chnl_pen[2])
                chnl_pen[0].show()
                chnl_pen[1].setData(_data, pen=chnl_pen[2])
                chnl_pen[1].show()
            else:
                chnl_pen[0].hide()
                chnl_pen[1].hide()


if __name__ == '__main__':
    import platform

    if platform.system() == 'Windows':
        import ctypes

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("naishu")

    view = WaveformView()
    # rfs.link_system_ui.show()
    printInfo("软件已启动")

    with global_event_loop:
        global_event_loop.run_forever()
