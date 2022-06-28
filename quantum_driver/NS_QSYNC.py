import pickle
import time
from typing import Union
import socket
import struct
import xmlrpc.client
from xmlrpc.client import Transport
from functools import lru_cache

import numpy as np
import waveforms

from .common import BaseDriver, Quantity, get_coef


class Driver(BaseDriver):
    CHs = list(range(1, 17))

    quants = [
        # 采集运行参数
        Quantity('Shot', value=1024, ch=1),  # set/get,运行次数
        Quantity('PointNumber', value=16384, unit='point'),  # set/get,AD采样点数
        Quantity('TriggerDelay', value=0, ch=1, unit='s'),  # set/get,AD采样延时
        Quantity('FrequencyList', value=[], ch=1, unit='Hz'),  # set/get,解调频率列表，list，单位Hz
        Quantity('PhaseList', value=[], ch=1, unit='Hz'),  # set/get,解调频率列表，list，单位Hz
        Quantity('Coefficient', value=None, ch=1),
        Quantity('DemodulationParam', value=None, ch=1),
        Quantity('CaptureMode'),
        Quantity('StartCapture'),  # set,开启采集（执行前复位）
        Quantity('TraceIQ', ch=1),  # get,获取原始时域数据
        # 返回：array(shot, point)
        Quantity('IQ', ch=1),  # get,获取解调后数据,默认复数返回
        # 系统参数，宏定义修改，open时下发
        # 复数返回：array(shot,frequency)
        # 实数返回：array(IQ,shot,frequency)

        # 任意波形发生器
        Quantity('Waveform', value=np.array([]), ch=1),  # set/get,下发原始波形数据
        Quantity('Delay', value=0, ch=1),  # set/get,播放延时
        Quantity('LinSpace', value=[0, 30e-6, 1000], ch=1),  # set/get, np.linspace函数，用于生成timeline
        Quantity('Output', value=True, ch=1),  # set/get,播放通道开关设置
        Quantity('GenWave', value=waveforms.Waveform(), ch=1),  # set/get, 设备接收waveform对象，根据waveform对象直接生成波形
        # set/get, 设备接收IQ分离的waveform对象列表，根据waveform对象列表直接生成波形
        Quantity('GenWaveIQ', value=[waveforms.Waveform(), waveforms.Waveform()], ch=1),

        # 内触发
        Quantity('GenerateTrig', value=1e7, unit='ns'),  # set/get,触发周期单位ns，触发数量=shot
    ]

    SystemParameter = {
        'MixMode': 2,  # Mix模式，1：第一奈奎斯特去； 2：第二奈奎斯特区
        'RefClock': 'out',  # 参考时钟选择： ‘out’：外参考时钟；‘in’：内参考时钟
        'ADrate': 4e9,  # AD采样率，单位Hz
        'DArate': 6e9,  # DA采样率，单位Hz
        'KeepAmp': 1,  # DA波形发射完毕后，保持最后一个值
        'DAC抽取倍数': 1,  # DA内插比例，1,2,4,8
        'DAC本振频率': 0,  # DUC本振频率，单位MHz
        'ADC抽取倍数': 1,  # AD抽取比例，1,2,4,8
        'ADC本振频率': 0  # DDC本振频率，单位MHz
    }

    def __init__(self, addr: str = '', timeout: float = 10.0, **kw):
        super().__init__(addr, timeout, **kw)
        self.fast_rpc = None
        self.handle = None
        self.model = 'NS_QSYNC'  # 默认为设备名字
        self.srate = 6e9

    def open(self, **kw):
        """
        输入IP打开设备，配置默认超时时间为5秒
        打开设备时配置RFSoC采样时钟，采样时钟以参数定义
        """
        tran = Transport(use_builtin_types=True)
        tran.accept_gzip_encoding = False
        self.handle = xmlrpc.client.ServerProxy(f'http://{self.addr}:10801', transport=tran, allow_none=True,
                                                use_builtin_types=True)

        self.fast_rpc = FastRPC(self.addr)

        # 判断是否更改ip
        rfs_ip = kw.get('rfs_ip', None)
        if rfs_ip is not None:
            self.handle.start_command(rfs_ip)
            # self.handle.change_rfs_addr(rfs_ip)
        # else:
        #     # 此时会连接rfsoc的指令接收tcp server
        #     self.handle.start_command()

        # 配置系统初始值
        system_parameter = kw.get('system_parameter', {})
        values = self.SystemParameter.copy()
        values.update(system_parameter)
        for name, value in values.items():
            if value is not None:
                self.handle.rpc_set(name, value, 1, False)

        # 系统开启前必须进行过一次初始化
        result = self.__exec_command('初始化')
        result = self.__exec_command('DAC配置')
        result = self.__exec_command('ADC配置')
        self.handle.init_dma()
        if not result:
            print(self.handle.get_all_status())

    def close(self, **kw):
        """
        关闭设备
        """
        # self.handle.release_dma()
        # self.handle.close()
        pass

    def write(self, name: str, value, **kw):
        channel = kw.get('ch', 1)
        return self.set(name, value, channel)

    def read(self, name: str, **kw):
        channel = kw.get('ch', 1)
        result = self.get(name, channel)
        return result

    def set(self, name, value=0, channel=1):
        """
        设置设备属性
        """
        pass

    def get(self, name, channel=1, value=0):
        """
        查询设备属性，获取数据

        """
        pass

    def _connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.addr, 5001))
        sock.settimeout(self.timeout)
        # sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
        # sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, True)
        # sock.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 60 * 1000, 30 * 1000))
        # sock.close()
        return sock

    def _send_command(self, data: Union[str, bytes], wait=0):
        command_bak = data
        try:
            sock = self._connect()
            sock.sendall(memoryview(data))
        except Exception as e:
            print(e)
            return False

        try:
            time.sleep(wait)
            _feedback = sock.recv(20)
            if not _feedback.startswith(self.icd_param.recv_header):
                print('返回指令包头错误')
                return False
            if command_bak[4:8] != _feedback[4:8]:
                print('返回指令ID错误')
                return False
            _feedback = struct.unpack(self.icd_param.fmt_mode + 'IIIII', _feedback)
            if _feedback[4] != 0:
                print('指令成功下发，但执行失败')
                return False
        except Exception as e:
            print(e)
            return False
        return True

    @lru_cache(maxsize=16)
    def __fmt_qsync_reset(self):
        cmd_pack = (
            0x5F5F5F5F,
            0x31000000,
            0x00000000,
            16,
        )

        return struct.pack('=IIII', *cmd_pack)

    @lru_cache(maxsize=32)
    def __fmt_qsync_start(self, period, shots):
        cmd_pack = (
            0x5F5F5F5F,
            0x31000000,
            0x00000000,
            24,
            period,
            shots
        )

        return struct.pack('=IIIIII', *cmd_pack)

    @lru_cache(maxsize=32)
    def __fmt_qsync_sync(self, *args):
        cmd_pack = (
            0x5F5F5F5F,
            0x31000000,
            0x00000000,
            24,
            ...
        )

        return struct.pack('=IIIIII', *cmd_pack)
