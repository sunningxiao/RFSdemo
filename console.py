#! /usr/bin/python3
# -*- coding:utf-8 -*-

import sys
import time
import numpy as np
import threading
import qdarkstyle
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg

# import ui.ui as ui
import ui.CTYui as ui
from printLog import *
import icd_parser
from pgdialog import pgdialog
from data_solve import us_signal
from utils import Page, sleep


class QSignal(QtCore.QObject):
    txt_trigger = QtCore.pyqtSignal(str)

    def __init__(self, queue, *args, **kwargs):
        QtCore.QObject.__init__(self, *args, **kwargs)
        self.queue = queue

    def printLog(self):
        while True:
            text = self.queue.get()
            self.txt_trigger.emit(text)


class JGFConsole(QtWidgets.QWidget):
    max_channel_count = 6
    page_size = 50
    _speed_fmt = "传输速率: {:.2f} MB/s"
    _save_speed_fmt = "存储速率: {:.2f} MB/s"
    _update_unload_status_interval = 1
    _update_record_status_interval = 1e-3
    _status = 0  # 运行状态

    def __init__(self):
        super().__init__()
        self.ui = ui.Ui_Form()
        self.initUI()

        self.icd_param = icd_parser.ICDParams()

        # self.check_all_btn = self.ui.btn_checkall
        # self.page = Page(self.ui, self.page_size, self.update_table)  # 分页
        self.enable_chk_channels = []

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

        self.ui.btn_connect.clicked.connect(self.click_connect)
        self.ui.btn_start.clicked.connect(
            self.linking_button('系统开启', need_feedback=True, need_file=False, callback=self.click_start))
        self.ui.btn_stop.clicked.connect(
            self.linking_button('系统停止', need_feedback=True, need_file=False, callback=self.click_stop))
        self.ui.btn_rf_cfg.clicked.connect(self.linking_button('RF配置', need_feedback=True, need_file=False))
        self.ui.btn_dss_cfg.clicked.connect(self.linking_button('DDS配置', need_feedback=True, need_file=False))
        self.ui.btn_wave.clicked.connect(self.linking_button('波形装载', need_feedback=True, need_file=True))
        self.ui.btn_framwork_up.clicked.connect(self.linking_button('固件更新', need_feedback=True, need_file=True))

        self.ui.dds_chose.currentIndexChanged.connect(self.select_dds)
        self.ui.dds_chose.currentIndexChanged.connect(self.change_param('DDS_RAM', self.ui.dds_chose, int, 'index'))

        # 关联界面参数与json
        self.ui.select_source.currentIndexChanged.connect(self.change_param('DAC0播放数据来源', self.ui.select_source, int, 'index'))
        self.ui.txt_gate_delay.editingFinished.connect(self.change_param('DAC0播放波门延迟', self.ui.txt_gate_delay))
        self.ui.txt_gate_width.editingFinished.connect(self.change_param('DAC0播放波门宽度', self.ui.txt_gate_width))
        self.ui.txt_sampling_delay.editingFinished.connect(self.change_param('ADC0采样延迟', self.ui.txt_sampling_delay))
        self.ui.txt_sampling_points.editingFinished.connect(self.change_param('ADC0采样点数', self.ui.txt_sampling_points))

        self.ui.txt_dds_fc.editingFinished.connect(self.change_param('dds0中心频率', self.ui.txt_dds_fc))
        self.ui.txt_dds_band.editingFinished.connect(self.change_param('dds0带宽', self.ui.txt_dds_band))
        self.ui.txt_dds_pulse.editingFinished.connect(self.change_param('dds0脉宽', self.ui.txt_dds_pulse))

        self.ui.txt_prf_cyc.editingFinished.connect(self.change_param('基准PRF周期', self.ui.txt_prf_cyc))
        self.ui.txt_prf_cnt.editingFinished.connect(self.change_param('基准PRF数量', self.ui.txt_prf_cnt))
        self.ui.select_clock.currentIndexChanged.connect(self.change_param('系统参考时钟选择', self.ui.select_clock, int, 'index'))
        self.ui.select_adc_sample.currentIndexChanged.connect(self.change_param('ADC采样率', self.ui.select_adc_sample, int))
        self.ui.txt_adc_noc_f.editingFinished.connect(self.change_param('ADC NCO频率', self.ui.txt_adc_noc_f))
        self.ui.txt_adc_nyq.editingFinished.connect(self.change_param('ADC 奈奎斯特区', self.ui.txt_adc_nyq, int))
        self.ui.select_dac_sample.currentIndexChanged.connect(self.change_param('DAC采样率', self.ui.select_dac_sample, int))
        self.ui.txt_dac_noc_f.editingFinished.connect(self.change_param('DAC NCO频率', self.ui.txt_dac_noc_f))
        self.ui.txt_dac_nyq.editingFinished.connect(self.change_param('DAC 奈奎斯特区', self.ui.txt_dac_nyq, int))

        self.lplt = pg.PlotWidget()
        self.ui.grid_graph.addWidget(self.lplt)
        # self.lplt.setYRange(-1.5, 1.5)
        self.lplt.setLabel('top', '回波数据')
        self.plot_color = ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'w']
        self.chk_channels = [self.ui.chk1, self.ui.chk2, self.ui.chk3, self.ui.chk4, self.ui.chk5, self.ui.chk6, self.ui.chk7, self.ui.chk8]
        self.channel_plots = {self.chk_channels[i]: [self.lplt.plot(name=f'chnl{i}'), self.plot_color[i]]
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

    def update_textlog(self, msg):
        try:
            self.ui.textBrowser.moveCursor(QtGui.QTextCursor.End)
            self.ui.textBrowser.insertHtml(msg)
        except Exception as e:
            printException(e)

    def click_connect(self):
        _pg = pgdialog(self, self.icd_param.connect, label="系统连接", withcancel=False)
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
        self.icd_param.data_solve.start_solve()
        return True

    def click_stop(self):
        self.gui_state(1)
        self.icd_param.data_solve._stop_flag = True
        return True

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
            self.set_btn([False, False, True, False, False, False, False, False])
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

    def show_param(self):
        dds = self.icd_param.get_param('DDS_RAM', 0, int)
        self.ui.dds_chose.setCurrentIndex(dds)
        self.select_dds(dds)
        self.ui.txt_prf_cyc.setText(self.icd_param.get_param('基准PRF周期', 0, str))
        self.ui.txt_prf_cnt.setText(self.icd_param.get_param('基准PRF数量', 1000, str))
        self.ui.select_clock.setCurrentIndex(int(self.icd_param.get_param('系统参考时钟选择', 0)))
        self.ui.select_adc_sample.setCurrentIndex({1000: 0, 2000: 1, 4000: 2}[self.icd_param.get_param('ADC采样率', 1000)])
        self.ui.txt_adc_noc_f.setText(self.icd_param.get_param('ADC NCO频率', 0, str))
        self.ui.txt_adc_nyq.setText(self.icd_param.get_param('ADC 奈奎斯特区', 1, str))
        self.ui.select_dac_sample.setCurrentIndex({1000: 0, 2000: 1, 4000: 2}[self.icd_param.get_param('DAC采样率', 1000)])
        self.ui.txt_dac_noc_f.setText(self.icd_param.get_param('DAC NCO频率', 0, str))
        self.ui.txt_dac_nyq.setText(self.icd_param.get_param('DAC 奈奎斯特区', 1, str))

        for btn in self.icd_param.command:
            self.ui.select_command.addItem(btn)

    def change_param(self, param_name, param_label: [QtWidgets.QLineEdit, QtWidgets.QComboBox], type_fmt=str, combo_flag='text'):
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

    def linking_button(self, button_name, need_feedback=True, need_file=False, callback=lambda *args: True):
        def _func(*args, **kwargs):
            if need_file:
                filename = QFileDialog.getOpenFileName(self, '请选择文件')[0]
                if filename == '':
                    return
                thread = threading.Thread(target=self.icd_param.send_command,
                                          args=[button_name, need_feedback, filename],
                                          kwargs={'callback': callback})
            else:
                thread = threading.Thread(target=self.icd_param.send_command,
                                          args=[button_name, need_feedback],
                                          kwargs={'callback': callback})
            thread.start()

        return _func

    def linking_auto_button(self):
        btn = self.ui.select_command.currentText()
        self.linking_button(btn, need_feedback=False, need_file=False)()

    def select_dds(self, dds=0):
        self.ui.txt_dds_fc.editingFinished.disconnect()
        self.ui.txt_dds_band.editingFinished.disconnect()
        self.ui.txt_dds_pulse.editingFinished.disconnect()
        self.ui.select_source.currentIndexChanged.disconnect()
        self.ui.txt_gate_delay.editingFinished.disconnect()
        self.ui.txt_gate_width.editingFinished.disconnect()
        self.ui.txt_sampling_delay.editingFinished.disconnect()
        self.ui.txt_sampling_points.editingFinished.disconnect()
        self.ui.txt_dds_fc.editingFinished.connect(self.change_param(f'dds{dds}中心频率', self.ui.txt_dds_fc))
        self.ui.txt_dds_band.editingFinished.connect(self.change_param(f'dds{dds}带宽', self.ui.txt_dds_band))
        self.ui.txt_dds_pulse.editingFinished.connect(self.change_param(f'dds{dds}脉宽', self.ui.txt_dds_pulse))
        self.ui.select_source.currentIndexChanged.connect(
            self.change_param(f'DAC{dds}播放数据来源', self.ui.select_source, int, 'index'))
        self.ui.txt_gate_width.editingFinished.connect(self.change_param(f'DAC{dds}播放波门宽度', self.ui.txt_gate_width))
        self.ui.txt_gate_delay.editingFinished.connect(self.change_param(f'DAC{dds}播放波门延迟', self.ui.txt_gate_delay))
        self.ui.txt_sampling_delay.editingFinished.connect(self.change_param(f'ADC{dds}采样延迟', self.ui.txt_sampling_delay))
        self.ui.txt_sampling_points.editingFinished.connect(self.change_param(f'ADC{dds}采样点数', self.ui.txt_sampling_points))

        self.ui.txt_dds_fc.setText(self.icd_param.get_param(f'dds{dds}中心频率', 0, str))
        self.ui.txt_dds_band.setText(self.icd_param.get_param(f'dds{dds}带宽', 100, str))
        self.ui.txt_dds_pulse.setText(self.icd_param.get_param(f'dds{dds}脉宽', 1.1, str))
        self.ui.select_source.setCurrentIndex(self.icd_param.get_param(f'DAC{dds}播放数据来源', 0, int))
        self.ui.txt_gate_width.setText(self.icd_param.get_param(f'DAC{dds}播放波门宽度', 0, str))
        self.ui.txt_gate_delay.setText(self.icd_param.get_param(f'DAC{dds}播放波门延迟', 0, str))
        self.ui.txt_sampling_delay.setText(self.icd_param.get_param(f'ADC{dds}采样延迟', 0, str))
        self.ui.txt_sampling_points.setText(self.icd_param.get_param(f'ADC{dds}采样点数', 1024, str))


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
