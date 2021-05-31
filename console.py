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
from upload_ctl import UploadCtl, us_signal
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
    _speed_fmt = "速率: {:.2f} MB/s"
    _update_unload_status_interval = 1
    _update_record_status_interval = 1e-3
    _status = 0  # 运行状态

    def __init__(self):
        super().__init__()
        self.ui = ui.Ui_Form()
        self.initUI()

        self.icd_param = icd_parser.ICDParams()

        self.upload_ctl = UploadCtl(self.update_record_status)
        self.selectedlist = np.array([], dtype='u1')  # tableWidget内显示的控件
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

        self.ui.btn_connect.clicked.connect(self.click_connect)
        self.ui.btn_start.clicked.connect(self.click_record)
        self.ui.btn_stop.clicked.connect(self.click_stoprecord)

        self.ui.dds_chose.currentIndexChanged.connect(self.select_dds)

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

        self.checkboxs = self.gen_CheckBox()
        self.lplt = pg.PlotWidget()
        self.ui.grid_graph.addWidget(self.lplt)
        # self.lplt.setYRange(-1.5, 1.5)
        self.lplt.setLabel('top', '回波数据')
        self.plot_color = ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'w']
        self.chk_channels = [self.ui.chk1, self.ui.chk2, self.ui.chk3, self.ui.chk4, self.ui.chk5, self.ui.chk6, self.ui.chk7, self.ui.chk8]
        self.channel_plots = {self.chk_channels[i]: [self.lplt.plot(name=f'chnl{i}'), self.plot_color[i]]
                              for i in range(self.max_channel_count)}
        pg.mkPen()
        self.gui_state(1)
        self.ui.tabWidget.setCurrentIndex(0)
        self.ui.tabWidget.setTabEnabled(1, False)
        self.show()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        # self.close(程序退出)触发
        # self.icd_param.param.pop('DDS_RAM')
        self.icd_param.save_icd()
        if self._status == 2:
            self.click_stopunload()
        elif self._status == 3:
            self.click_stoprecord()

    def gen_CheckBox(self):
        # 创建page_size个CheckBox 在tableWidget使用
        cks = []
        for _ in range(self.page_size):
            ck = QtWidgets.QCheckBox()
            ck.clicked.connect(self.update_checkbox)
            cks.append(ck)
        return cks

    def update_textlog(self, msg):
        try:
            self.ui.textBrowser.moveCursor(QtGui.QTextCursor.End)
            self.ui.textBrowser.insertHtml(msg)
        except Exception as e:
            printException(e)

    def click_connect(self):
        _pg = pgdialog(self, self.upload_ctl.connect, label="系统连接", withcancel=False)
        if _pg.perform():
            self.gui_state(1)
            self.ui.tabWidget.setCurrentIndex(0)
            self.upload_ctl.start_get_record_status()
            printInfo("记录系统连接成功")
        else:
            self.gui_state(0)
            printError(f"记录系统连接失败（{_pg.get_err_msg()}）")

    def click_getlist(self):
        try:
            self.ui.textBrowser.clear()  # 清空消息栏信息
            self.check_all_btn.setText("全选")
            if not pgdialog(self, self._get_file_list, label="获取文件列表", withcancel=False).perform():
                printError("获取文件列表失败")
                return
            self.page.file_list = self.upload_ctl.filelist  # 更新分页参数
            printInfo("获取文件列表成功")
        except Exception as e:
            printException(e)

    def _get_file_list(self, pthread=None):
        try:
            result = self.upload_ctl.get_filelist()
            self.selectedlist = np.zeros(len(self.upload_ctl.filelist), dtype='u1')
        except Exception as e:
            result = False
            printException(e)
        finally:
            pthread.update_state(result)

    def update_table(self, file_list):
        qtable = self.ui.tableWidget
        qtable.setRowCount(self.page_size)
        cur_file_count = len(file_list)
        # 将多出的行隐藏，避免 RuntimeError: wrapped C/C++ object has been deleted
        for i in range(self.page_size):
            if i < cur_file_count:
                info = file_list[i]
                self.checkboxs[i].setChecked(self.selectedlist[self.page.get_current_index() + i])
                qtable.setCellWidget(i, 0, self.checkboxs[i])  # 当setRowCount行数少于之前行时, setCellWidget的Widget将被删除
                qtable.setItem(i, 1, QTableWidgetItem(str(info[0])))
                qtable.setItem(i, 2, QTableWidgetItem(info[1]))
                qtable.setItem(i, 3, QTableWidgetItem(str("{:.2f}".format(info[3] / 1024))))
                qtable.showRow(i)
            else:
                qtable.hideRow(i)

        header = qtable.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        qtable.clearSelection()
        qtable.verticalScrollBar().setSliderPosition(0)  # 设置滚动条位置
        qtable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        qtable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        qtable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Interactive)
        qtable.horizontalHeader().setSectionResizeMode(3, QHeaderView.Interactive)

    def update_checkbox(self):
        # tableWidget内CheckBox状态改变触发
        current_row = self.ui.tableWidget.currentRow()  # 获取table当前行, 从0开始
        # printDebug(self.checkboxs[current_row].isChecked())

        self.selectedlist[self.page.get_current_index() + current_row] = self.checkboxs[current_row].isChecked()

    def click_format(self):
        _pg = pgdialog(self, self.upload_ctl.format, label="系统格式化", withcancel=False)
        if _pg.perform():
            printInfo("系统格式化成功")
        else:
            printError(f"系统格式化失败（{_pg.get_err_msg()}）")

    def click_unload(self):
        # 选中的文件列表
        sel_files = [self.upload_ctl.filelist[index].copy() for index, state in enumerate(self.selectedlist) if state]
        de_interleave = self.ui.chk_unpack.isChecked()  # 解交织
        if not sel_files:
            return
        elif len(sel_files) == 1 and not de_interleave and sel_files[0][3]:
            # 解交织全文件卸载
            total = sel_files[0][3]
            start, ok = QInputDialog.getInt(self, '卸载信息', "请输入起始偏移（0MB~%dMB）" % (total - 1), 0, 0, total - 1, 1)
            if ok is False:
                return
            stop, ok = QInputDialog.getInt(self, '卸载信息', "请输入截止偏移（%dMB~%dMB）" % (start, total), total, start + 1,
                                           total, 1)
            if ok is False:
                return

            if (stop - start) != total:
                start = start - start % 128
                sel_files[0].append(start)
                cut_size = stop - start
                left_size = cut_size % 128
                cut_size = cut_size + 128 - left_size if left_size else cut_size
                if cut_size > total - start:
                    cut_size = total - start
                sel_files[0].append(cut_size)
                sel_files[0][3] = cut_size
                printInfo(f"起始偏移(MB): {start}, 截取(MB): {cut_size}")
            # _weave_length_byte = self.upload_ctl.processor.get_weave_length()
            # if de_interleave and sel_files[0][3] % (_weave_length_byte * sel_files[0][2]):
            #     printError(f"解交织在未来将失败的, 无法整除"
            #                f"(交织长度: {_weave_length_byte}, 采集通道数:{sel_files[0][2]}, 截取的大小:{stop - start}MB)")
            #     return
        for i in sel_files:
            printDebug(f"Id: {i[0]}, file name: {i[1]}, file size: {i[3]}MB")
        is_save = self.ui.chk_save.isChecked()  # 是否存盘
        if is_save:
            filepath = QtWidgets.QFileDialog.getExistingDirectory(self, "请选择导出文件路径", "./")
            if not filepath:
                return
        else:
            filepath = None

        speed = self.ui.label_speed  # 卸载处理速率
        file_process = self.ui.label_file_process  # 卸载文件进度
        label_show = [speed, file_process]
        if self.upload_ctl.start_unload(sel_files, filepath, de_interleave, label_show, finally_call=self.unload_stopped):
            self.gui_state(2)
            self.disable_tab(0)
            printInfo("数据卸载已启动")

    def click_stopunload(self):
        if pgdialog(self, self.upload_ctl.stop_unload, label="卸载停止", withcancel=False).perform():
            self.unload_stopped()
            printInfo("数据卸载已停止")
        else:
            printError("数据卸载停止失败")

    def unload_stopped(self):
        self.gui_state(1)
        self.disable_tab(0, True)
        us_signal.status_trigger.emit([0])

    def show_unload_status(self, status):
        """
            status: state, percent, speed, file_process
            state: 0: unload disable; 1: running; 2: stopped;
        """
        state, *status = status
        if state:
            percent, speed, file_process = status
            if file_process:
                self.ui.label_file_process.setText(file_process)
            if state == 2:
                self.gui_state(1)
            else:
                self.ui.bar_percent.setValue(int(percent))
                self.ui.label_speed.setText(self._speed_fmt.format(speed))
        else:
            self.ui.bar_percent.setValue(0)
            self.ui.label_speed.setText("")
            self.ui.label_file_process.setText("")

    def click_record(self):
        try:
            work_mode = int(self.ui.txt_p2_3.text().strip())    # 工作模式
            sample_chnl_cnt = int(self.ui.txt_p2.text().strip())    # 采样通道数
            sample_count = int(self.ui.txt_p3.text().strip())   # 采样点数
            prf = int(self.ui.txt_p3_3.text().strip())          # PRF
            pretreat = int(self.ui.checkBox.isChecked())        # 预处理使能
        except ValueError as e:
            printError(f"参数输入非纯数字, {e}")
            return
        _pg = pgdialog(self, self.upload_ctl.start_record,
                       args=([work_mode, sample_chnl_cnt, sample_count, prf, pretreat], ),
                       label="采集启动", withcancel=False)
        if _pg.perform():
            self.gui_state(3)
            self.disable_tab(1)
            self.upload_ctl.start_get_record_status()

            self.chk_update(sample_chnl_cnt)
            printInfo("数据记录启动成功")
        else:
            printError(f"数据记录启动失败（{_pg.get_err_msg()}）")

    def click_stoprecord(self):
        _pg = pgdialog(self, self.upload_ctl.stop_record, label="采集停止", withcancel=False)
        if _pg.perform():
            self.gui_state(1)
            self.disable_tab(1, True)
            self.upload_ctl.stop_get_record_status()
            # self.record_status_timer.stop()
            printInfo("数据记录停止成功")
        else:
            printError(f"数据记录停止失败（{_pg.get_err_msg()}）")

    def click_updatecoe(self):
        filename, filetype = QtWidgets.QFileDialog.getOpenFileName(self, "选择待更新因子文件", './', "file(*)")
        if not filename:
            return
        coe_count = int(self.ui.txt_p7.text().strip()) * 1024  # 滤波因子点数
        _pg = pgdialog(self, self.upload_ctl.update_coe, args=(filename, coe_count), label="更新因子", mode=1)
        if _pg.perform():
            printInfo("滤波因子系数更新成功")
        else:
            printError(f"滤波因子系数更新失败（{_pg.get_err_msg()}）")

    def update_record_status(self, event: threading.Event):
        # [self.ui.chk1, self.ui.chk2, self.ui.chk3, self.ui.chk4, self.ui.chk5, self.ui.chk6]
        interval = self._update_record_status_interval
        run_start = time.time()
        event.wait()
        while True:
            sleep(interval - (time.time() - run_start))
            run_start = time.time()
            result, state, graph = self.upload_ctl.record_status()
            if result:
                if state:
                    self.ui.lab_p1.setText(str(state['state']))                 # 记录状态
                    self.ui.lab_p2.setText(str(state['mode']))                  # 工作模式
                    self.ui.lab_p3.setText(str(state['left']) + 'GB')           # 剩余容量
                    self.ui.lab_p4.setText(str(state['bandwidth']) + 'MB/s')    # 记录带宽
                    self.ui.label.setText(f"{state['round_number']: 10}")           # SSD历史读写轮次
                    self.ui.label_3.setText(f"{state['fpga_temperature']: 8}℃")      # FPGA温度
                if graph:
                    channel_number, *graph = graph
                    for index, chk in enumerate(self.enable_chk_channels):
                        plots_info = self.channel_plots[chk]
                        if index + 1 == channel_number and chk.isChecked():
                            plots_info[0].setData(graph, pen=plots_info[1])
                            plots_info[0].show()
                        else:
                            plots_info[0].hide()

    def chk_update(self, count):
        # 通道勾选使能
        self.enable_chk_channels.clear()
        for i, chk in enumerate(self.chk_channels):
            if i < count:
                state = True
                self.enable_chk_channels.append(chk)
            else:
                state = False
            chk.setEnabled(state)

    def select_all(self):
        try:
            if self.check_all_btn.text() == "全选":
                state = True
                status_comment = "取消全选"
            else:
                state = False
                status_comment = "全选"

            self.selectedlist[:] = state
            for i in self.checkboxs:
                i.setChecked(state)

            if len(self.selectedlist):
                self.check_all_btn.setText(status_comment)
        except Exception as e:
            printException(e)

    def gui_state(self, state=1):
        # 未连接状态
        if state == 0:
            self.ui.tabWidget.setEnabled(False)
        # 空闲状态
        elif state == 1:
            self.ui.label_status.setText("空闲状态")
            self.ui.tabWidget.setEnabled(True)
            self.set_btn([True, True, True, True, False, True, False, True])
        # 卸载状态
        elif state == 2:
            self.ui.label_status.setText("卸载状态")
            self.set_btn([False, False, False, False, True, False, False, False])
        # 记录状态
        elif state == 3:
            self.ui.label_status.setText("数据记录状态")
            self.set_btn([False, False, False, False, False, False, True, False])
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

    def disable_tab(self, index, cancel: bool = False):
        """
            非使能tabWidget，控制udp接收只能存在一个
        """
        pass
        # if index:
        #     self.ui.tabWidget.setCurrentIndex(1)
        #     self.ui.tabWidget.setTabEnabled(0, cancel)
        # else:
        #     self.ui.tabWidget.setCurrentIndex(0)
        #     self.ui.tabWidget.setTabEnabled(1, cancel)

    def load_param(self):
        self.icd_param.load_icd()
        self.show_param()

    def show_param(self):
        dds = self.icd_param.get_param('DDS_RAM', 0, int)
        self.ui.dds_chose.setCurrentIndex(dds)
        self.select_dds(dds)
        self.ui.txt_dds_band.setText(self.icd_param.get_param(f'dds{dds}带宽', 100, str))
        self.ui.txt_dds_pulse.setText(self.icd_param.get_param(f'dds{dds}脉宽', 1.1, str))
        self.ui.txt_dds_fc.setText(self.icd_param.get_param(f'dds{dds}中心频率', 0, str))
        self.ui.txt_prf_cyc.setText(self.icd_param.get_param('基准PRF周期', 0, str))
        self.ui.txt_prf_cnt.setText(self.icd_param.get_param('基准PRF数量', 1000, str))
        self.ui.select_clock.setCurrentIndex(int(self.icd_param.get_param('系统参考时钟选择', 0)))
        self.ui.select_adc_sample.setCurrentIndex({1000: 0, 2000: 1, 4000: 2}[self.icd_param.get_param('ADC采样率', 1000)])
        self.ui.txt_adc_noc_f.setText(self.icd_param.get_param('ADC NCO频率', 0, str))
        self.ui.txt_adc_nyq.setText(self.icd_param.get_param('ADC 奈奎斯特区', 1, str))
        self.ui.select_dac_sample.setCurrentIndex({1000: 0, 2000: 1, 4000: 2}[self.icd_param.get_param('DAC采样率', 1000)])
        self.ui.txt_dac_noc_f.setText(self.icd_param.get_param('DAC NCO频率', 0, str))
        self.ui.txt_dac_nyq.setText(self.icd_param.get_param('DAC 奈奎斯特区', 1, str))

        self.ui.select_source.setCurrentIndex(self.icd_param.get_param(f'DAC{dds}播放数据来源', 0, int))
        self.ui.txt_gate_delay.setText(self.icd_param.get_param(f'DAC{dds}播放波门延迟', 2000, str))
        self.ui.txt_gate_width.setText(self.icd_param.get_param(f'DAC{dds}播放波门宽度', 10000, str))
        self.ui.txt_sampling_delay.setText(self.icd_param.get_param(f'ADC{dds}采样延迟', 2000, str))
        self.ui.txt_sampling_points.setText(self.icd_param.get_param(f'ADC{dds}采样点数', 32, str))

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

    def select_dds(self, dds=0):
        self.ui.txt_dds_fc.setText(self.icd_param.get_param(f'dds{dds}中心频率', 0, str))
        self.ui.txt_dds_band.setText(self.icd_param.get_param(f'dds{dds}带宽', 100, str))
        self.ui.txt_dds_pulse.setText(self.icd_param.get_param(f'dds{dds}脉宽', 1.1, str))
        self.ui.select_source.setCurrentIndex(self.icd_param.get_param(f'DAC{dds}播放数据来源', 0, int))
        self.ui.txt_gate_width.setText(self.icd_param.get_param(f'DAC{dds}播放波门宽度', 0, str))
        self.ui.txt_gate_delay.setText(self.icd_param.get_param(f'DAC{dds}播放波门延迟', 0, str))
        self.ui.txt_sampling_delay.setText(self.icd_param.get_param(f'ADC{dds}采样延迟', 0, str))
        self.ui.txt_sampling_points.setText(self.icd_param.get_param(f'ADC{dds}采样点数', 1024, str))

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
