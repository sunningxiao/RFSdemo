from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import Binary
import numpy as np
from typing import Tuple

from NS_MCI.interface import DataNoneInterface, CommandTCPInterface
from NS_MCI import RFSKit
from NS_MCI.tools.data_unpacking import UnPackage
from NS_MCI.xdma import LightDMAMixin
from NS_MCI.config import param_cmd_map
from svqbit import SolveQubit


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
        self.qubit_solver = SolveQubit()
        self._setup_dma()

    @staticmethod
    def _transform_value(value):
        """
        支撑numpy.ndarray rpc

        :param value:
        :return:
        """
        if isinstance(value, list) and len(value)==3 and isinstance(value[0], bytes) and isinstance(value[1], str) and isinstance(value[2], list):
            data = np.frombuffer(value[0], dtype=value[1])
            value = data.reshape(value[2])
        return value

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
        value = self._transform_value(value)

        self.rfs_kit.set_param_value('DAC通道选择', channel)
        if name == 'Waveform':
            bit = 16
            value = (2 ** (bit - 1) - 1) * value
            self.rfs_kit.execute_command('DAC数据更新', True, value.tobytes())
        elif name == 'GenWave':
            pass
        elif name == 'Delay':
            param_name = f'DAC{channel}延迟'
            self.rfs_kit.set_param_value(param_name, value)
            self.rfs_kit.execute_command('DAC配置')
        elif name == 'Output':
            param_name = f'DAC{channel}使能'
            if value == 'OFF':
                value = False
            tmp = 1 if value else 0
            self.rfs_kit.set_param_value(param_name, tmp)

        elif name == 'Shot':
            self.rfs_kit.set_param_value('基准PRF数量', value)
            self.qubit_solver.setshots(value)
        elif name == 'StartCapture':
            self.clear_ad_cache()
            self.rfs_kit.execute_command('复位')
        elif name == 'FrequencyList':
            self.qubit_solver.setfreqlist(value, channel)
        elif name == 'PointNumber':
            param_name = f'ADC{channel}门宽'
            self.rfs_kit.set_param_value(param_name, value)
            self.rfs_kit.execute_command('ADC配置')
            # 转为16ns倍数对应的点数
            tmp = self.qubit_solver.ADrate * 1e-9 * value
            self.qubit_solver.setpointnum(int(tmp//16*16))

        elif name == 'Reset':
            self.rfs_kit.execute_command('复位')
        elif name == 'MixMode':
            self.rfs_kit.set_param_value('DAC 奈奎斯特区', value)
            if execute:
                self.rfs_kit.execute_command('初始化')
        elif name == 'RefClock':
            tmp = 4
            if value == 'out':
                tmp = 3
            self.rfs_kit.set_param_value('系统参考时钟选择', tmp)
            if execute:
                self.rfs_kit.execute_command('初始化')
        elif name == 'TriggerDelay':
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

    def rpc_get(self, name, channel=1):
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
            return self.get_adc_data(channel, True)

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

    def get_adc_data(self, channel=0, solve=True) -> Tuple[bytes, str, Tuple]:
        """
        通过pcie获取数据

        :param channel:
        :param solve:
        :return:
        """
        self._cache_dma_data()
        print('缓存数据更新完成')
        _data = self.ad_data
        data = UnPackage.channel_data_filter(_data, [], [channel])
        # 将解包的结果转为一整个np.ndarray shape为 包数*单通道采样点数
        data = np.array([data[0][frame_idx][channel] for frame_idx in data[0]])
        if solve:
            data = self.qubit_solver.calculateCPU(data, channel)
        return data.tobytes(), str(data.dtype), data.shape

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


if __name__ == '__main__':
    import sys
    with RFSKitRPCServer(rfs_addr='192.168.1.175', addr=("0.0.0.0", 10801), use_builtin_types=True) as server:
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
