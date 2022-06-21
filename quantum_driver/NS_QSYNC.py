import threading
import time
from typing import Union
import socket
import struct
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor
import atexit

from .common import BaseDriver, Quantity, get_coef

thread_pool = ThreadPoolExecutor(max_workers=10)
_scanning_lock = threading.Lock()
_scanning_stop_event = threading.Event()
_device_set = set()


@atexit.register
def global_system_exit():
    thread_pool.shutdown(wait=False)


class Driver(BaseDriver):
    _scanning_lock = _scanning_lock
    _device_set = _device_set

    icd_head_reset = 0x41000002
    icd_head_cmd_2 = 0x31000015
    icd_head_cmd_3 = 0x410000B1
    icd_head_cmd_4 = 0x31000013
    icd_head_cmd_5 = 0x410000B2
    icd_head_cmd_6 = 0x3100001A
    icd_head_cmd_7 = 0x410000B3
    CHs = list(range(1, 17))

    quants = [
        Quantity('SystemSync', value=None, ch=1),  # set/get,运行次数
        Quantity('GenerateTrig', value=None, unit='s'),  # set/get,触发周期单位s，触发数量=shot
        Quantity('ResetTrig', value=None),
        Quantity('Shot', value=1024, ch=1),  # set/get, 运行次数
        Quantity('TrigPeriod', value=200e-6, ch=1),  # set/get, 触发周期
        Quantity('TrigFrom', value=0, ch=1),  # Trig来源： 0：内部产生；1：外部输入
        Quantity('RefClock', value='out', ch=1),  # 参考时钟选择： ‘out’：外参考时钟；‘in’：内参考时钟
    ]

    SystemParameter = {
        'RefClock': 'out',  # 参考时钟选择： ‘out’：外参考时钟；‘in’：内参考时钟
        'TrigFrom': 0,  # Trig来源： 0：内部产生；1：外部输入
        'TrigPeriod': 200e-6,
    }

    def __init__(self, addr: str = '', timeout: float = 10.0, **kw):
        super().__init__(addr, timeout, **kw)
        self.handle = None
        self.model = 'NS_QSYNC'  # 默认为设备名字
        self.srate = 6e9

        self.param = {'shots': 1024, 'period': 200e-6, 'MixMode': 2, 'ADrate': 4e9, 'DArate': 6e9}

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

        self.sync_system()
        print(f'qsync {self.addr} opened successfully\nSystem synchronization succeeded')

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

    def set(self, name, value=None, channel=1):
        """
        设置设备属性
        """
        if name == 'SystemSync':
            self.sync_system()
        elif name == 'GenerateTrig':
            value = self.param['TrigPeriod'] if value is None else value
            data = self.__fmt_qsync_start(self.param['TrigFrom'], value, self.param['Shot'])
            self._send_command(data)
        elif name == 'ResetTrig':
            data = self.__fmt_qsync_common(self.icd_head_reset)
            self._send_command(data)
        elif name == 'RefClock':
            self.param['RefClock'] = value
            data = self.__fmt_qsync_ref_from(value)
            self._send_command(data)

        else:
            self.param[name] = value

    def get(self, name, channel=1, value=0):
        """
        查询设备属性，获取数据

        """
        return self.param.get(name, None)

    def sync_system(self):
        if Driver._scanning_lock.acquire(timeout=10):
            Driver._scanning_lock.release()
        if len(Driver._device_set) == 0:
            return

        # self._sendto_device(self.icd_head_cmd_2)
        # self._sendto_qsync(self.icd_head_cmd_3)
        # self._sendto_device(self.icd_head_cmd_4)
        # self._sendto_qsync(self.icd_head_cmd_5)
        # self._sendto_device(self.icd_head_cmd_6)
        # self._sendto_qsync(self.icd_head_cmd_7)

    def _sendto_device(self, cmd_head):
        cmd_data = self.__fmt_qsync_common(cmd_head)
        futures = [thread_pool.submit(self._send_command, cmd_data, 0, addr, 5000) for addr in Driver._device_set]
        if not all(future.result() for future in futures):
            print(f'device: 系统同步过程 {hex(cmd_head)} 执行失败')

    def _sendto_qsync(self, cmd_head):
        cmd_data = self.__fmt_qsync_common(cmd_head)
        if not self._send_command(cmd_data):
            print(f'qsync: 系统同步过程 {hex(cmd_head)} 执行失败')

    def _connect(self, addr=None, port=5001):
        addr = self.addr if addr is None else addr
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((addr, port))
        sock.settimeout(self.timeout)
        # sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
        # sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, True)
        # sock.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 60 * 1000, 30 * 1000))
        # sock.close()
        return sock

    # @__with_new_connection
    def _send_command(self, data: Union[str, bytes], wait=0, addr=None, port=5001):
        """
        发送指定内容到后端

        :param data: 指令内容
        :param wait: 指令发送完成后，等待一段时间再接收反馈，阻塞式等待
        :return:
        """
        command_bak = data
        try:
            sock = self._connect(addr=addr, port=port)
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
            # print(_feedback)
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

    @lru_cache(maxsize=32)
    def __fmt_qsync_common(self, head):
        cmd_pack = (
            0x5F5F5F5F,
            head,
            0x00000000,
            16,
        )

        return struct.pack('=IIII', *cmd_pack)

    @lru_cache(maxsize=16)
    def __fmt_qsync_ref_from(self, _from):
        if _from == 'in':
            _from = 0
        elif _from == 'out':
            _from = 1
        else:
            _from = 0
        cmd_pack = (
            0x5F5F5F5F,
            0x4100000F,
            0x00000000,
            20,
            _from
        )

        return struct.pack('=IIIII', *cmd_pack)

    @lru_cache(maxsize=32)
    def __fmt_qsync_start(self, src, period, shots):
        cmd_pack = (
            0x5F5F5F5F,
            0x41000001,
            0x00000000,
            28,
            int(src),
            int(period*1e9) & 0xFFFFFFFF,
            int(shots)
        )

        return struct.pack('=IIIIIII', *cmd_pack)


def do_scanning():
    """
    扫描板卡

    :return:
    """
    while True:
        dest = ('<broadcast>', 5003)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        addrs = socket.getaddrinfo(socket.gethostname(), None)
        addr = [addr[4][0] for addr in addrs if addr[4][0].startswith('192.168.1.')]
        _bind = False
        _port = 15000
        with _scanning_lock:
            while not _bind:
                try:
                    s.bind((addr[0], _port))
                    _bind = True
                except Exception as e:
                    _port += 1
                    if _port >= 30000:
                        raise e
            s.sendto(b"____\x20\x00\x002\x00\x00\x00\x00\x14\x00\x00\x00\x00\x00\x00\x00", dest)
            s.settimeout(3)

            try:
                while True:
                    (_, addr) = s.recvfrom(20)
                    _device_set.add(addr[0])
            except Exception as e:
                s.close()
        time.sleep(5)


threading.Thread(target=do_scanning, daemon=True, name='qsync_scanning_device').start()
