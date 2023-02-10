import threading
import time
import os

from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg

import ui.main_frame as ui
from ui.utils import SerialUIMixin, get_git_version, send_command, save_data_by_timer
from ui.DDS配置 import DDSConfig
from ui.开启工作 import StartConfig
from ui.波形预置 import WaveFileConfig
from ui.频谱显示 import SpectrumScreen
from ui.QMC配置 import QMCConfig
from ui.RF配置 import RFConfig
from ui.连接界面 import LinkSystemUI
from ui.RCM控制 import RCMConfigUI
from ui.core_pack_test import CorePackTestUI

from tools.printLog import *

from core import RFSKit
from core.interface import DataTCPInterface, CommandTCPInterface
from tools.data_unpacking import UnPackage

from widgets.pgdialog import pgdialog

UiVersion = 'v3.0'
get_git_version()

with open(f'{os.path.dirname(os.path.abspath(__file__))}/../VERSION', 'r', encoding='utf-8') as fp:
    UiVersion = fp.read()


class RFSControl(QtWidgets.QWidget, SerialUIMixin):
    status_trigger = QtCore.pyqtSignal(object)

    max_channel_count = 8
    page_size = 50
    _speed_fmt = "传输速率: {:.2f} MB/s"
    _save_speed_fmt = "存储速率: {:.2f} MB/s"
    _update_unload_status_interval = 1
    _update_record_status_interval = 1e-3
    # 运行状态
    _status = 0
    _text_line = 0

    def __init__(self):
        super().__init__()
        self.ui = ui.Ui_Form()
        self.dds_config_ui = DDSConfig(self)
        self.start_ui = StartConfig(self)
        self.wave_file_config_ui = WaveFileConfig(self)
        self.spectrum_screen = SpectrumScreen(self)
        self.qmc_config_ui = QMCConfig(self)
        self.rf_config_ui = RFConfig(self)
        self.link_system_ui = LinkSystemUI(self)
        self.rcm_config_ui = RCMConfigUI(self)
        self.core_pack_ui = CorePackTestUI(self)

        self.enable_chk_channels = []
        self.slave_rfs = []
        self.status_timer = QtCore.QTimer(self)
        self.status_timer.timeout.connect(self.action_get_status)

        self.status_trigger.connect(self.show_unload_status)
        self.link_system_ui.show()
        self.calibration = False

    def init_system(self, cmd_interface=CommandTCPInterface, data_interface=DataTCPInterface, **kwargs):
        self.rfs_kit = RFSKit(
            cmd_interface=cmd_interface,
            data_interface=data_interface,
            auto_load_icd=True)
        self.initUI()
        self.load_param()

        self.ui.select_link_addr.setCurrentText(cmd_interface._target_id)
        self.ui.select_link_addr.setDisabled(True)

        self.click_connect()

        # 获取其余从机ip
        self.slave_rfs = kwargs.get('addrs', [])

    def initUI(self):
        self.ui.setupUi(self)
        self.init_serial_ui()
        pix = QtGui.QPixmap("static/logo.png")
        self.ui.lab_logo.setPixmap(pix)
        self.ui.lab_logo.setScaledContents(True)

        ico = QtGui.QIcon()
        ico.addPixmap(QtGui.QPixmap('static/logo.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(ico)

        self.ui.select_is_master.setVisible(False)

        self.ui.label_version.setText(UiVersion)

        self.ui.splitter_log.moveSplitter(0, 1)
        self.ui.chk_port_follow_ip.setHidden(True)
        self.ui.btn_connect_com.clicked.connect(self.click_connect_com)
        self.ui.btn_start_calibration.clicked.connect(self.click_start_calibration)

        print_wheel.txt_trigger.connect(self.update_textlog)

        self.ui.select_is_master.currentTextChanged.connect(self.action_is_master_changed)

        # 关联按钮
        self.ui.btn_cail_from_file.clicked.connect(self.core_pack_ui.show)

        self.ui.btn_rf_collaboration.clicked.connect(self.action_click_collaboration)

        self.ui.btn_auto_command.clicked.connect(self.linking_auto_button)

        self.ui.btn_reload_icd.clicked.connect(self.reload_param)

        self.ui.btn_connect.clicked.connect(self.click_connect)

        self.ui.btn_show_spectrum.clicked.connect(self.spectrum_screen.show)

        self.ui.btn_qmc_cfg.clicked.connect(self.qmc_config_ui.show)
        self.qmc_config_ui.btn_config.clicked.connect(
            self.linking_button('QMC配置', need_feedback=True, need_file=False)
        )
        self.link_qmc_config_ui()

        # RCM相关
        self.ui.btn_rcm_cfg.clicked.connect(self.rcm_config_ui.show)
        self.rcm_config_ui.link_rcm_config_ui()

        self.ui.btn_start.clicked.connect(self.start_ui.show)
        self.start_ui.btn_config.clicked.connect(
            self.linking_button('系统开启', need_feedback=True, need_file=False,
                                callback=lambda: self.status_trigger.emit((1, 3, self.click_start))))
        self.link_start_ui()

        self.ui.btn_stop.clicked.connect(
            self.linking_button('系统停止', need_feedback=True, need_file=False,
                                callback=lambda: self.status_trigger.emit((1, 3, self.click_stop))))

        # 多机RF配置
        self.ui.btn_rf_cfg.clicked.connect(self.rf_config_ui.show)
        self.rf_config_ui.btn_master_clock_cfg.clicked.connect(lambda: self.rfs_kit.set_param_value('RF指令ID', 0x31000010))
        self.rf_config_ui.btn_master_clock_cfg.clicked.connect(self.linking_button('RF配置', need_feedback=True, need_file=False))

        self.rf_config_ui.btn_slave_clock_cfg.clicked.connect(lambda: self.rfs_kit.set_param_value('RF指令ID', 0x31000011))
        self.rf_config_ui.btn_slave_clock_cfg.clicked.connect(
            self.linking_button('RF配置', need_feedback=True, need_file=False))

        self.rf_config_ui.btn_master_clock_sync.clicked.connect(lambda: self.rfs_kit.set_param_value('RF指令ID', 0x31000012))
        self.rf_config_ui.btn_master_clock_sync.clicked.connect(
            self.linking_button('RF配置', need_feedback=True, need_file=False))

        self.rf_config_ui.btn_slave_clock_sync.clicked.connect(lambda: self.rfs_kit.set_param_value('RF指令ID', 0x31000013))
        self.rf_config_ui.btn_slave_clock_sync.clicked.connect(
            self.linking_button('RF配置', need_feedback=True, need_file=False))

        self.rf_config_ui.btn_sysref_gen.clicked.connect(lambda: self.rfs_kit.set_param_value('RF指令ID', 0x31000014))
        self.rf_config_ui.btn_sysref_gen.clicked.connect(
            self.linking_button('RF配置', need_feedback=True, need_file=False))

        self.rf_config_ui.btn_master_rf_config.clicked.connect(lambda: self.rfs_kit.set_param_value('RF指令ID', 0x31000003))
        self.rf_config_ui.btn_master_rf_config.clicked.connect(
            self.linking_button('RF配置', need_feedback=True, need_file=False))

        self.rf_config_ui.btn_slave_rf_config.clicked.connect(lambda: self.rfs_kit.set_param_value('RF指令ID', 0x31000003))
        self.rf_config_ui.btn_slave_rf_config.clicked.connect(
            self.linking_button('RF配置', need_feedback=True, need_file=False))
        # self.ui.btn_rf_cfg.clicked.connect(self.linking_button('RF配置', need_feedback=True, need_file=False))

        # dds相关的输入关联
        self.ui.btn_dss_cfg.clicked.connect(self.dds_config_ui.show)
        self.dds_config_ui.btn_config.clicked.connect(
            self.linking_button('DDS配置', need_feedback=True, need_file=False,
                                callback=lambda: self.status_trigger.emit((1, 3, self.dds_config_ui.close))))
        self.link_dds_config_ui()

        self.ui.btn_wave.clicked.connect(self.wave_file_config_ui.show)
        self.wave_file_config_ui.btn_config.clicked.connect(self.click_wave)
        self.link_wave_file_ui()
        # self.ui.btn_wave.clicked.connect(self.linking_button('波形装载', need_feedback=True, need_file=True))
        self.ui.btn_framwork_up.clicked.connect(
            self.linking_button('固件更新', need_feedback=True, need_file=True, wait=20)
        )
        self.ui.btn_clock_up.clicked.connect(
            self.linking_button('时钟校准', need_feedback=True, need_file=True, wait=20)
        )
        # 关联界面参数与json
        self.ui.select_clock.currentIndexChanged.connect(
            self.change_param('系统参考时钟选择', self.ui.select_clock, int, 'index'))
        self.ui.txt_adc_sample.editingFinished.connect(
            self.change_param('ADC采样率', self.ui.txt_adc_sample, int))
        self.ui.txt_adc_extract.editingFinished.connect(
            self.change_param('ADC 抽取倍数', self.ui.txt_adc_extract, int))
        self.ui.txt_adc_noc_f.editingFinished.connect(self.change_param('ADC NCO频率', self.ui.txt_adc_noc_f))
        self.ui.txt_adc_nyq.editingFinished.connect(self.change_param('ADC 奈奎斯特区', self.ui.txt_adc_nyq, int))
        self.ui.txt_dac_sample.editingFinished.connect(
            self.change_param('DAC采样率', self.ui.txt_dac_sample, int))
        self.ui.txt_dac_extract.editingFinished.connect(
            self.change_param('DAC 抽取倍数', self.ui.txt_dac_extract, int))
        self.ui.txt_dac_noc_f.editingFinished.connect(self.change_param('DAC NCO频率', self.ui.txt_dac_noc_f))
        self.ui.txt_dac_nyq.editingFinished.connect(self.change_param('DAC 奈奎斯特区', self.ui.txt_dac_nyq, int))
        self.ui.txt_pll_f.editingFinished.connect(self.change_param('PLL参考时钟频率', self.ui.txt_pll_f, int))
        self.ui.chk_pll_adc.stateChanged.connect(self.change_param('ADC PLL使能', self.ui.chk_pll_adc, int))
        self.ui.chk_pll_dac.stateChanged.connect(self.change_param('DAC PLL使能', self.ui.chk_pll_dac, int))

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
        # self.ui.tabWidget.setTabEnabled(1, False)
        # self.show()
        self.core_pack_ui.show()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        # self.close(程序退出)触发
        # self.rfs_kit.param.pop('DDS_RAM')
        self._serial_stop_event.set()
        self.rfs_kit.save_icd()
        self.rfs_kit.close()
        if self._status == 2:
            # 判断状态，发送停止指令
            self.linking_button('系统停止', need_feedback=False, need_file=False)()

    def click_connect_com(self):
        port = self.ui.select_com_id.currentText()
        baud = self.ui.select_com_baud_rate.currentText()
        check_sum = self.ui.select_com_checksum.currentText()
        byte_size = self.ui.select_com_data_bit.currentText()
        stop_bit = self.ui.select_com_stop_bit.currentText()
        stream_str = self.ui.select_com_stream.currentText()
        self.connect_com(port, baud, check_sum, byte_size, stop_bit, stream_str)

    def click_start_calibration(self):
        if self.calibration == False:
            self.calibration = True
            self.ui.btn_start_calibration.setStyleSheet("background-color: rgb(255, 0, 0);")
        else:
            self.calibration = False
            self.ui.btn_start_calibration.setStyleSheet("background-color: None;")

    def update_textlog(self, msg):
        try:
            if self._text_line >= 5000:
                self.ui.textBrowser.clear()
                self._text_line = 0
            self.ui.textBrowser.moveCursor(QtGui.QTextCursor.End)
            self.ui.textBrowser.insertHtml(msg)
            self._text_line += 1
        except Exception as e:
            printException(e)

    def wrap_start_command(self, *args, pthread=None):
        if pthread:
            res = self.rfs_kit.start_command(*args)
            pthread.update_state(res)
        else:
            return self.rfs_kit.start_command(*args)

    def click_connect(self):
        # ip = self.ui.select_link_addr.currentText()
        # follow = self.ui.chk_port_follow_ip.isChecked()
        _pg = pgdialog(self, self.wrap_start_command, label="系统连接", withcancel=False, mode=0)
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
        ip = self.ui.select_link_addr.currentText()
        split_time = self.ui.txt_split_file_step.text()
        if not self.ui.chk_write_file.isChecked():
            self.rfs_kit.start_stream(auto_write_file=True,
                                      write_file=False,
                                      file_name=ip.split('.')[3])
        elif split_time in {'', 'inf', '0', None}:
            path_id = 1
            rfs_ip = ip.split('.')[3]
            while os.path.exists(f'{path_id}_{rfs_ip}'):
                path_id += 1
            file_name = f'{path_id}_{rfs_ip}'
            self.rfs_kit.start_stream(auto_write_file=True,
                                      write_file=self.ui.chk_write_file.isChecked(),
                                      file_name=file_name)
        else:
            self.rfs_kit.start_stream(auto_write_file=False)
            try:
                split_time = float(split_time)
            except ValueError as e:
                split_time = 1
            package_num = split_time // (self.rfs_kit.get_param_value('基准PRF周期', 1e6, float) * 1e-9)
            _thread = threading.Thread(
                target=save_data_by_timer,
                args=(self.rfs_kit, package_num),
                daemon=True
            )
            _thread.start()

        self.start_ui.close()
        self.status_timer.start(1000)

        def _func():
            while self._status == 2:
                data = self.rfs_kit.view_stream_data()
                data = UnPackage.solve_source_data(data, [True]*16, 16384)
                if data:
                    self.status_trigger.emit([1, 2, data])
                    time.sleep(1)

        _thread = threading.Thread(target=_func, daemon=True)
        _thread.start()
        return True

    def click_stop(self):
        self.gui_state(1)
        self.rfs_kit.stop_stream()
        # self.rfs_kit.data_server.close_recv()
        self.status_timer.stop()
        self.show_unload_status([0, 0])
        return True

    def click_wave(self):
        def _func():
            chl = self.rfs_kit.get_param_value('DDS_RAM')
            try:
                for dds in range(8):
                    self.rfs_kit.set_param_value('DDS_RAM', dds)
                    filename = self.rfs_kit.get_param_value(f'通道{dds}文件路径', '', str)
                    if filename != '':
                        assert self.rfs_kit.execute_command('波形装载', file_name=filename)
                        printColor(f'通道{dds+1}波形装载完成', 'blue')
            except:
                printWarning('波形装载失败')
            finally:
                self.rfs_kit.set_param_value('DDS_RAM', chl)
                self.status_trigger.emit((1, 3, self.wave_file_config_ui.close))
                # self.wave_file_config_ui.close()

        thread = threading.Thread(target=_func, daemon=True)
        thread.start()

    def show_unpack(self, data):
        """每次解包成功后都会调用此方法

        :param data: 解包后的数据，data结构为

        :return:
        """
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
                self.rfs_kit.save_icd(status[1])
        else:
            self.ui.label.setText(self._speed_fmt.format(0))
            self.ui.label_3.setText(self._save_speed_fmt.format(0))

    def action_get_status(self):
        status = self.rfs_kit.upload_status()
        self.show_unload_status([1, 0, status[0]])
        self.show_unload_status([1, 1, status[1]])

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
            self.set_btn([True, False, True, False, False, True, False, True])
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
        # self.rfs_kit.load_icd()
        self.show_param()
        # self.ui.select_link_addr.addItem(self.rfs_kit.icd_data['remote_ip'])
        # self.rfs_kit.start_data_server()

    def reload_param(self):
        self.rfs_kit.load_icd(reload=True)
        self.show_param()

    def show_param(self):
        self.action_is_master_changed('主机' if int(self.rfs_kit.get_param_value('脱机工作', 0)) == 0 else '单机')
        self.ui.select_clock.setCurrentIndex(int(self.rfs_kit.get_param_value('系统参考时钟选择', 0)))
        self.ui.txt_adc_sample.setText(self.rfs_kit.get_param_value('ADC采样率', 1000, str))
        self.ui.txt_adc_extract.setText(self.rfs_kit.get_param_value('ADC 抽取倍数', 1, str))
        self.ui.txt_adc_noc_f.setText(self.rfs_kit.get_param_value('ADC NCO频率', 0, str))
        self.ui.txt_adc_nyq.setText(self.rfs_kit.get_param_value('ADC 奈奎斯特区', 1, str))
        self.ui.txt_dac_sample.setText(self.rfs_kit.get_param_value('DAC采样率', 1000, str))
        self.ui.txt_dac_extract.setText(self.rfs_kit.get_param_value('DAC 抽取倍数', 1, str))
        self.ui.txt_dac_noc_f.setText(self.rfs_kit.get_param_value('DAC NCO频率', 0, str))
        self.ui.txt_dac_nyq.setText(self.rfs_kit.get_param_value('DAC 奈奎斯特区', 1, str))
        self.ui.txt_pll_f.setText(self.rfs_kit.get_param_value('PLL参考时钟频率', 250, str))
        self.ui.chk_pll_adc.setChecked(self.rfs_kit.get_param_value('ADC PLL使能', 0, bool))
        self.ui.chk_pll_dac.setChecked(self.rfs_kit.get_param_value('DAC PLL使能', 0, bool))

        self.ui.select_command.clear()
        for btn in self.rfs_kit.icd_param.button:
            self.ui.select_command.addItem(btn)

    def change_param(self, param_name, param_label: [QtWidgets.QLineEdit, QtWidgets.QComboBox], type_fmt=str,
                     combo_flag='text'):
        def _func(*args, **kwargs):
            if isinstance(param_label, QtWidgets.QLineEdit):
                self.rfs_kit.set_param_value(param_name, param_label.text(), type_fmt)
            elif isinstance(param_label, QtWidgets.QComboBox):
                if combo_flag == 'text':
                    self.rfs_kit.set_param_value(param_name, param_label.currentText(), type_fmt)
                elif combo_flag == 'index':
                    self.rfs_kit.set_param_value(param_name, param_label.currentIndex(), type_fmt)
            elif isinstance(param_label, QtWidgets.QCheckBox):
                self.rfs_kit.set_param_value(param_name, int(param_label.isChecked()), type_fmt)
            else:
                printWarning('不受支持的控件类型')

        return _func

    def linking_button(self, button_name, need_feedback=True, check_feedback=True, need_file=False, callback=lambda *args: None,
                       wait: int = 0):
        def _func(*args, **kwargs):
            if need_file:
                filename = QFileDialog.getOpenFileName(self, '请选择文件')[0]
                if filename == '':
                    return
                thread = threading.Thread(target=self.rfs_kit.execute_command,
                                          args=[button_name, need_feedback, filename],
                                          kwargs={'check_feedback': check_feedback, 'callback': callback, 'wait': wait},
                                          daemon=True)
            else:
                thread = threading.Thread(target=self.rfs_kit.execute_command,
                                          args=[button_name, need_feedback],
                                          kwargs={'check_feedback': check_feedback, 'callback': callback, 'wait': wait},
                                          daemon=True)
            thread.start()

        return _func

    def linking_wave_button(self, dds):
        def _func(*args, **kwargs):
            filename = QFileDialog.getOpenFileName(self.wave_file_config_ui, '请选择文件')[0]
            if filename == '':
                return
            file_name_label: QtWidgets.QLabel = getattr(self.wave_file_config_ui, f'file_name_label_{dds}')
            file_name_label.setText(filename)
            self.rfs_kit.set_param_value(f'通道{dds}文件路径', filename, str)

        return _func

    def linking_wave_button_all(self):
        def _func(*args, **kwargs):
            filename = QFileDialog.getOpenFileName(self.wave_file_config_ui, '请选择文件')[0]
            if filename == '':
                return
            for dds in range(8):
                file_name_label: QtWidgets.QLabel = getattr(self.wave_file_config_ui, f'file_name_label_{dds}')
                file_name_label.setText(filename)
                self.rfs_kit.set_param_value(f'通道{dds}文件路径', filename, str)

        return _func

    def linking_auto_button(self):
        btn = self.ui.select_command.currentText()
        self.linking_button(btn, need_feedback=True, check_feedback=False, need_file=False)()

    def show_start_ui(self):
        self.start_ui.select_prf_src.setCurrentIndex(self.rfs_kit.get_param_value('基准PRF来源', 0))
        self.start_ui.txt_prf_cyc.setText(self.rfs_kit.get_param_value('基准PRF周期', 0, str))
        self.start_ui.txt_prf_cnt.setText(self.rfs_kit.get_param_value('基准PRF数量', 1000, str))
        for dds in range(8):
            select_source: QtWidgets.QLineEdit = getattr(self.start_ui, f'select_source_{dds}')
            select_source.setCurrentIndex(self.rfs_kit.get_param_value(f'DAC{dds}播放数据来源', 0, int))
            txt_gate_width: QtWidgets.QLineEdit = getattr(self.start_ui, f'txt_gate_width_{dds}')
            txt_gate_width.setText(self.rfs_kit.get_param_value(f'DAC{dds}播放波门宽度', 0, str))
            txt_gate_delay: QtWidgets.QLineEdit = getattr(self.start_ui, f'txt_gate_delay_{dds}')
            txt_gate_delay.setText(self.rfs_kit.get_param_value(f'DAC{dds}播放波门延迟', 0, str))
            txt_sampling_delay: QtWidgets.QLineEdit = getattr(self.start_ui, f'txt_sampling_delay_{dds}')
            txt_sampling_delay.setText(self.rfs_kit.get_param_value(f'ADC{dds}采样延迟', 0, str))
            txt_sampling_points: QtWidgets.QLineEdit = getattr(self.start_ui, f'txt_sampling_points_{dds}')
            txt_sampling_points.setText(self.rfs_kit.get_param_value(f'ADC{dds}采样点数', 1024, str))

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
            txt.setText(self.rfs_kit.get_param_value(param_name, 0, str))

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

        def _dds_sample(*args, **kwargs):
            dac_sample = self.ui.txt_dac_sample.text()
            multi = self.ui.txt_dac_extract.text()
            dds_sample = int(float(dac_sample)/float(multi))
            self.rfs_kit.set_param_value('DDS采样率', dds_sample)

        for chl in range(8):
            edits = [f'txt_dds_fc_{chl}', f'txt_dds_fc_step_{chl}', f'txt_dds_fc_range_{chl}',
                     f'txt_dds_band_{chl}', f'txt_dds_pulse_{chl}',
                     f'txt_dds_phase_{chl}', f'txt_dds_phase_step_{chl}', f'txt_dds_phase_range_{chl}']
            params = [f'dds{chl}中心频率', f'dds{chl}频率扫描步进', f'dds{chl}频率扫描范围',
                      f'dds{chl}带宽', f'dds{chl}脉宽',
                      f'dds{chl}初始相位', f'dds{chl}相位扫描步进', f'dds{chl}相位扫描范围']
            for edit, param in zip(edits, params):
                _func(self.dds_config_ui, edit, param)

        self.ui.txt_dac_sample.editingFinished.connect(_dds_sample)
        self.ui.txt_dac_extract.editingFinished.connect(_dds_sample)

    def show_qmc_config_ui(self):
        def _func(_ui, edit_name, param_name):
            txt: QtWidgets.QLineEdit = getattr(_ui, edit_name)
            txt.setText(self.rfs_kit.get_param_value(param_name, 0, str))

        for chl in range(8):
            edits = [f'txt_adc_gain_{chl}', f'txt_adc_offset_{chl}', f'txt_adc_phase_{chl}',
                     f'txt_dac_gain_{chl}', f'txt_dac_gain_step_{chl}', f'txt_dac_gain_target_{chl}',
                     f'txt_dac_offset_{chl}', f'txt_dac_phase_{chl}']
            params = [f'ADC{chl}增益', f'ADC{chl}偏置', f'ADC{chl}相位',
                      f'DAC{chl}增益', f'DAC{chl}衰减步进', f'DAC{chl}衰减截止',
                      f'DAC{chl}偏置', f'DAC{chl}相位']
            for edit, param in zip(edits, params):
                _func(self.qmc_config_ui, edit, param)

    def link_qmc_config_ui(self):
        def _func(_ui, edit_name, param_name):
            txt: QtWidgets.QLineEdit = getattr(_ui, edit_name)
            txt.editingFinished.connect(self.change_param(param_name, txt))

        for chl in range(8):
            edits = [f'txt_adc_gain_{chl}', f'txt_adc_offset_{chl}', f'txt_adc_phase_{chl}',
                     f'txt_dac_gain_{chl}', f'txt_dac_gain_step_{chl}', f'txt_dac_gain_target_{chl}',
                     f'txt_dac_offset_{chl}', f'txt_dac_phase_{chl}']
            params = [f'ADC{chl}增益', f'ADC{chl}偏置', f'ADC{chl}相位',
                      f'DAC{chl}增益', f'DAC{chl}衰减步进', f'DAC{chl}衰减截止',
                      f'DAC{chl}偏置', f'DAC{chl}相位']
            for edit, param in zip(edits, params):
                _func(self.qmc_config_ui, edit, param)

    def show_wave_file_ui(self):
        for dds in range(8):
            file_name_label: QtWidgets.QLabel = getattr(self.wave_file_config_ui, f'file_name_label_{dds}')
            file_name_label.setText(self.rfs_kit.get_param_value(f'通道{dds}文件路径', '', str))

    def link_wave_file_ui(self):

        # 双击文件名清空
        def mouseDoubleClickEvent(label, _dds):
            def _func(e):
                label.setText('')
                self.rfs_kit.set_param_value(f'通道{_dds}文件路径', '', str)
            return _func

        for dds in range(8):
            file_name_label: QtWidgets.QLabel = getattr(self.wave_file_config_ui, f'file_name_label_{dds}')
            file_name_label.mouseDoubleClickEvent = mouseDoubleClickEvent(file_name_label, dds)
            select_file: QtWidgets.QPushButton = getattr(self.wave_file_config_ui, f'select_file_{dds}')
            select_file.clicked.connect(self.linking_wave_button(dds))

        self.wave_file_config_ui.set_all.clicked.connect(self.linking_wave_button_all())

    def action_is_master_changed(self, status):
        self.ui.select_is_master.setCurrentText(status)
        self.ui.btn_rf_cfg.clicked.disconnect()

        if status == '单机':
            self.rfs_kit.set_param_value('脱机工作', 1, int)
            self.ui.btn_rf_cfg.clicked.connect(
                lambda: self.rfs_kit.set_param_value('RF指令ID', 0x31000003))
            self.ui.btn_rf_cfg.clicked.connect(self.linking_button('RF配置', need_feedback=True, need_file=False))

        elif status == '从机':
            self.rfs_kit.set_param_value('脱机工作', 0, int)

            self.ui.btn_rf_cfg.clicked.connect(self.rf_config_ui.show)

        elif status == '主机':
            self.rfs_kit.set_param_value('脱机工作', 0, int)

            self.ui.btn_rf_cfg.clicked.connect(self.rf_config_ui.show)

    def action_click_collaboration(self, *args):
        """
        主从协同RF配置

        :param args:
        :return:
        """
        slaves = self.slave_rfs

        def _func():
            self.rfs_kit.set_param_value('RF指令ID', 0x31000010)
            self.rfs_kit.execute_command('RF配置')
            time.sleep(0.5)

            self.rfs_kit.set_param_value('RF指令ID', 0x31000011)
            data = self.rfs_kit.icd_param.fmt_command('RF配置')
            for ip in slaves:
                send_command(ip, 5001, data)
            time.sleep(0.5)

            self.rfs_kit.set_param_value('RF指令ID', 0x31000012)
            self.rfs_kit.execute_command('RF配置')
            time.sleep(0.5)

            self.rfs_kit.set_param_value('RF指令ID', 0x31000013)
            data = self.rfs_kit.icd_param.fmt_command('RF配置')
            for ip in slaves:
                send_command(ip, 5001, data)
            time.sleep(0.5)

            self.rfs_kit.set_param_value('RF指令ID', 0x31000014)
            self.rfs_kit.execute_command('RF配置')
            time.sleep(0.5)

            self.rfs_kit.set_param_value('RF指令ID', 0x31000003)
            data = self.rfs_kit.icd_param.fmt_command('RF配置')
            for ip in slaves:
                send_command(ip, 5001, data)
            time.sleep(0.5)

            self.rfs_kit.set_param_value('RF指令ID', 0x31000003)
            self.rfs_kit.execute_command('RF配置')

        thread = threading.Thread(target=_func, daemon=True)
        thread.start()


def init_ui():
    from core.config import global_application
    import platform

    if platform.system() == 'Windows':
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("naishu")

    if __file__.endswith('.pyc'):
        import pyi_splash
        pyi_splash.close()
    rfs = RFSControl()
    # rfs.link_system_ui.show()
    printInfo("软件已启动")

    return global_application
