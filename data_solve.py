import time

from printLog import *
from PyQt5 import QtCore
import threading
import os
import numpy as np
from netconn import DataTCPServer
from tools.unpackage import UnPackage
from tools import Queue, Fifo

# 是否解包存储
UNPACK = False


class UploadStatusSignal(QtCore.QObject):
    status_trigger = QtCore.pyqtSignal(object)  # 信号


us_signal = UploadStatusSignal()


class DataSolve:
    # 数据处理
    _weave_length_byte = 256
    _weave_length = _weave_length_byte // 4  # 4Byte
    _board = 0
    _channel_num = 8
    # _least_common_multiple = np.lcm.reduce((1, 2, 3, 4, 6))
    _dma_size = 1024 ** 2 * 15  # 4Byte  需要为(1, 2, 3, 4, 6)的公倍数, 解交织时
    _buf_count = 10
    _error_message = ""
    _files = None
    _queue = None
    _dma_channel_num = 0
    _left_size = 0
    _write_start_time = 0
    _prev_count = 0
    _info = None
    _stop_flag = False

    def get_weave_length(self):
        return self._weave_length_byte

    def __init__(self, server: DataTCPServer):
        self.server = server
        self._files = []
        self._cache = Queue(1024)

    def start_solve(self, filepath=None, write_file=True):
        self._cache = Queue(1024)
        # 启动数据接收线程
        _thread = threading.Thread(target=self.wait_connect)
        _thread.start()

        if filepath is None:
            filepath = time.strftime('%Y%m%d_%H-%M-%S', time.localtime())
        if not os.path.exists(filepath):
            os.mkdir(filepath)
        if not UNPACK:
            filename = 'data.dat'
            self._files.append(open(f'{filepath}/{filename}', 'wb'))
            _thread = threading.Thread(target=self.write, args=(self._files[-1], write_file))
            _thread.start()
        else:
            for i in range(self._channel_num):
                filename = f'cnt_{i}'
                self._files.append(open(f'{filepath}/{filename}', 'wb'))
            self.write_unpack()

        _thread = threading.Thread(target=self.solve, args=([True]*8, ))
        _thread.start()

        return True

    def wait_connect(self):
        self._stop_flag = False
        try:
            self.server.accept()
            # self.server.recv_server.settimeout(None)
            printColor('已建立连接', 'green')
            _header = self.server.recv()
            header = np.frombuffer(_header, dtype='u4')
            info = UnPackage.get_pack_info(0, header)
            self._info = info
            once_package = info[0] * info[7]
            if once_package > 1024**2*16:
                printWarning('解析包长过大，按16M接收')
                once_package = 1024**2*16
            printInfo(f'包长度{once_package}')
            _data = _header
            _data += self.server.recv(once_package - len(_header))
            # data = np.frombuffer(_data, dtype='u4')
            self._cache.put(_data)
            start_time = time.time()
            data_length = 0
            # self.server.recv_server.settimeout(5)
            while True:
                if self._stop_flag:
                    break
                # 接收数据
                _data = self.server.recv(once_package)
                # if _data is False:
                #     continue
                if len(_data) < once_package:
                    printInfo('数据连接已断开')
                    break
                self._cache.put(_data)
                data_length += once_package
                if time.time() - start_time > 1:
                    us_signal.status_trigger.emit((1, 0, data_length/(time.time() - start_time)/1024**2))
                    start_time = time.time()
                    data_length = 0
        except Exception as e:
            self._stop_flag = True
            self.server.recv_server.close()
            printException(e)
        self._stop_flag = True

    def solve(self, chl_flag: iter):
        """ 数据解包 """
        try:
            while self._cache.qsize() or not self._stop_flag:
                _data = self._cache.lookup()
                if _data:
                    data = np.frombuffer(_data, dtype='u4')
                    data = UnPackage.solve_source_data(data, chl_flag, for_save=False, step=-1)
                    if data:
                        us_signal.status_trigger.emit((1, 2, data))
                        time.sleep(1)
        except AssertionError as e:
            printDebug(e)
        except Exception as e:
            printException(e)

    def write(self, file, write_file):
        """ 数据存储
        """
        try:
            start_time = time.time()
            data_length = 0
            while self._cache.qsize() or not self._stop_flag:
                _data = self._cache.m_get(timeout=1)
                if _data and write_file:
                    file.write(_data[1])
                    data_length += len(_data[1])
                    if time.time() - start_time > 1:
                        us_signal.status_trigger.emit((1, 1, data_length/(time.time() - start_time)/1024**2))
                        start_time = time.time()
                        data_length = 0
        except AssertionError as e:
            printDebug(e)
        except Exception as e:
            printException(e)
        finally:
            file.close()
            printColor("文件保存完成", 'green')
            us_signal.status_trigger.emit((0,))

    def write_unpack(self):
        pass

    def _update(self, start_time, cur_count, count, s_count):
        gap_time = time.time() - start_time
        percent = cur_count / count * 100
        gap_count = cur_count - s_count
        if cur_count == count and self._left_size:
            gap_size = self._dma_size * 4 * (gap_count - 1) + self._left_size
        else:
            gap_size = self._dma_size * 4 * gap_count
        speed = gap_size / 1024 ** 2 / gap_time
        us_signal.status_trigger.emit([1, percent, speed, ""])
        return time.time(), cur_count
