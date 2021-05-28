import time

from printLog import *
from pscn import Xdma
from PyQt5 import QtCore
import threading
import os
import numpy as np
from tools import Queue, Fifo


class UploadStatusSignal(QtCore.QObject):
    status_trigger = QtCore.pyqtSignal(object)  # 信号


us_signal = UploadStatusSignal()


class DataSolve:
    # 数据处理
    _weave_length_byte = 256
    _weave_length = _weave_length_byte // 4  # 4Byte
    _board = 0
    _channel_num = 0
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
    _stop_flag = False

    def get_weave_length(self):
        return self._weave_length_byte

    def __init__(self):
        self.xdma = Xdma()
        self._run_event = threading.Event()
        self._fd_list = []
        self._buffers = []
        self._unload_enable_state = self.init()  # 卸载使能状态， 启动卸载前需要判断改属性是否为True
        # 用于upload和solve函数之间互斥锁
        self.upload_solve_fifo = Fifo(self._buf_count, self._run_event)

    def init(self):
        fd_list = []
        try:
            buffers = []
            if not self.xdma.open_board(self._board) or not self.xdma.reset_board(self._board):
                assert 0, "xdma board init fail."
            for _ in range(self._buf_count):
                fd = self.xdma.alloc_buffer(self._board, self._dma_size)
                assert fd, "xdma alloc buffer fail."
                buffer = self.xdma.get_buffer(fd, self._dma_size)
                assert not isinstance(buffer, bool), "xdma get buffer fail."
                fd_list.append(fd)
                buffers.append(buffer)
            self._fd_list, self._buffers = fd_list, buffers
            return True
        except AssertionError as e:
            printError(e)
            self._error_message, = e.args
            [self.xdma.free_buffer(fd) for fd in fd_list]
            self.xdma.close_board(self._board)
            return False

    def get_state(self):
        return self._unload_enable_state

    def init_param(self):
        # 参数初始化
        self._run_event.set()
        self._files = None
        self.upload_solve_fifo.reset(self._run_event)
        self._queue = None
        self._stop_flag = False

    def stop_unload(self, is_alive):
        self._run_event.clear()
        if is_alive:
            self._run_event.wait()

    def start_unload(self, start_unload_function, finally_call, *args):
        """ 文件列表数据卸载 """
        try:
            if not self.get_state():
                printWarning(f"unload disabled, {self._error_message}")
                us_signal.status_trigger.emit([self.get_state()])
                return
            self.init_param()
            sel_files, filepath, de_interleave, label_show = args
            total_count = len(sel_files)
            for index, info in enumerate(sel_files):
                file_id, filename, sample_channel_count, file_sel_size, *icd_args = info
                # icd_args: [文件起始位置偏移, 文件卸载大小], 当为空时标识全部卸载, 则为[0, 0]
                if not icd_args:
                    icd_args = [0, 0]
                # 向qt发送signal，更新界面数值
                us_signal.status_trigger.emit([1, 0, 0, '%d / %d' % (index + 1, total_count)])
    
                if not start_unload_function(1, *icd_args, file_id):
                    printError(f"unload No.{index + 1} File fail, {filename}.")
                    return
                # ---- 指令发送/接收正常, 启动upload, write ----
                cur_size = file_sel_size * 1024 ** 2 // 4
                self._left_size = cur_size % self._dma_size
                count = cur_size // self._dma_size + 1 if self._left_size else cur_size // self._dma_size

                start_time = time.time()
    
                _de_interleave = de_interleave and sample_channel_count > 1
    
                printDebug(f"dma size: {self._dma_size}, channel count: {sample_channel_count}, "
                           f"current size: {cur_size}, count: {count}, left size: {self._left_size}, "
                           f"de-interleave: {_de_interleave}")
                s_thread = threading.Thread(target=self.solve, args=(count, _de_interleave, sample_channel_count))
                s_thread.start()
                if filepath is not None:
                    # 防止同时操作一片内存导致存入数据异常
                    self._queue = Queue(self.upload_solve_fifo.mininum - 1, sample_channel_count if _de_interleave else 1)
                    self._files = files = []

                    if not _de_interleave:
                        files.append(open(f"{filepath}/{filename}", "wb"))
                        threading.Thread(target=self.write, args=(0, count, _de_interleave)).start()
                    else:
                        base_filename, suffix = os.path.splitext(filename)
                        filename_fmt = "{}/{}_C{}{}".format(filepath, base_filename, "{}", suffix)
                        for c_num in range(sample_channel_count):
                            files.append(open(filename_fmt.format(c_num), "wb"))
                            threading.Thread(target=self.write, args=(c_num, count, _de_interleave)).start()

                u_thread = threading.Thread(target=self.upload, args=(count, ))
                u_thread.start()
                u_thread.join()
                s_thread.join()
                if self._queue:
                    self._queue.join()
                if self._stop_flag or not self._run_event.is_set():
                    us_signal.status_trigger.emit([2, 0, 0, 'Abort'])
                    break
                speed = file_sel_size / (time.time() - start_time)
                printColor(f'File: {filename} transmission Done. Everage speed is {speed:.2f} MB/s', color='green')
                us_signal.status_trigger.emit([1, 100, 0, ""])

            self._run_event.clear()
            us_signal.status_trigger.emit([2, 0, 0, 'Done'])
        except Exception as e:
            printException(e)
        finally:
            if not self._run_event.is_set():
                # 当所有文件卸载完或点击停止卸载时执行
                finally_call()

            self._run_event.set()

    def upload(self, count):
        """ 数据上传 """
        try:
            length = self._dma_size
            for i in range(1, count+1):
                fd_index = self.upload_solve_fifo.chk_ful()
                if not self._run_event.is_set():
                    return
                if i == count and self._left_size:
                    length = self._left_size
                if not self.xdma.stream_read(self._board, self._dma_channel_num, self._fd_list[fd_index], length,
                                             stop_event=self._run_event.is_set):
                    printError(f"Dma has the problem on round {i}")
                    return
                self.upload_solve_fifo.push()

        except AssertionError as e:
            printDebug(e)
        except Exception as e:
            printException(e)

    def solve(self, count, de_interleave, sample_channel_count):
        """ 数据解包 """
        try:
            once_weave = self._weave_length * sample_channel_count  # 通道一次交织的长度
            start_time, s_count = time.time(), 0
            length = self._dma_size
            _stop_flag = self._stop_flag
            for i in range(1, count+1):
                data = self._buffers[self.upload_solve_fifo.chk_ept()]
                if i == count and self._left_size:
                    length = self._left_size
                    if de_interleave:
                        length -= length % once_weave
                    data = data[: length]

                if not self._run_event.is_set():
                    return

                if not _stop_flag:
                    try:
                        if de_interleave:
                            data = data.reshape(length // once_weave, sample_channel_count, self._weave_length)
                            data = np.einsum("abc->bac", data).reshape(sample_channel_count, length // sample_channel_count)
                    except Exception as e:
                        printException(e)
                        self._stop_flag = _stop_flag = True

                if self._queue:
                    while not self._queue.m_put(data):
                        if not self._run_event.is_set():
                            return

                elif time.time() - start_time >= 1:
                    start_time, s_count = self._update(start_time, i, count, s_count)

                self.upload_solve_fifo.pop()

        except AssertionError as e:
            printDebug(e)
        except Exception as e:
            printException(e)

    def write(self, c_num, count, de_interleave):
        """ 数据存储
            c_num: 通道号
        """
        try:
            cur_count, t_count = 1, count + 1
            if c_num == 0:
                self._write_start_time, self._prev_count = time.time(), 0
            while cur_count != t_count:
                data = self._queue.m_get(c_num)

                if not self._run_event.is_set():
                    return

                if isinstance(data, bool):
                    continue

                flag, data = data

                if not self._stop_flag:
                    try:
                        self._files[c_num].write(data[c_num] if de_interleave else data)
                    except Exception as e:
                        printException(e)
                        self._stop_flag = True

                if flag and time.time() - self._write_start_time >= 1:
                    self._write_start_time, self._prev_count = self._update(
                        self._write_start_time, cur_count, count, self._prev_count)
                cur_count += 1
        except AssertionError as e:
            printDebug(e)
        except Exception as e:
            printException(e)
        finally:
            self._files[c_num].close()
            self._queue.task_done()
            printDebug("c_num task done")

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
