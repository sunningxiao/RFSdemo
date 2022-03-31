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
from NS_MCI.config import solve_exception
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
        # self.cmd_server = socketserver.TCPServer(('0.0.0.0', 10800), socketserver.StreamRequestHandler)
        self.qubit_solver = SolveQubit()
        self._setup_dma()

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
        channel = channel - 1
        # print(f'转换前 {name} -> {type(value)} -> {value}')
        value = RPCValueParser.load(value)
        # print(f'转换后 {name} -> {type(value)} -> {value}')

        self.rfs_kit.set_param_value('DAC通道选择', channel)
        if name == 'Waveform':
            if not isinstance(value, np.ndarray):
                raise ValueError(f'value类型应为{np.ndarray}, 而不是{type(value)}')
            bit = 16
            value = (2 ** (bit - 1) - 1) * value
            value = value.astype('int16')
            if channel == 8:
                for i in range(8):
                    self.rfs_kit.set_param_value('DAC通道选择', i)
                    self.rfs_kit.execute_command('DAC数据更新', True, value.tobytes())
            else:
                self.rfs_kit.set_param_value('DAC通道选择', channel)
                self.rfs_kit.execute_command('DAC数据更新', True, value.tobytes())
        elif name == 'GenWave':
            if not isinstance(value, waveforms.Waveform):
                raise ValueError(f'value类型应为{waveforms.Waveform}, 而不是{type(value)}')
            bit = 16
            rate = self.qubit_solver.DArate
            if channel == 8:
                for i in range(8):
                    if value.start is not None and value.stop is not None:
                        data = (2 ** (bit - 1) - 1) * value.sample(self.qubit_solver.DArate)
                    else:
                        points = self.qubit_solver.dac_points[i]
                        # print(points)
                        time_line = np.linspace(*points)
                        data = (2 ** (bit - 1) - 1) * value(time_line)
                    data = data.astype('int16')
                    self.rfs_kit.set_param_value('DAC通道选择', i)
                    self.rfs_kit.execute_command('DAC数据更新', True, data.tobytes())
            else:
                if value.start is not None and value.stop is not None:
                    data = (2 ** (bit - 1) - 1) * value.sample(self.qubit_solver.DArate)
                else:
                    points = self.qubit_solver.dac_points[channel]
                    # print(points)
                    time_line = np.linspace(*points)
                    data = (2 ** (bit - 1) - 1) * value(time_line)
                # if data.size >= 32e-6 * self.qubit_solver.DArate:
                #     raise ValueError(f'波形长度{data.size}超界，当前最大长度')
                data = data.astype('int16')
                self.rfs_kit.execute_command('DAC数据更新', True, data.tobytes())
        elif name == 'GenWaveIQ':
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

                    data = np.vstack((I, Q)).transpose((1, 0)).reshape(I.size*2)
                    data = (2 ** (bit - 1) - 1) * data.copy()
                    data = data.astype('int16')
                    self.rfs_kit.set_param_value('DAC通道选择', i)
                    self.rfs_kit.execute_command('DAC数据更新', True, data.tobytes())
            else:
                if value[0].start is not None and value[0].stop is not None:
                    I = value[0].sample(self.qubit_solver.DArate)
                    Q = value[1].sample(self.qubit_solver.DArate)
                else:
                    points = self.qubit_solver.dac_points[channel]
                    time_line = np.linspace(*points)
                    I = value[0](time_line)
                    Q = value[1](time_line)
                data = np.vstack((I, Q)).transpose((1, 0)).reshape(I.size*2)
                data = (2 ** (bit - 1) - 1) * data.copy()
                data = data.astype('int16')
                self.rfs_kit.execute_command('DAC数据更新', True, data.tobytes())
        elif name == 'Delay':
            param_name = f'DAC{channel}延迟'
            self.rfs_kit.set_param_value(param_name, value)
            self.rfs_kit.execute_command('DAC配置')
        elif name == 'LinSpace':
            if channel == 8:
                for i in range(8):
                    self.qubit_solver.dac_points[i] = value
            else:
                self.qubit_solver.dac_points[channel] = value
        elif name == 'Output':
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

        elif name == 'ADrate':
            self.qubit_solver.ADrate = value
        elif name == 'DArate':
            self.qubit_solver.DArate = value
        elif name == 'Shot':
            self.rfs_kit.set_param_value('基准PRF数量', value)
            self.qubit_solver.setshots(value)
        elif name == 'StartCapture':
            self.stop_event.set()
            self.rfs_kit.execute_command('复位')
            self.clear_ad_cache()
            if self.recv_lock.locked():
                raise RuntimeError('上次dma未结束')
            # points = int((self.qubit_solver.pointnum+15)//16*16)
            thread = Thread(target=self._cache_dma_size, args=(self.qubit_solver.pointnum*self.qubit_solver.shots*4, ), daemon=True)
            thread.start()
            # self._cache_dma_size(self.qubit_solver.pointnum*self.qubit_solver.shots*4)
        elif name == 'FrequencyList':
            if channel == 8:
                for i in range(8):
                    self.qubit_solver.setfreqlist(value, i)
            else:
                self.qubit_solver.setfreqlist(value, channel)
        elif name == 'PointNumber':
            # print(f'PointNumber:{value}')
            if channel == 8:
                for i in range(8):
                    param_name = f'ADC{i}门宽'
                    self.rfs_kit.set_param_value(param_name, value)
                    self.rfs_kit.execute_command('ADC配置')
            else:
                param_name = f'ADC{channel}门宽'
                self.rfs_kit.set_param_value(param_name, value)
                self.rfs_kit.execute_command('ADC配置')
            # 转为16ns倍数对应的点数
            self.qubit_solver.setpointnum(int((value + 63) // 64 * 64))

        elif name == 'Reset':
            self.rfs_kit.execute_command('复位')
        elif name == 'MixMode':
            self.rfs_kit.set_param_value('DAC 奈奎斯特区', value)
            if execute:
                self.rfs_kit.execute_command('初始化')
        elif name == 'RefClock':
            tmp = 4
            pll_frq = 125
            if value == 'out':
                tmp = 3
                pll_frq = 250
            self.rfs_kit.set_param_value('PLL参考时钟频率', pll_frq)
            self.rfs_kit.set_param_value('系统参考时钟选择', tmp)
            if execute:
                self.rfs_kit.execute_command('初始化')
        elif name == 'TriggerDelay':
            if channel == 8:
                for i in range(8):
                    param_name = f'ADC{i}延迟'
                    self.rfs_kit.set_param_value(param_name, value)
                    self.rfs_kit.execute_command('ADC配置')
            else:
                param_name = f'ADC{channel}延迟'
                self.rfs_kit.set_param_value(param_name, value)
                self.rfs_kit.execute_command('ADC配置')

        elif name == 'GenerateTrig':
            self.rfs_kit.set_param_value('基准PRF周期', value)
            self.rfs_kit.set_param_value('基准PRF数量', self.qubit_solver.shots)
            if execute:
                self.rfs_kit.execute_command('内部PRF产生')
        else:
            # 参数名透传，直接根据icd.json中的参数名配置对应值
            # 如果在param_cmd_map中找到了对应参数配置后要执行的指令，则执行相应指令
            self.rfs_kit.set_param_value(name, value)
            for params, cmd in param_cmd_map.items():
                if name in params and execute:
                    self.rfs_kit.execute_command(cmd)

        return True

    @solve_exception
    def rpc_get(self, name, channel=1, value=0):
        """
        查询设备属性，获取数据

        """
        channel = channel - 1
        if name == 'TraceIQ':
            # 返回快视数据
            self.rfs_kit.set_param_value('获取内容', 0)
            return self.get_adc_data(channel, False)
        elif name == 'IQ':
            self.rfs_kit.set_param_value('获取内容', 1)
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

    @solve_exception
    def get_adc_data(self, channel=0, solve=True, no_complex=0) -> Tuple[bytes, str, Tuple]:
        """
        通过pcie获取数据

        :param channel:
        :param solve:
        :param no_complex
        :return:
        """
        if self.recv_lock.acquire(timeout=3):
            self.recv_lock.release()
        else:
            printWarning('未获取完成')
            return RPCValueParser.dump(np.array([]))
        _data = self.ad_data
        # np.save('adc.npy', _data)
        if _data.size*2 < self.qubit_solver.pointnum*8:
        # if _data.size < (self.qubit_solver.pointnum*2+256)*8:
            printWarning('数据不足一包')
            return RPCValueParser.dump(np.array([]))
        # data = UnPackage.channel_data_filter(_data, [], [channel])
        # 将解包的结果转为一整个np.ndarray shape为 包数*单通道采样点数
        # data = np.array([data[0][frame_idx][channel] for frame_idx in data[0]])
        data: np.ndarray = np.frombuffer(_data, dtype='int16')
        assert data.size == self.qubit_solver.pointnum*8*self.qubit_solver.shots, '数据长度不足'
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
        pass

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


class LightTCPHandler(socketserver.StreamRequestHandler):
    rpc_server: RFSKitRPCServer = None

    def handle(self):
        head = self.rfile.read(16)
        head = struct.unpack('=IIII', head)
        if head[0] == 0x5F5F5F5F:
            if head[1] == 0x32000001:
                param = pickle.loads(self.rfile.read(head[3]-16))
                data = self.rpc_server.rpc_set(*param)



if __name__ == '__main__':
    import sys
    with RFSKitRPCServer(rfs_addr='192.168.1.176', addr=("0.0.0.0", 10801), use_builtin_types=True) as server:
        server.register_instance(server.rfs_kit, allow_dotted_names=True)

        server.register_function(server.get_adc_data)
        server.register_function(server.clear_ad_cache)
        server.register_function(server.init_dma)
        server.register_function(server.release_dma)

        server.register_function(server.rpc_set)
        server.register_function(server.rpc_get)
        server.register_function(server.execute_command)
        server.register_function(lambda: None, name='close')

        server.register_multicall_functions()
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            sys.exit(0)
