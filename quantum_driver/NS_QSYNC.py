import pickle
import time
from typing import Union
import socket
import struct
import xmlrpc.client
from xmlrpc.client import Transport
from functools import lru_cache, wraps

import numpy as np
import waveforms

from .common import BaseDriver, Quantity, get_coef


class Driver(BaseDriver):
    CHs = list(range(1, 17))

    quants = [
        Quantity('SystemSync', value=None, ch=1),         # set/get,运行次数
        Quantity('GenerateTrig', value=None, unit='ns'),  # set/get,触发周期单位ns，触发数量=shot
        Quantity('ResetTrig', value=None, unit='ns'),
        Quantity('Shot', value=1024, ch=1),               # set/get, 运行次数
        Quantity('TrigPeriod', value=200e-6, ch=1),       # set/get, 触发周期
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
        self.handle = None
        self.model = 'NS_QSYNC'  # 默认为设备名字
        self.srate = 6e9

        self.param = {'shots': 1024, 'period': 200e6, 'MixMode': 2, 'ADrate': 4e9, 'DArate': 6e9}

    def open(self, **kw):
        """
        输入IP打开设备，配置默认超时时间为5秒
        打开设备时配置RFSoC采样时钟，采样时钟以参数定义
        """
        # 配置系统初始值
        system_parameter = kw.get('system_parameter', {})
        values = self.SystemParameter.copy()
        values.update(system_parameter)
        for name, value in values.items():
            if value is not None:
                self.set(name, value, 1)

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
        if name == 'SystemSync':
            data = self.__fmt_qsync_sync(self.param['MixMode'], self.param['ADrate'], self.param['DArate'])
            self._send_command(data)
        elif name == 'GenerateTrig':
            data = self.__fmt_qsync_start(self.param['TrigPeriod'], self.param['Shot'])
            self._send_command(data)
        elif name == 'ResetTrig':
            data = self.__fmt_qsync_reset()
            self._send_command(data)

        else:
            self.param[name] = value

    def get(self, name, channel=1, value=0):
        """
        查询设备属性，获取数据

        """
        return self.param.get(name, None)

    def _connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.addr, 5001))
        sock.settimeout(self.timeout)
        # sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
        # sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, True)
        # sock.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 60 * 1000, 30 * 1000))
        # sock.close()
        return sock

    # @__with_new_connection
    def _send_command(self, data: Union[str, bytes], wait=0):
        """
        发送指定内容到后端

        :param data: 指令内容
        :param wait: 指令发送完成后，等待一段时间再接收反馈，阻塞式等待
        :return:
        """
        command_bak = data
        try:
            sock = self._connect()
        except Exception as e:
            print(e)
            return False

        try:
            sock.sendall(memoryview(data))

            time.sleep(wait)
            _feedback = sock.recv(20)
            if not _feedback.startswith(b'\xcf\xcf\xcf\xcf'):
                print('返回指令包头错误')
                return False
            if command_bak[4:8] != _feedback[4:8]:
                print('返回指令ID错误')
                return False
            _feedback = struct.unpack('=IIIII', _feedback)
            if _feedback[4] != 0:
                print('指令成功下发，但执行失败')
                return False
        except Exception as e:
            print(e)
            return False
        finally:
            sock.close()
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
            *args
        )

        return struct.pack('=IIIIII', *cmd_pack)
