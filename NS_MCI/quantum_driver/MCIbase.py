import numpy as np
from typing import List
import xmlrpc.client

from NS_MCI.interface import DataNoneInterface, CommandTCPInterface


class Quantity(object):
    def __init__(self, name: str, value=None, ch: int = 1, unit: str = ''):
        self.name = name
        self.default = dict(value=value, ch=ch, unit=unit)


class DriverAchieve:
    wave_file_name = 'wave_cache_file.dat'
    recv_block_size = 1024

    quants: List[Quantity] = []

    def __init__(self, addr: str = '', timeout: float = 3.0, default_length=6, **kw):
        self.model = 'NS_MCI'  # 默认为设备名字
        # self.rfs_kit = RFSKit(auto_load_icd=True,
        #                       auto_write_file=False,
        #                       cmd_interface=CommandTCPInterface,
        #                       data_interface=DataNoneInterface)
        # self.handle = self.rfs_kit
        self.addr = addr
        self.timeout = timeout
        self.default_length = default_length

        self.data_interface_class = DataNoneInterface
        self.cmd_interface_class = CommandTCPInterface

    def _close(self, **kw):
        """
        关闭设备
        """
        self.rfs_kit.release_dma()
        self.rfs_kit.close()

    # -----------------------------------------------------------------

    def _open(self):
        """
        输入IP打开设备，配置默认超时时间为5秒
        打开设备时配置RFSoC采样时钟，采样时钟以参数定义

        :param ipaddr: RFS的ip地址
        :param timeout: 指令发送超时时间
        """
        self.rfs_kit = xmlrpc.client.ServerProxy(f'http://{self.addr}:10801', allow_none=True, use_builtin_types=True)
        # 此时会连接rfsoc的指令接收tcp server
        self.rfs_kit.start_command()

        # 配置系统初始值
        for param in self.quants[:self.default_length]:
            value = param.default.get('value', None)
            if value is not None:
                channel = param.default['ch'] if param.default['ch'] else 1
                self.rfs_kit.rpc_set(param.name, value, channel, False)

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
        if isinstance(value, np.ndarray):
            value = [value.tobytes(), str(value.dtype), value.shape]
        self.rfs_kit.rpc_set(name, value, channel)

    def setValue(self, name, value=0, channel=1):
        self.set(name, value, channel)

    def get(self, name, channel=1):
        """
        查询设备属性，获取数据

        """
        tmp = self.rfs_kit.rpc_get(name, channel)
        if name in {'TraceIQ', 'IQ'}:
            data = np.frombuffer(tmp[0], dtype=tmp[1])
            tmp = data.reshape(tmp[2])

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
