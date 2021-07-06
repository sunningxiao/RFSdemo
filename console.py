#! /usr/bin/python3
# -*- coding:utf-8 -*-

import sys
import threading
import qdarkstyle
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg
import socket
import numpy as np
from numpy import fft

import ui.CTYui as ui
import ui.dds_config_ui as dds_config_ui
import ui.start_ui as start_ui
import ui.wave_file_ui as wave_file_ui
import ui.spectrum_ui as spectrum_ui
import ui.qmc_config_ui as qmc_config_ui
from printLog import *
import icd_parser
from pgdialog import pgdialog
from data_solve import us_signal


class QSignal(QtCore.QObject):
    txt_trigger = QtCore.pyqtSignal(str)

    def __init__(self, queue, *args, **kwargs):
        QtCore.QObject.__init__(self, *args, **kwargs)
        self.queue = queue

    def printLog(self):
        while True:
            text = self.queue.get()
            self.txt_trigger.emit(text)


class DDSConfig(QtWidgets.QDialog, dds_config_ui.Ui_Dialog):
    def __init__(self, ui_parent):
        super(DDSConfig, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('DDS设置_参数检查')
        self.btn_cancel.clicked.connect(self.close)
        self.ui_parent: JGFConsole = ui_parent

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.ui_parent.show_param()

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        self.ui_parent.show_dds_config_ui()


class StartConfig(QtWidgets.QDialog, start_ui.Ui_Dialog):
    def __init__(self, ui_parent):
        super(StartConfig, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('系统开启_参数检查')
        self.btn_cancel.clicked.connect(self.close)
        self.ui_parent: JGFConsole = ui_parent

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.ui_parent.show_param()

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        self.ui_parent.show_start_ui()


class WaveFileConfig(QtWidgets.QDialog, wave_file_ui.Ui_Dialog):
    def __init__(self, ui_parent):
        super(WaveFileConfig, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('波形装载--双击文件名清除选择')
        self.btn_cancel.clicked.connect(self.close)
        self.ui_parent: JGFConsole = ui_parent

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        self.ui_parent.show_wave_file_ui()


class QMCConfig(QtWidgets.QDialog, qmc_config_ui.Ui_Dialog):
    def __init__(self, ui_parent):
        super(QMCConfig, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('QMC配置')
        self.btn_cancel.clicked.connect(self.close)
        self.ui_parent: JGFConsole = ui_parent

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        self.ui_parent.show_qmc_config_ui()


class SpectrumScreen(QtWidgets.QDialog, spectrum_ui.Ui_Dialog):
    def __init__(self, ui_parent):
        super(SpectrumScreen, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('频谱快视')
        self.ui_parent: JGFConsole = ui_parent
        self.plot_win = pg.GraphicsLayoutWidget()
        self.wave_show_win.addWidget(self.plot_win)
        self.plots = []
        # 频谱展示
        self.spectrum_plot = self.append_plot('回波频谱(dB)')
        self.channel_plots = [self.spectrum_plot.plot(name=f'chnl{i}') for i in range(8)]

    def append_plot(self, name, axis=None):
        if axis:
            plot = self.plot_win.addPlot(axisItems={'bottom': axis})
        else:
            plot = self.plot_win.addPlot()
        plot.setLabel('top', name)
        self.plots.append(plot)
        return plot

    # def showEvent(self, a0: QtGui.QShowEvent) -> None:
    #     self.plot_win.clear()
    #     self.plots = []
    #     axis = pg.AxisItem(orientation='bottom')
    #     n = self.ui_parent.icd_param.get_param(f'ADC0采样点数', 32) * 1000
    #     fs = self.ui_parent.icd_param.get_param(f'ADC采样率', 4000)
    #     tick = [list(zip(range(n), ('{:.2f}'.format(fs / (i + 1)) for i in range(n))))]
    #     axis.setTicks(tick)
    #     self.spectrum_plot = self.append_plot('回波频谱(dB)', axis)

    def show_data(self, index, need_show, data=(), _pen='w'):
        if need_show:
            self.channel_plots[index].setData(20*np.log10(np.abs(fft.fftshift(fft.fft(data)))), pen=_pen)
            self.channel_plots[index].show()
        else:
            self.channel_plots[index].hide()


class JGFConsole(QtWidgets.QWidget):
    max_channel_count = 8
    page_size = 50
    _speed_fmt = "传输速率: {:.2f} MB/s"
    _save_speed_fmt = "存储速率: {:.2f} MB/s"
    _update_unload_status_interval = 1
    _update_record_status_interval = 1e-3
    _status = 0  # 运行状态
    _text_line = 0

    def __init__(self):
        super().__init__()
        self.ui = ui.Ui_Form()
        self.dds_config_ui = DDSConfig(self)
        self.start_ui = StartConfig(self)
        self.wave_file_config_ui = WaveFileConfig(self)
        self.spectrum_screen = SpectrumScreen(self)
        self.qmc_config_ui = QMCConfig(self)
        self.initUI()

        self.icd_param = icd_parser.ICDParams()

        # self.check_all_btn = self.ui.btn_checkall
        # self.page = Page(self.ui, self.page_size, self.update_table)  # 分页
        self.enable_chk_channels = []
        self.scanning_board()

    def initUI(self):
        self.ui.setupUi(self)
        pix = QtGui.QPixmap("ui/logo.png")
        self.ui.lab_logo.setPixmap(pix)
        self.ui.lab_logo.setScaledContents(True)

        ico = QtGui.QIcon()
        ico.addPixmap(QtGui.QPixmap('ui/logo.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(ico)

        # 关联按钮
        self.ui.btn_auto_command.clicked.connect(self.linking_auto_button)

        self.ui.btn_reload_icd.clicked.connect(self.reload_param)

        self.ui.btn_connect.clicked.connect(self.click_connect)

        self.ui.btn_show_spectrum.clicked.connect(self.spectrum_screen.show)

        self.ui.btn_qmc_cfg.clicked.connect(self.qmc_config_ui.show)
        self.qmc_config_ui.btn_config.clicked.connect(
            self.linking_button('QMC配置', need_feedback=True, need_file=False)
        )
        self.link_qmc_config_ui()

        self.ui.btn_start.clicked.connect(self.start_ui.show)
        self.start_ui.btn_config.clicked.connect(
            self.linking_button('系统开启', need_feedback=True, need_file=False, callback=self.click_start))
        self.link_start_ui()

        self.ui.btn_stop.clicked.connect(
            self.linking_button('系统停止', need_feedback=True, need_file=False, callback=self.click_stop))
        self.ui.btn_rf_cfg.clicked.connect(self.linking_button('RF配置', need_feedback=True, need_file=False))

        # dds相关的输入关联
        self.ui.btn_dss_cfg.clicked.connect(self.dds_config_ui.show)
        self.dds_config_ui.btn_config.clicked.connect(self.linking_button('DDS配置',
                                                                          need_feedback=True,
                                                                          need_file=False,
                                                                          callback=self.dds_config_ui.close))
        self.link_dds_config_ui()

        self.ui.btn_wave.clicked.connect(self.wave_file_config_ui.show)
        self.wave_file_config_ui.btn_config.clicked.connect(self.click_wave)
        self.link_wave_file_ui()
        # self.ui.btn_wave.clicked.connect(self.linking_button('波形装载', need_feedback=True, need_file=True))
        self.ui.btn_framwork_up.clicked.connect(
            self.linking_button('固件更新', need_feedback=True, need_file=True, wait=20)
        )

        # 关联界面参数与json
        self.ui.select_clock.currentIndexChanged.connect(
            self.change_param('系统参考时钟选择', self.ui.select_clock, int, 'index'))
        self.ui.select_adc_sample.currentIndexChanged.connect(
            self.change_param('ADC采样率', self.ui.select_adc_sample, int))
        self.ui.txt_adc_noc_f.editingFinished.connect(self.change_param('ADC NCO频率', self.ui.txt_adc_noc_f))
        self.ui.txt_adc_nyq.editingFinished.connect(self.change_param('ADC 奈奎斯特区', self.ui.txt_adc_nyq, int))
        self.ui.select_dac_sample.currentIndexChanged.connect(
            self.change_param('DAC采样率', self.ui.select_dac_sample, int))
        self.ui.txt_dac_noc_f.editingFinished.connect(self.change_param('DAC NCO频率', self.ui.txt_dac_noc_f))
        self.ui.txt_dac_nyq.editingFinished.connect(self.change_param('DAC 奈奎斯特区', self.ui.txt_dac_nyq, int))

        self.plot_win = pg.GraphicsLayoutWidget()
        self.ui.grid_graph.addWidget(self.plot_win)

        self.lplt = self.plot_win.addPlot()
        # self.ui.grid_graph.addWidget(self.lplt)
        # self.lplt.setYRange(-1.5, 1.5)
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
        self.chk_channels = [self.ui.chk1, self.ui.chk2, self.ui.chk3, self.ui.chk4, self.ui.chk5, self.ui.chk6,
                             self.ui.chk7, self.ui.chk8]
        self.channel_plots = {self.chk_channels[i]: [self.lplt.plot(name=f'chnl{i}'), self.lplt_all.plot(name=f'chnl{i}'), self.plot_color[i]]
                              for i in range(self.max_channel_count)}
        pg.mkPen()
        self.gui_state(0)
        self.ui.tabWidget.setCurrentIndex(0)
        self.ui.tabWidget.setTabEnabled(1, False)
        self.show()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        # self.close(程序退出)触发
        # self.icd_param.param.pop('DDS_RAM')
        self.icd_param.save_icd()
        self.icd_param.data_solve._stop_flag = True
        self.icd_param.data_server.close()
        if self._status == 2:
            # 判断状态，发送停止指令
            self.linking_button('系统停止', need_feedback=False, need_file=False)()

    def scanning_board(self):
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

        def _func():
            try:
                while True:
                    (_, addr) = s.recvfrom(2048)
                    self.ui.select_link_addr.addItem(addr[0])
            except:
                s.close()
                self.ui.select_link_addr.setCurrentIndex(0)
                printInfo('板卡扫描完成')

        _thread = threading.Thread(target=_func)
        _thread.start()

    def update_textlog(self, msg):
        try:
            if self._text_line >= 100:
                self.ui.textBrowser.clear()
                self._text_line = 0
            self.ui.textBrowser.moveCursor(QtGui.QTextCursor.End)
            self.ui.textBrowser.insertHtml(msg)
            self._text_line += 1
        except Exception as e:
            printException(e)

    def click_connect(self):
        ip = self.ui.select_link_addr.currentText()
        _pg = pgdialog(self, self.icd_param.connect, args=(ip, ), label="系统连接", withcancel=False)
        if _pg.perform():
            self.gui_state(1)
            self.ui.tabWidget.setCurrentIndex(0)
            printInfo("记录系统连接成功")
            self.show_unload_status((0, 0))
        else:
            self.gui_state(0)
            printError(f"记录系统连接失败（{_pg.get_err_msg()}）")

    def click_start(self):
        self.gui_state(2)
        self.icd_param.data_solve.start_solve(write_file=self.ui.chk_write_file.isChecked())
        self.start_ui.close()
        return True

    def click_stop(self):
        self.gui_state(1)
        self.icd_param.data_solve._stop_flag = True
        self.icd_param.data_server.close_recv()
        return True

    def click_wave(self):
        def _func():
            chl = self.icd_param.get_param('DDS_RAM')
            try:
                for dds in range(8):
                    self.icd_param.set_param('DDS_RAM', dds)
                    filename = self.icd_param.get_param(f'通道{dds}文件路径', '', str)
                    if filename != '':
                        assert self.icd_param.send_command('波形装载', file_name=filename)
                        printColor(f'通道{dds+1}波形装载完成', 'blue')
            except:
                printWarning('波形装载失败')
            finally:
                self.icd_param.set_param('DDS_RAM', chl)
                us_signal.status_trigger.emit((1, 3, self.wave_file_config_ui.close))
                # self.wave_file_config_ui.close()

        thread = threading.Thread(target=_func)
        thread.start()

    def show_unpack(self, data):
        chk_info = [chk.isChecked() for chk in self.channel_plots]
        for index, (chk, chnl_pen) in enumerate(self.channel_plots.items()):
            if chk_info[index]:
                try:
                    _data = data[data['head'][index]['name']]
                except:
                    _data = [0] * 4096
                chnl_pen[0].setData(_data, pen=chnl_pen[2])
                # 频谱（未归一化）
                # chnl_pen[0].setData(20*np.log10(np.abs(fft.fftshift(fft.fft(_data)))), pen=chnl_pen[2])
                chnl_pen[0].show()
                chnl_pen[1].setData(_data, pen=chnl_pen[2])
                chnl_pen[1].show()
                if self.spectrum_screen.isVisible():
                    self.spectrum_screen.show_data(index, True, _data, chnl_pen[2])
            else:
                chnl_pen[0].hide()
                chnl_pen[1].hide()
                if self.spectrum_screen.isVisible():
                    self.spectrum_screen.show_data(index, False)

    def show_unload_status(self, status):
        """
            status: state, percent, speed, file_process
            state: 0: unload disable; 1: running; 2: stopped;
        """
        state, *status = status
        if state:
            if status[0] == 0:
                self.ui.label.setText(self._speed_fmt.format(status[1]))
            elif status[0] == 1:
                self.ui.label_3.setText(self._save_speed_fmt.format(status[1]))
            elif status[0] == 2:
                self.show_unpack(status[1])
            elif status[0] == 3:
                # 执行回调函数,优化指令执行后的函数回调机制
                status[1]()
            elif status[0] == 4:
                self.icd_param.save_icd(status[1])
        else:
            self.ui.label.setText(self._speed_fmt.format(0))
            self.ui.label_3.setText(self._save_speed_fmt.format(0))

    def gui_state(self, state=1):
        # 未连接状态
        if state == 0:
            self.ui.tabWidget.setEnabled(False)
            self.set_btn([True, True, True, True, True, True, False, False])
        # 空闲状态
        elif state == 1:
            self.ui.label_status.setText("空闲状态")
            self.ui.tabWidget.setEnabled(True)
            self.set_btn([True, True, False, True, True, True, True, True])
        # 记录状态
        elif state == 2:
            self.ui.label_status.setText("开始记录")
            self.set_btn([False, False, True, False, False, True, False, True])
        self._status = state

    def set_btn(self, state):
        self.ui.btn_connect.setEnabled(state[0])         # 建立连接
        self.ui.btn_start.setEnabled(state[1])           # 采集启动
        self.ui.btn_stop.setEnabled(state[2])            # 采集停止
        self.ui.btn_wave.setEnabled(state[3])            # 波形装载
        self.ui.btn_rf_cfg.setEnabled(state[4])          # RF配置
        self.ui.btn_dss_cfg.setEnabled(state[5])         # DSS设置
        self.ui.btn_framwork_up.setEnabled(state[6])     # 固件更新
        self.ui.btn_auto_command.setEnabled(state[7])    # 自定义指令

    def load_param(self):
        self.icd_param.load_icd()
        self.show_param()
        # self.ui.select_link_addr.addItem(self.icd_param.icd_data['remote_ip'])
        # self.icd_param.start_data_server()

    def reload_param(self):
        self.icd_param.load_icd(reload=True)
        self.show_param()

    def show_param(self):
        self.ui.select_clock.setCurrentIndex(int(self.icd_param.get_param('系统参考时钟选择', 0)))
        self.ui.select_adc_sample.setCurrentIndex({1000: 0, 2000: 1, 4000: 2}[self.icd_param.get_param('ADC采样率', 1000)])
        self.ui.txt_adc_noc_f.setText(self.icd_param.get_param('ADC NCO频率', 0, str))
        self.ui.txt_adc_nyq.setText(self.icd_param.get_param('ADC 奈奎斯特区', 1, str))
        self.ui.select_dac_sample.setCurrentIndex({1000: 0, 2000: 1, 4000: 2}[self.icd_param.get_param('DAC采样率', 1000)])
        self.ui.txt_dac_noc_f.setText(self.icd_param.get_param('DAC NCO频率', 0, str))
        self.ui.txt_dac_nyq.setText(self.icd_param.get_param('DAC 奈奎斯特区', 1, str))

        self.ui.select_command.clear()
        for btn in self.icd_param.button:
            self.ui.select_command.addItem(btn)

    def change_param(self, param_name, param_label: [QtWidgets.QLineEdit, QtWidgets.QComboBox], type_fmt=str,
                     combo_flag='text'):
        def _func(*args, **kwargs):
            if isinstance(param_label, QtWidgets.QLineEdit):
                self.icd_param.set_param(param_name, param_label.text(), type_fmt)
            elif isinstance(param_label, QtWidgets.QComboBox):
                if combo_flag == 'text':
                    self.icd_param.set_param(param_name, param_label.currentText(), type_fmt)
                elif combo_flag == 'index':
                    self.icd_param.set_param(param_name, param_label.currentIndex(), type_fmt)
            else:
                printWarning('不受支持的控件类型')

        return _func

    def linking_button(self, button_name, need_feedback=True, check_feedback=True, need_file=False, callback=lambda *args: True,
                       wait: int = 0):
        def _func(*args, **kwargs):
            if need_file:
                filename = QFileDialog.getOpenFileName(self, '请选择文件')[0]
                if filename == '':
                    return
                thread = threading.Thread(target=self.icd_param.send_command,
                                          args=[button_name, need_feedback, filename],
                                          kwargs={'check_feedback': check_feedback, 'callback': callback, 'wait': wait})
            else:
                thread = threading.Thread(target=self.icd_param.send_command,
                                          args=[button_name, need_feedback],
                                          kwargs={'check_feedback': check_feedback, 'callback': callback, 'wait': wait})
            thread.start()

        return _func

    def linking_wave_button(self, dds):
        def _func(*args, **kwargs):
            filename = QFileDialog.getOpenFileName(self.wave_file_config_ui, '请选择文件')[0]
            if filename == '':
                return
            file_name_label: QtWidgets.QLabel = getattr(self.wave_file_config_ui, f'file_name_label_{dds}')
            file_name_label.setText(filename)
            self.icd_param.set_param(f'通道{dds}文件路径', filename, str)

        return _func

    def linking_wave_button_all(self):
        def _func(*args, **kwargs):
            filename = QFileDialog.getOpenFileName(self.wave_file_config_ui, '请选择文件')[0]
            if filename == '':
                return
            for dds in range(8):
                file_name_label: QtWidgets.QLabel = getattr(self.wave_file_config_ui, f'file_name_label_{dds}')
                file_name_label.setText(filename)
                self.icd_param.set_param(f'通道{dds}文件路径', filename, str)

        return _func

    def linking_auto_button(self):
        btn = self.ui.select_command.currentText()
        self.linking_button(btn, need_feedback=True, check_feedback=False, need_file=False)()

    def show_start_ui(self):
        self.start_ui.select_prf_src.setCurrentIndex(self.icd_param.get_param('基准PRF来源', 0))
        self.start_ui.txt_prf_cyc.setText(self.icd_param.get_param('基准PRF周期', 0, str))
        self.start_ui.txt_prf_cnt.setText(self.icd_param.get_param('基准PRF数量', 1000, str))
        for dds in range(8):
            select_source: QtWidgets.QLineEdit = getattr(self.start_ui, f'select_source_{dds}')
            select_source.setCurrentIndex(self.icd_param.get_param(f'DAC{dds}播放数据来源', 0, int))
            txt_gate_width: QtWidgets.QLineEdit = getattr(self.start_ui, f'txt_gate_width_{dds}')
            txt_gate_width.setText(self.icd_param.get_param(f'DAC{dds}播放波门宽度', 0, str))
            txt_gate_delay: QtWidgets.QLineEdit = getattr(self.start_ui, f'txt_gate_delay_{dds}')
            txt_gate_delay.setText(self.icd_param.get_param(f'DAC{dds}播放波门延迟', 0, str))
            txt_sampling_delay: QtWidgets.QLineEdit = getattr(self.start_ui, f'txt_sampling_delay_{dds}')
            txt_sampling_delay.setText(self.icd_param.get_param(f'ADC{dds}采样延迟', 0, str))
            txt_sampling_points: QtWidgets.QLineEdit = getattr(self.start_ui, f'txt_sampling_points_{dds}')
            txt_sampling_points.setText(self.icd_param.get_param(f'ADC{dds}采样点数', 1024, str))

    def link_start_ui(self):
        self.start_ui.select_prf_src.currentIndexChanged.connect(
            self.change_param('基准PRF来源', self.start_ui.select_prf_src, int, 'index'))
        self.start_ui.txt_prf_cyc.editingFinished.connect(self.change_param('基准PRF周期', self.start_ui.txt_prf_cyc))
        self.start_ui.txt_prf_cnt.editingFinished.connect(self.change_param('基准PRF数量', self.start_ui.txt_prf_cnt))
        for dds in range(8):
            select_source: QtWidgets.QLineEdit = getattr(self.start_ui, f'select_source_{dds}')
            select_source.currentIndexChanged.connect(self.change_param(f'DAC{dds}播放数据来源', select_source, int, 'index'))
            txt_gate_width: QtWidgets.QLineEdit = getattr(self.start_ui, f'txt_gate_width_{dds}')
            txt_gate_width.editingFinished.connect(self.change_param(f'DAC{dds}播放波门宽度', txt_gate_width))
            txt_gate_delay: QtWidgets.QLineEdit = getattr(self.start_ui, f'txt_gate_delay_{dds}')
            txt_gate_delay.editingFinished.connect(self.change_param(f'DAC{dds}播放波门延迟', txt_gate_delay))
            txt_sampling_delay: QtWidgets.QLineEdit = getattr(self.start_ui, f'txt_sampling_delay_{dds}')
            txt_sampling_delay.editingFinished.connect(self.change_param(f'ADC{dds}采样延迟', txt_sampling_delay))
            txt_sampling_points: QtWidgets.QLineEdit = getattr(self.start_ui, f'txt_sampling_points_{dds}')
            txt_sampling_points.editingFinished.connect(self.change_param(f'ADC{dds}采样点数', txt_sampling_points))

    def show_dds_config_ui(self):
        def _func(_ui, edit_name, param_name):
            txt: QtWidgets.QLineEdit = getattr(_ui, edit_name)
            txt.setText(self.icd_param.get_param(param_name, 0, str))

        for chl in range(8):
            edits = [f'txt_dds_fc_{chl}', f'txt_dds_fc_step_{chl}', f'txt_dds_fc_range_{chl}',
                     f'txt_dds_band_{chl}', f'txt_dds_pulse_{chl}',
                     f'txt_dds_phase_{chl}', f'txt_dds_phase_step_{chl}', f'txt_dds_phase_range_{chl}']
            params = [f'dds{chl}中心频率', f'dds{chl}频率扫描步进', f'dds{chl}频率扫描范围',
                      f'dds{chl}带宽', f'dds{chl}脉宽',
                      f'dds{chl}初始相位', f'dds{chl}相位扫描步进', f'dds{chl}相位扫描范围']
            for edit, param in zip(edits, params):
                _func(self.dds_config_ui, edit, param)

    def link_dds_config_ui(self):
        def _func(_ui, edit_name, param_name):
            txt: QtWidgets.QLineEdit = getattr(_ui, edit_name)
            txt.editingFinished.connect(self.change_param(param_name, txt))

        for chl in range(8):
            edits = [f'txt_dds_fc_{chl}', f'txt_dds_fc_step_{chl}', f'txt_dds_fc_range_{chl}',
                     f'txt_dds_band_{chl}', f'txt_dds_pulse_{chl}',
                     f'txt_dds_phase_{chl}', f'txt_dds_phase_step_{chl}', f'txt_dds_phase_range_{chl}']
            params = [f'dds{chl}中心频率', f'dds{chl}频率扫描步进', f'dds{chl}频率扫描范围',
                      f'dds{chl}带宽', f'dds{chl}脉宽',
                      f'dds{chl}初始相位', f'dds{chl}相位扫描步进', f'dds{chl}相位扫描范围']
            for edit, param in zip(edits, params):
                _func(self.dds_config_ui, edit, param)

    def show_qmc_config_ui(self):
        def _func(_ui, edit_name, param_name):
            txt: QtWidgets.QLineEdit = getattr(_ui, edit_name)
            txt.setText(self.icd_param.get_param(param_name, 0, str))

        for chl in range(8):
            edits = [f'txt_adc_gain_{chl}', f'txt_adc_offset_{chl}', f'txt_adc_phase_{chl}',
                     f'txt_dac_gain_{chl}', f'txt_dac_offset_{chl}', f'txt_dac_phase_{chl}']
            params = [f'ADC{chl}增益', f'ADC{chl}偏置', f'ADC{chl}相位',
                      f'DAC{chl}增益', f'DAC{chl}偏置', f'DAC{chl}相位']
            for edit, param in zip(edits, params):
                _func(self.qmc_config_ui, edit, param)

    def link_qmc_config_ui(self):
        def _func(_ui, edit_name, param_name):
            txt: QtWidgets.QLineEdit = getattr(_ui, edit_name)
            txt.editingFinished.connect(self.change_param(param_name, txt))

        for chl in range(8):
            edits = [f'txt_adc_gain_{chl}', f'txt_adc_offset_{chl}', f'txt_adc_phase_{chl}',
                     f'txt_dac_gain_{chl}', f'txt_dac_offset_{chl}', f'txt_dac_phase_{chl}']
            params = [f'ADC{chl}增益', f'ADC{chl}偏置', f'ADC{chl}相位',
                      f'DAC{chl}增益', f'DAC{chl}偏置', f'DAC{chl}相位']
            for edit, param in zip(edits, params):
                _func(self.qmc_config_ui, edit, param)

    def show_wave_file_ui(self):
        for dds in range(8):
            file_name_label: QtWidgets.QLabel = getattr(self.wave_file_config_ui, f'file_name_label_{dds}')
            file_name_label.setText(self.icd_param.get_param(f'通道{dds}文件路径', '', str))

    def link_wave_file_ui(self):

        # 双击文件名清空
        def mouseDoubleClickEvent(label, _dds):
            def _func(e):
                label.setText('')
                self.icd_param.set_param(f'通道{_dds}文件路径', '', str)
            return _func

        for dds in range(8):
            file_name_label: QtWidgets.QLabel = getattr(self.wave_file_config_ui, f'file_name_label_{dds}')
            file_name_label.mouseDoubleClickEvent = mouseDoubleClickEvent(file_name_label, dds)
            select_file: QtWidgets.QPushButton = getattr(self.wave_file_config_ui, f'select_file_{dds}')
            select_file.clicked.connect(self.linking_wave_button(dds))

        self.wave_file_config_ui.set_all.clicked.connect(self.linking_wave_button_all())


if __name__ == '__main__':
    import platform

    if platform.system() == 'Windows':
        import ctypes

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("naishu")

    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    jgf = JGFConsole()
    QT_thread = QtCore.QThread()
    qs = QSignal(print_queue)
    qs.txt_trigger.connect(jgf.update_textlog)
    qs.moveToThread(QT_thread)
    QT_thread.started.connect(qs.printLog)
    QT_thread.start()

    us_signal.status_trigger.connect(jgf.show_unload_status)
    printInfo("软件已启动")
    jgf.load_param()

    sys.exit(app.exec_())
