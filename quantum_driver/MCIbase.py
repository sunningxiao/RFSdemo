from typing import List, Tuple
import xmlrpc.client
import pickle

import numpy as np
import waveforms


class Quantity(object):
    def __init__(self, name: str, value=None, ch: int = 1, unit: str = ''):
        self.name = name
        self.default = dict(value=value, ch=ch, unit=unit)


class DriverAchieve:
    quants: List[Quantity] = []
    SystemParameter = {'MixMode': 1,  # Mix模式，1：第一奈奎斯特去； 2：第二奈奎斯特区
                       'RefClock': 'out',  # 参考时钟选择： ‘out’：外参考时钟；‘in’：内参考时钟
                       'ADrate': 4e9,  # AD采样率，单位Hz
                       'DArate': 6e9,  # DA采样率，单位Hz
                       'DAC抽取倍数': 1,  # DA内插比例，1,2,4,8
                       'DAC本振频率': 0,  # DUC本振频率，单位MHz
                       'ADC抽取倍数': 1,  # AD抽取比例，1,2,4,8
                       'ADC本振频率': 0  # DDC本振频率，单位MHz
                       }

    def __init__(self, addr: str = '', timeout: float = 3.0, **kw):
        self.model = 'NS_MCI'  # 默认为设备名字
        # self.rfs_kit = RFSKit(auto_load_icd=True,
        #                       auto_write_file=False,
        #                       cmd_interface=CommandTCPInterface,
        #                       data_interface=DataNoneInterface)
        # self.handle = self.rfs_kit
        self.addr = addr
        self.timeout = timeout

    def _close(self, **kw):
        """
        关闭设备
        """
        self.rfs_kit.release_dma()
        self.rfs_kit.close()

    # -----------------------------------------------------------------

    def _open(self, system_parameter=None):
        """
        输入IP打开设备，配置默认超时时间为5秒
        打开设备时配置RFSoC采样时钟，采样时钟以参数定义

        :param system_parameter: 系统参数
        """
        if system_parameter is None:
            system_parameter = {}
        self.rfs_kit = xmlrpc.client.ServerProxy(f'http://{self.addr}:10801', allow_none=True, use_builtin_types=True)
        # 此时会连接rfsoc的指令接收tcp server
        self.rfs_kit.start_command()

        # 配置系统初始值
        values = self.SystemParameter.copy()
        values.update(system_parameter)
        for name, value in values.items():
            if value is not None:
                self.rfs_kit.rpc_set(name, value, 1, False)

        # 系统开启前必须进行过一次初始化
        self.__exec_command('初始化')
        self.__exec_command('DAC配置')
        self.__exec_command('ADC配置')
        self.rfs_kit.init_dma()

    def set(self, name, value=0, channel=1):
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
        """
        value = RPCValueParser.dump(value)
        if self.rfs_kit.rpc_set(name, value, channel):
            print(f'{name} 配置成功')

    def setValue(self, name, value=0, channel=1):
        self.set(name, value, channel)

    def get(self, name, channel=1, value=0):
        """
        查询设备属性，获取数据

        """
        tmp = self.rfs_kit.rpc_get(name, channel, value)
        # if name in {'TraceIQ', 'IQ', 'SIQ'}:
        #     data = np.frombuffer(tmp[0], dtype=tmp[1])
        #     tmp = data.reshape(tmp[2])
        tmp = RPCValueParser.load(tmp)

        return tmp

    def getValue(self, name, channel=1):
        self.get(name, channel)

    def __exec_command(self, button_name: str,
                       need_feedback=True, file_name=None, check_feedback=True,
                       callback=lambda *args: True, wait: int = 0):
        flag = self.rfs_kit.execute_command(button_name, need_feedback, file_name, check_feedback)
        if flag:
            print(f'指令{button_name}执行成功')
        else:
            print(f'指令{button_name}执行失败')

    def __del__(self):
        self._close()


class RPCValueParser:
    """
    rpc调用格式化工具集

    """
    @staticmethod
    def dump(value):
        if isinstance(value, np.ndarray):
            value = [str(type(value)), value.tobytes(), str(value.dtype), value.shape]
        elif isinstance(value, waveforms.Waveform):
            value = [str(type(value)), pickle.dumps(value)]
        elif isinstance(value, (list, tuple)):
            value = [RPCValueParser.dump(_v) for _v in value]

        return value

    @staticmethod
    def load(value):
        if isinstance(value, list) and len(value)>=2:
            if value[0] == str(type(np.ndarray)):
                data = np.frombuffer(value[1], dtype=value[2])
                value = data.reshape(value[3])
            elif value[0] == str(type(waveforms.Waveform)):
                value = pickle.loads(value[1])
        elif isinstance(value, (list, tuple)):
            value = [RPCValueParser.load(_v) for _v in value]
        return value
