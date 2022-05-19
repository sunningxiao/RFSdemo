import time
from xmlrpc.server import SimpleXMLRPCServer
import numpy as np
from typing import List, Tuple
import waveforms
from threading import Thread
import socketserver
import struct
import pickle

from NS_MCI.tools.printLog import *
from NS_MCI.config import solve_exception, dumps_dict
from NS_MCI.interface import DataNoneInterface, CommandTCPInterface
from NS_MCI import RFSKit
from NS_MCI.xdma import LightDMAMixin
from NS_MCI.config import param_cmd_map
from svqbit import SolveQubit
from quantum_driver.NS_MCI import RPCValueParser


class RFSKitRPCServer(SimpleXMLRPCServer, LightDMAMixin):

    def __init__(self, rfs_addr='192.168.1.175', **kwargs):
        kwargs.update({'allow_none': True})
        super(RFSKitRPCServer, self).__init__(**kwargs)
        CommandTCPInterface._timeout = 10
        CommandTCPInterface._target_id = rfs_addr
        self.rfs_kit = RFSKit(auto_load_icd=True,
                              auto_write_file=False,
                              cmd_interface=CommandTCPInterface,
                              data_interface=DataNoneInterface)
        handle = LightTCPHandler
        handle.rpc_server = self
        self.cmd_server = socketserver.TCPServer(('0.0.0.0', 10800), handle)
        # self.cmd_server.server_bind()
        # self.cmd_server.server_activate()
        self.cmd_thread = Thread(target=self.cmd_server.serve_forever, daemon=True)
        self.cmd_thread.start()
        # self.cmd_server.serve_forever()
        self.qubit_solver = SolveQubit()
        self._setup_dma()

        self.compute_cache = {}
        self.config_params = {}
        self.start_mode = False

    def change_rfs_addr(self, rfs_addr):
        printWarning('更换ip')
        if self.rfs_kit._connected:
            self.rfs_kit.close()
        CommandTCPInterface._timeout = 10
        CommandTCPInterface._target_id = rfs_addr
        self.rfs_kit = RFSKit(auto_load_icd=True,
                              auto_write_file=False,
                              cmd_interface=CommandTCPInterface,
                              data_interface=DataNoneInterface)
        printWarning('ip更换完成')

    @solve_exception
    def rpc_set(self, name, value=0, channel=1, execute=True):
        """
        设置设备属性

        :param name: 属性名
                "Waveform"| "Amplitude" | "Offset"| "Output"
        :param value: 属性值
                "Waveform" --> 1d np.ndarray & -1 <= value <= 1
                "Amplitude"| "Offset"| "Phase" --> float    dB | dB | °
                “PRFNum”   采用内部PRF时，可以通过这个参数控制开启后prf的数量
                "Output" --> bool
        :param channel：通道号
        :param execute: 是否立即生效
        """
        result = True
        channel = channel - 1
        print(f'channel: {channel}')
        value = RPCValueParser.load(value)
        # self.rfs_kit.set_param_value('DAC通道选择', channel)

        if channel < 0:
            raise ValueError('channel超界')

        match name:
            case 'DownLoadTest':
                self._download_da_data()
            case 'Waveform':
                if not isinstance(value, np.ndarray):
                    raise ValueError(f'value类型应为{np.ndarray}, 而不是{type(value)}')
                if value.size > self.da_cache.size//self.da_channel_num:
                    raise ValueError(f'waveform的时间长度超过{self.da_channel_width}s')
                printInfo(f'Waveform配置: {value.shape}_{value.dtype}')
                value, valid_bit = self.qubit_solver.get_valid_bit(value)
                if channel == 8:
                    # self.da_cache[:, :] = 0
                    for i in range(8):
                        self.da_cache[i, :value.size] = value
                        self.padding_dac(i, value.size)
                        self.config_params[f'waveform_{i}'] = value
                        self.rfs_kit.set_param_value(f'BIT移位DAC{i}', valid_bit)
                        # result = self.rfs_kit.execute_command('DAC数据更新', True, value.tobytes())
                else:
                    # channel //= 2
                    # self.da_cache[channel, :] = 0
                    self.da_cache[channel, :value.size] = value
                    self.padding_dac(channel, value.size)
                    self.config_params[f'waveform_{channel}'] = value
                    self.rfs_kit.set_param_value(f'BIT移位DAC{channel}', valid_bit)
                    # result = self.rfs_kit.execute_command('DAC数据更新', True, value.tobytes())
            case 'GenWave':
                if not isinstance(value, waveforms.Waveform):
                    raise ValueError(f'value类型应为{waveforms.Waveform}, 而不是{type(value)}')
                bit = 16
                rate = self.qubit_solver.DArate
                if channel == 8:
                    # self.da_cache[:, :] = 0
                    for i in range(8):
                        if value.start is not None and value.stop is not None:
                            data = value.sample(rate)
                        else:
                            points = self.qubit_solver.dac_points[i]
                            # print(points)
                            time_line = np.linspace(*points)
                            data = value(time_line)
                        data, valid_bit = self.qubit_solver.get_valid_bit(data)
                        self.da_cache[i, :data.size] = data
                        self.padding_dac(i, data.size)
                        self.config_params[f'waveform_{i}'] = data
                        self.rfs_kit.set_param_value(f'BIT移位DAC{i}', valid_bit)
                        # result = self.rfs_kit.execute_command('DAC数据更新', True, data.tobytes())
                else:
                    if value.start is not None and value.stop is not None:
                        data = value.sample(rate)
                    else:
                        points = self.qubit_solver.dac_points[channel]
                        # print(points)
                        time_line = np.linspace(*points)
                        data = value(time_line)
                    if data.size >= self.da_cache.size//self.da_channel_num:
                        raise ValueError(f'waveform的时间长度超过{self.da_channel_width}s')
                    data, valid_bit = self.qubit_solver.get_valid_bit(data)
                    # channel //= 2
                    self.da_cache[channel, :] = 0
                    self.da_cache[channel, :data.size] = data
                    self.config_params[f'waveform_{channel}'] = data
                    self.rfs_kit.set_param_value(f'BIT移位DAC{channel}', valid_bit)
                    # result = self.rfs_kit.execute_command('DAC数据更新', True, data.tobytes())
            case 'GenWaveIQ':
                if not isinstance(value, list) and len(value) == 2 and isinstance(value[0], waveforms.Waveform):
                    raise ValueError(f'value类型应为{[waveforms.Waveform]}, 而不是{type(value)}')
                bit = 16
                rate = self.qubit_solver.DArate
                if channel == 8:
                    for i in range(8):
                        if value[0].start is not None and value[0].stop is not None:
                            I = value[0].sample(self.qubit_solver.DArate)
                            Q = value[1].sample(self.qubit_solver.DArate)
                        else:
                            points = self.qubit_solver.dac_points[i]
                            time_line = np.linspace(*points)
                            I = value[0](time_line)
                            Q = value[1](time_line)

                        data = np.vstack((I, Q)).transpose((1, 0)).reshape(I.size * 2)
                        data = (2 ** (bit - 1) - 1) * data.copy()
                        data = data.astype('int16')
                        self.rfs_kit.set_param_value('DAC通道选择', i)
                        result = self.rfs_kit.execute_command('DAC数据更新', True, data.tobytes())
                else:
                    if value[0].start is not None and value[0].stop is not None:
                        I = value[0].sample(self.qubit_solver.DArate)
                        Q = value[1].sample(self.qubit_solver.DArate)
                    else:
                        points = self.qubit_solver.dac_points[channel]
                        time_line = np.linspace(*points)
                        I = value[0](time_line)
                        Q = value[1](time_line)
                    data = np.vstack((I, Q)).transpose((1, 0)).reshape(I.size * 2)
                    data = (2 ** (bit - 1) - 1) * data.copy()
                    data = data.astype('int16')
                    result = self.rfs_kit.execute_command('DAC数据更新', True, data.tobytes())
            case 'Delay':
                value = round(self.qubit_solver.DArate * value)
                param_name = f'DAC{channel}延迟'
                self.rfs_kit.set_param_value(param_name, value)
                result = self.rfs_kit.execute_command('DAC配置')
                self.config_params[f'{name}_{channel}'] = value
            case 'LinSpace':
                if channel == 8:
                    for i in range(8):
                        self.qubit_solver.dac_points[i] = value
                else:
                    self.qubit_solver.dac_points[channel] = value
            case 'Output':
                if channel == 8:
                    for i in range(8):
                        param_name = f'DAC{i}使能'
                        if value == 'OFF':
                            value = False
                        tmp = 1 if value else 0
                        self.rfs_kit.set_param_value(param_name, tmp)
                else:
                    param_name = f'DAC{channel}使能'
                    if value == 'OFF':
                        value = False
                    tmp = 1 if value else 0
                    self.rfs_kit.set_param_value(param_name, tmp)

            case 'ADrate':
                print(f'AD采样率: {value}')
                self.qubit_solver.ADrate = value
                self.rfs_kit.set_param_value('ADC采样率', value * 1e-6)
                self.config_params[f'{name}'] = value
            case 'DArate':
                print(f'DA采样率: {value}')
                self.qubit_solver.DArate = value
                self.rfs_kit.set_param_value('DAC采样率', value * 1e-6)
                self.config_params[f'{name}'] = value
            case 'KeepAmp':
                self.da_keep_amp = value
                self.config_params[f'{name}'] = value
            case 'Shot':
                print(f'shots: {value}')
                self.rfs_kit.set_param_value('基准PRF数量', value)
                self.qubit_solver.setshots(value)
                self.config_params[f'{name}'] = value
            case 'StartCapture':
                # self.config_params['StartCapture前'] = f'时钟锁定 {self.sig_fpga_clk_online}, ' \
                #                                       f'接收触发数 {self.sig_fpga_trig_count}, ' \
                #                                       f'当前ddr深度 {self.sig_fpga_current_deep}, ' \
                #                                       f'进入ddr数据量 {self.sig_fpga_recv_count}, ' \
                #                                       f'ddr流出数据两 {self.sig_fpga_send_count}'
                self.stop_event.set()
                self.rfs_kit.execute_command('复位')
                if not self.sig_fpga_reset_trig:
                    raise RuntimeError('清空trig计数出错')
                # self.compute_cache.clear()
                self.clear_ad_cache()

                self.stop_event.clear()
                self._download_da_data()
                self.stop_event.set()
                while self.recv_lock.locked():
                    time.sleep(0.1)
                    # raise RuntimeError('上次dma未结束')
                # points = int((self.qubit_solver.pointnum+15)//16*16)
                thread = Thread(target=self._cache_dma_size,
                                args=(self.qubit_solver.pointnum * self.qubit_solver.shots * 4, self._compute_data),
                                daemon=True)
                thread.start()

                # self.config_params['StartCapture后'] = f'时钟锁定 {self.sig_fpga_clk_online}, ' \
                #                                       f'接收触发数 {self.sig_fpga_trig_count}, ' \
                #                                       f'当前ddr深度 {self.sig_fpga_current_deep}, ' \
                #                                       f'进入ddr数据量 {self.sig_fpga_recv_count}, ' \
                #                                       f'ddr流出数据两 {self.sig_fpga_send_count}'
            case 'FrequencyList':
                print(f'FrequencyList: {value}')
                if channel == 8:
                    for i in range(8):
                        self.qubit_solver.setfreqlist(value, i)
                        self.config_params[f'{name}_{i}'] = value
                else:
                    self.qubit_solver.setfreqlist(value, channel)
                    self.config_params[f'{name}_{channel}'] = value
            case 'PhaseList':
                print(f'PhaseList: {value}')
                if channel == 8:
                    for i in range(8):
                        self.qubit_solver.setphaselist(value, i)
                        self.config_params[f'{name}_{i}'] = value
                else:
                    self.qubit_solver.setphaselist(value, channel)
                    self.config_params[f'{name}_{channel}'] = value
            case 'PointNumber':
                print(f'PointNumber: {value}')
                if channel == 8:
                    for i in range(8):
                        param_name = f'ADC{i}门宽'
                        self.rfs_kit.set_param_value(param_name, value)
                        result = self.rfs_kit.execute_command('ADC配置')
                        self.config_params[f'{name}_{i}'] = value
                else:
                    param_name = f'ADC{0}门宽'
                    self.rfs_kit.set_param_value(param_name, value)
                    result = self.rfs_kit.execute_command('ADC配置')
                    self.config_params[f'{name}_{channel}'] = value
                # 转为16ns倍数对应的点数
                self.qubit_solver.setpointnum(int((value + 63) // 64 * 64), channel)
            case 'DemodulationParam':
                print(f'DemodulationParam: {value}')
                if channel == 8:
                    for i in range(8):
                        self.qubit_solver.cofflist[i] = value
                        self.config_params[f'{name}_{i}'] = value
                else:
                    self.qubit_solver.cofflist[channel] = value
                    self.config_params[f'{name}_{channel}'] = value
                result = self.rpc_set('PointNumber', value.shape[1], channel + 1, execute)

            case 'Reset':
                result = self.rfs_kit.execute_command('复位')
            case 'MixMode':
                self.rfs_kit.set_param_value('DAC 奈奎斯特区', value)
                self.config_params[f'{name}'] = value
                if execute:
                    result = self.rfs_kit.execute_command('初始化')
            case 'RefClock':
                tmp = 4
                pll_frq = 125
                self.start_mode = True
                if value == 'out':
                    tmp = 3
                    pll_frq = 250
                    self.start_mode = False
                print(f'pll_frq: {pll_frq}')
                print(f'RefClock: {value}')
                self.rfs_kit.set_param_value('PLL参考时钟频率', pll_frq)
                self.rfs_kit.set_param_value('系统参考时钟选择', tmp)
                self.config_params[f'{name}'] = value
                if execute:
                    result = self.rfs_kit.execute_command('初始化')
            case 'TriggerDelay':
                print(f'TriggerDelay_time: {value}')
                value = round(self.qubit_solver.ADrate * value)
                print(f'TriggerDelay: {value}')
                if channel == 8:
                    for i in range(8):
                        param_name = f'ADC{i}延迟'
                        self.rfs_kit.set_param_value(param_name, value)
                        result = self.rfs_kit.execute_command('ADC配置')
                        self.config_params[f'{name}_{i}'] = value
                else:
                    param_name = f'ADC{channel}延迟'
                    self.rfs_kit.set_param_value(param_name, value)
                    result = self.rfs_kit.execute_command('ADC配置')
                    self.config_params[f'{name}_{channel}'] = value

            case 'GenerateTrig':
                printInfo('内部触发开启')
                self.rfs_kit.set_param_value('基准PRF周期', value)
                self.rfs_kit.set_param_value('基准PRF数量', self.qubit_solver.shots)
                if execute:
                    result = self.rfs_kit.execute_command('内部PRF产生')

                # def __test():
                #     self.config_params['GenerateTrig后'] = {
                #         '时钟锁定': [],
                #         '接收触发数': [],
                #         '当前ddr深度': [],
                #         '进入ddr数据量': [],
                #         'ddr流出数据量': []
                #     }
                #     printInfo('查询线程启动')
                #     _i = 0
                #     while _i <= 10 and not self.stop_event.is_set():
                #         self.config_params['GenerateTrig后']['时钟锁定'].append(self.sig_fpga_clk_online)
                #         self.config_params['GenerateTrig后']['接收触发数'].append(self.sig_fpga_trig_count)
                #         self.config_params['GenerateTrig后']['当前ddr深度'].append(self.sig_fpga_current_deep)
                #         self.config_params['GenerateTrig后']['进入ddr数据量'].append(self.sig_fpga_recv_count)
                #         self.config_params['GenerateTrig后']['ddr流出数据量'].append(self.sig_fpga_send_count)
                #         _i += 1
                # thread = Thread(target=__test, daemon=True)
                # thread.start()
            case _:
                # 参数名透传，直接根据icd.json中的参数名配置对应值
                # 如果在param_cmd_map中找到了对应参数配置后要执行的指令，则执行相应指令
                self.rfs_kit.set_param_value(name, value)
                for params, cmd in param_cmd_map.items():
                    if name in params and execute:
                        result = self.rfs_kit.execute_command(cmd)

        return result

    @solve_exception
    def rpc_get(self, name, channel=1, value=0):
        """
        查询设备属性，获取数据

        """
        channel = channel - 1
        print(f'channel: {channel}')
        if name == 'TraceIQ':
            # 返回快视数据
            self.rfs_kit.set_param_value('获取内容', 0)
            return self.fast_adc_data(channel, False)
        elif name == 'IQ':
            self.rfs_kit.set_param_value('获取内容', 1)
            return self.fast_adc_data(channel, True, value)
        elif name == 'CPUIQ':
            return self.get_adc_data(channel, True, value)

        elif name == 'Amplitude':
            param_name = f'DAC{channel}增益'
            return self.rfs_kit.get_param_value(param_name)
        elif name == 'Offset':
            param_name = f'DAC{channel}偏置'
            return self.rfs_kit.get_param_value(param_name)
        elif name == 'Phase':
            param_name = f'DAC{channel}相位'
            return self.rfs_kit.get_param_value(param_name)
        else:
            return self.rfs_kit.get_param_value(name)

    def get_all_status(self):
        """
        获取后台所有状态信息

        :return:
        """
        _string = [f'-------固件版本: {self.sig_fpga_frame_version}-------',
                   f'RFS在位: {self.rfs_kit._connected}', f'参考时钟来源: {self.sig_fpga_clk_from}',
                   f'参考时钟锁定: {self.sig_fpga_clk_online}', f'上次开启后接收触发数: {self.sig_fpga_trig_count}']
        config_params = dumps_dict(self.config_params)
        _string.append(config_params)
        return '\n'.join(_string)

    @solve_exception
    def get_debug_status(self, param):
        """
        获取后台参数

        :param param:
        :return:
        """
        return self.config_params.get(param, None)

    @solve_exception
    def fast_adc_data(self, channel=0, solve=True, no_complex=0):
        printInfo('获取数据')
        if self.recv_lock.acquire(timeout=3):
            self.recv_lock.release()
        else:
            trig_count = self.sig_fpga_trig_count
            if not self.rfs_kit._connected:
                raise RuntimeError('异常: 板卡不在位，请重新open设备')
            elif self.sig_fpga_clk_online == '未锁定':
                raise RuntimeError(f'异常: 无时钟信号输入, 当前时钟来源 {self.sig_fpga_clk_from}')
            elif trig_count == 0:
                raise RuntimeError(f'异常: 无触发信号接入, 当前时钟来源 {self.sig_fpga_clk_from}')
            elif trig_count != self.qubit_solver.shots:
                raise RuntimeError(f'异常: 接收shots不全, 当前已接收 {self.sig_fpga_trig_count}')
            else:
                raise RuntimeError(f'异常: DA采集数据溢出，请检查触发信号是否过快 \n'
                                   f'当前ddr深度 {self.sig_fpga_current_deep}\n'
                                   f'进入ddr数据量 {self.sig_fpga_recv_count}\n'
                                   f'ddr流出数据两 {self.sig_fpga_send_count}')
            # return RPCValueParser.dump(np.array([]))
        if solve:
            data = self.compute_cache[channel][1]
            if data.size == 0:
                raise RuntimeError(f'异常: 通道{channel} 硬解失败，没有有效的硬解参数或频点列表')
        else:
            data = self.compute_cache[channel][0]
        return RPCValueParser.dump(data)

    @solve_exception
    def get_adc_data(self, channel=0, solve=True, no_complex=0) -> Tuple[bytes, str, Tuple]:
        """
        通过pcie获取数据

        :param channel:
        :param solve:
        :param no_complex
        :return:
        """
        printInfo('获取数据')
        if self.recv_lock.acquire(timeout=3):
            self.recv_lock.release()
        else:
            printWarning('未获取完成')
            return RPCValueParser.dump(np.array([]))
        _data = self.ad_data
        if _data.size * 2 < self.qubit_solver.pointnum * 8:
            printWarning('数据不足一包')
            return RPCValueParser.dump(np.array([]))
        data: np.ndarray = np.frombuffer(_data, dtype='int16')
        assert data.size == self.qubit_solver.pointnum * 8 * self.qubit_solver.shots, '数据长度不足'
        data = data.reshape((self.qubit_solver.shots, 8, self.qubit_solver.pointnum))
        data = data[:, channel, :].reshape((self.qubit_solver.shots, self.qubit_solver.pointnum))
        if solve:
            try:
                data = self.qubit_solver.calculateCPU(data, channel, bool(no_complex))
            except Exception as e:
                printException(e)
                printWarning('硬解失败')
        return RPCValueParser.dump(data)

    def _compute_data(self):
        _data = self.ad_data
        # np.save('adc.npy', _data)
        if _data.size * 2 < self.qubit_solver.pointnum * 8:
            # if _data.size < (self.qubit_solver.pointnum*2+256)*8:
            printWarning('数据不足一包')
            return RPCValueParser.dump(np.array([]))
        data: np.ndarray = np.frombuffer(_data, dtype='int16')
        assert data.size == self.qubit_solver.pointnum * 8 * self.qubit_solver.shots, '数据长度不足'
        data = data.reshape((self.qubit_solver.shots, 8, self.qubit_solver.pointnum))
        for i in range(8):
            channel_data = data[:, i, :].reshape((self.qubit_solver.shots, self.qubit_solver.pointnum))
            channel_solve = self.qubit_solver.calculate_matrix(channel_data, i, False)
            self.compute_cache[i] = [channel_data, channel_solve]

    def execute_command(self, button_name: str,
                        need_feedback=True, file_name=None, check_feedback=True,
                        callback=lambda *args: True, wait: int = 0):
        if button_name in ['初始化', 'ADC配置']:
            self.clear_ad_cache()
        if button_name in ['内部PRF产生']:
            a = self.rfs_kit.get_param_value('基准PRF周期')
            b = self.rfs_kit.get_param_value('基准PRF数量')
            self.has_data_flag += 1
        return self.rfs_kit.execute_command(button_name, need_feedback, file_name, check_feedback, callback, wait)

    def __del__(self):
        self.cmd_server.shutdown()


class LightTCPHandler(socketserver.StreamRequestHandler):
    rpc_server: RFSKitRPCServer = None

    def handle(self):
        head = self.rfile.read(16)
        head = struct.unpack('=IIII', head)
        match head:
            case (0x5F5F5F5F, 0x32000001, _id, _length):
                printInfo('-------接收指令rpc_set--------')
                param = pickle.loads(self.rfile.read(_length - 16))
                try:
                    data = self.rpc_server.rpc_set(*param)
                    error = 0
                except Exception as e:
                    data = str(e)
                    error = 1
                data = pickle.dumps(data)
                head = struct.pack('=IIIII', *[0xCFCFCFCF, 0x32000001, 0, 20 + len(data), error])
                self.wfile.write(head)
                self.wfile.write(data)
                printInfo('-------rpc_set反馈完成-------')
            case (0x5F5F5F5F, 0x32000002, _id, _length):
                printInfo('-------接收指令rpc_get-------')
                param = pickle.loads(self.rfile.read(_length - 16))
                try:
                    data = self.rpc_server.rpc_get(*param)
                    error = 0
                except Exception as e:
                    data = str(e)
                    error = 1
                data = pickle.dumps(data)
                head = struct.pack('=IIIII', *[0xCFCFCFCF, 0x32000002, 0, 20 + len(data), error])
                self.wfile.write(head)
                self.wfile.write(data)
                printInfo('-------rpc_get反馈完成-------')
            case (0x5F5F5F5F, 0x32000003, _id, _length):
                printInfo('-------接收指令get_debug_status-------')
                param = pickle.loads(self.rfile.read(_length - 16))
                try:
                    data = self.rpc_server.get_debug_status(*param)
                    error = 0
                except Exception as e:
                    data = str(e)
                    error = 1
                data = pickle.dumps(data)
                head = struct.pack('=IIIII', *[0xCFCFCFCF, 0x32000003, 0, 20 + len(data), error])
                self.wfile.write(head)
                self.wfile.write(data)
                printInfo('-------get_debug_status反馈完成-------')
            case _:
                printWarning('错误的FastRPC指令包头')


if __name__ == '__main__':
    import sys

    with RFSKitRPCServer(rfs_addr='192.168.1.176', addr=("0.0.0.0", 10801), use_builtin_types=True) as server:
        server.register_instance(server.rfs_kit, allow_dotted_names=True)
        server.register_function(server.change_rfs_addr)

        server.register_function(server.get_adc_data)
        server.register_function(server.clear_ad_cache)
        server.register_function(server.init_dma)
        server.register_function(server.release_dma)

        server.register_function(server.rpc_set)
        server.register_function(server.rpc_get)
        server.register_function(server.get_all_status)
        server.register_function(server.execute_command)
        server.register_function(lambda: None, name='close')

        server.register_multicall_functions()
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            sys.exit(0)
