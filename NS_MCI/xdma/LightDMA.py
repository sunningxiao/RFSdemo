import threading
import time

from NS_MCI.xdma import xdma_base
from NS_MCI.xdma.xdma import Xdma
import numpy as np


class LightDMAMixin:
    fpga_ddr_in_address = 0x0
    fpga_ddr_out_address = 0x4
    fpga_ddr_deep_address = 0x8
    fpga_clk_from_address = 0x00+4*3
    fpga_clk_online_address = 0x00+4*4
    fpga_trig_count_address = 0x00+4*5
    fpga_frame_version_address = 0x0+4*6
    fpga_clear_trig_address = 0x0+4*63

    fd_count = 1  # 10个颗粒度的缓存
    dma_size = 512 * 1024 ** 2  # 2GB颗粒度
    da_channel_num = 4
    da_channel_width = 102.4e-6

    def __init__(self):
        self.fd_index = 0
        self.fd_list = []
        self.down_fd_list = []
        self.buffer_pointer_list = []
        self.buffer_list = []
        self.down_buffer_list = []
        self.ad_data = np.array([], dtype='u4')
        self.init_ddr_deep = 0
        self.has_data_flag = 0
        self.xdma_opening = False
        self.da_cache = np.array([], dtype='int16')
        self.recv_lock = threading.Lock()
        self.recv_lock = threading.Lock()
        self.stop_event = threading.Event()
        self.xdma_obj = Xdma()

    def _setup_dma(self):
        self.fd_index = 0
        self.fd_list = []
        self.down_fd_list = []
        self.buffer_pointer_list = []
        self.buffer_list = []
        self.down_buffer_list = []
        self.ad_data = np.array([], dtype='u4')
        self.init_ddr_deep = 0
        self.has_data_flag = 0
        self.xdma_opening = False
        self.da_cache = np.array([], dtype='int16')
        self.recv_lock = threading.Lock()
        self.send_lock = threading.Lock()
        self.stop_event = threading.Event()
        self.xdma_obj = Xdma()

    def init_dma(self):
        """
        初始化dma

        :return:
        """
        # 初始化dma上行内存
        if self.xdma_opening:
            return
        xdma_base.fpga_open(0, poll_interval_ms=0)
        for i in range(self.fd_count):
            fd = xdma_base.fpga_alloc_dma(0, self.dma_size)
            self.fd_list.append(fd)
            self.buffer_list.append(xdma_base.fpga_get_dma_buffer(fd, self.dma_size))
            self.buffer_pointer_list.append(0)

        self.init_ddr_deep = self.sig_fpga_recv_count
        self.xdma_opening = True

        # 初始化dma下行内存
        channel_size = round(self.da_channel_width*self.qubit_solver.DArate)
        down_size = int(self.da_channel_num*channel_size/2)
        fd = xdma_base.fpga_alloc_dma(0, down_size)
        self.down_fd_list.append(fd)
        buffer = np.frombuffer(xdma_base.fpga_get_dma_buffer(fd, down_size), dtype='int16')
        buffer = buffer.reshape((self.da_channel_num, channel_size))
        self.da_cache = buffer
        self.down_buffer_list.append(buffer)
        self.buffer_memset()

        print('xdma初始化成功')

    def release_dma(self):
        """
        释放dma

        :return:
        """
        if not self.xdma_opening:
            return

        for i in range(self.fd_count):
            fd = self.fd_list[i]
            xdma_base.fpga_free_dma(fd)
        self.fd_list = []
        self.buffer_list = []
        self.buffer_pointer_list = []
        xdma_base.fpga_close(0)
        self.xdma_opening = False

        for i in self.down_fd_list:
            xdma_base.fpga_free_dma(i)

        print('xdma释放成功')

    def buffer_memset(self):
        for i in range(4):
            self.da_cache[i][0] = (int(f'0x{i}{i}', 16) << 8)+0xFF
            self.da_cache[i][1:] = np.arange(round(self.da_channel_width*self.qubit_solver.DArate)-1, dtype='int16')

    def clear_ad_cache(self):
        self.stop_event.set()
        self.init_ddr_deep = self.sig_fpga_recv_count
        self.buffer_pointer_list = [0 for _ in range(self.fd_count)]
        self.ad_data = np.array([], dtype='u4')
        print('缓存清空')

    def _download_da_data(self, size=None, callback=None):
        fd = self.down_fd_list[0]
        size = self.down_buffer_list[0].size//2 if size is None else size
        print(f'开始下发da数据 {size*4}Bytes')
        with self.send_lock:
            if self.stop_event.is_set():
                print('da下发终止')
                return

            if not self.xdma_obj.stream_write(0, 0, fd, size, 0, lambda: self.stop_event.is_set(), 0):
                print('下行失败')
                return

            if self.stop_event.is_set():
                print('da下发终止')
                return
            print('下行成功')

    def _cache_dma_data(self, size: int, callback=None):
        """
        取空xdma

        :return:
        """
        print(self.fd_index)
        stop_flag = 1
        while stop_flag and self.sig_fpga_recv_count > self.sig_agx_recv_count:
            print('取数循环体开始')
            fd = self.fd_list[self.fd_index]
            pointer = self.buffer_pointer_list[self.fd_index]
            current_deep = self.sig_fpga_recv_count - self.init_ddr_deep - pointer
            print(f'current_deep: {current_deep}')
            dma_size = current_deep - current_deep % 64
            if dma_size == 0:
                break

            print(f'dma数据量{dma_size}')

            recv_length = xdma_base.fpga_recv(0, 0, fd, 0, dma_size, offset=pointer,
                                              timeout=xdma_base.DMA_WAIT_FOR_EVER)
            if recv_length == xdma_base.FAIL:
                print(xdma_base.fpga_err_msg().decode())
                break
            # if recv_length != self.dma_size:
            #     xdma_base.fpga_pause_dma(fd)
            #     recv_length = xdma_base.fpga_poll_dma(fd)
            #     xdma_base.fpga_break_dma(fd)

            pointer += recv_length
            print(f'数据指针位置{pointer}')
            self.ad_data = self.buffer_list[self.fd_index][:pointer]
            self.buffer_pointer_list[self.fd_index] = pointer

            # self.fd_index += 1
            # if self.fd_index >= self.fd_count:
            #     self.fd_index = 0

            if self.ad_data.size >= 1024 ** 3:
                # 总长度大于4G直接退出
                break
            # stop_flag -= 1
        self.has_data_flag -= 1

    def _cache_dma_size(self, size: int, callback=None):
        st = time.time()
        print(f'dma开始: {size} ')
        split = 1
        frame = size // split
        self.stop_event.clear()
        with self.recv_lock:
            for i in range(split):
                fd = self.fd_list[self.fd_index]
                pointer = self.buffer_pointer_list[self.fd_index]
                if self.stop_event.is_set():
                    print('xdma终止')
                    return

                if not self.xdma_obj.stream_read(0, 0, fd, frame, pointer,
                                                 lambda: self.stop_event.is_set(), 0):
                    print('上行失败')
                    return

                if self.stop_event.is_set():
                    print('xdma终止')
                    return

                pointer += frame
                print(f'数据指针位置{pointer}')
                self.ad_data = self.buffer_list[self.fd_index][:pointer]
                self.buffer_pointer_list[self.fd_index] = pointer

            print(f'dma耗时{time.time()-st}')
            if callable(callback):
                callback()
            print(f'总耗时{time.time()-st}')
        # self.recv_event.clear()

    @property
    def sig_fpga_clk_from(self):
        """

        :return: 外参考时钟选择 0: 内参考、 1：外参考
        """
        flag = xdma_base.fpga_rd_lite(0, self.fpga_clk_from_address)
        print(f'***fpga时钟源 {flag}')
        res = '内参考时钟' if flag else '外参考时钟'
        return res

    @property
    def sig_fpga_clk_online(self):
        """

        :return: 参考时钟锁定 0: 未锁定、 1：锁定
        """
        flag = xdma_base.fpga_rd_lite(0, self.fpga_clk_online_address)
        print(f'***fpga参考时钟 {flag}')
        res = '锁定' if flag else '未锁定'
        return res

    @property
    def sig_fpga_trig_count(self):
        """

        :return: 触发数量 收到的触发信号数量
        """
        return xdma_base.fpga_rd_lite(0, self.fpga_trig_count_address)

    @property
    def sig_fpga_frame_version(self):
        """

        :return: FPGA版本
        """
        return hex(xdma_base.fpga_rd_lite(0, self.fpga_frame_version_address))[2:]

    @property
    def sig_fpga_reset_trig(self):
        """

        :return: 重置trig计数
        """
        xdma_base.fpga_wr_lite(0, self.fpga_clear_trig_address, 1)
        xdma_base.fpga_wr_lite(0, self.fpga_clear_trig_address, 0)
        return True

    @property
    def sig_fpga_recv_count(self):
        """

        :return: 进入fpga ddr的数据计数，单位4Byte
        """
        return xdma_base.fpga_rd_lite(0, self.fpga_ddr_in_address) * 8

    @property
    def sig_fpga_send_count(self):
        """

        :return: 从fpga ddr取出数据计数，单位4Byte
        """
        return xdma_base.fpga_rd_lite(0, self.fpga_ddr_out_address) * 8

    @property
    def sig_fpga_current_deep(self):
        """

        :return: fpga ddr的当前深度，单位4Byte  但当前深度为0时会被标成16
        """
        return xdma_base.fpga_rd_lite(0, self.fpga_ddr_deep_address) * 8

    @property
    def sig_agx_recv_count(self):
        # print(f'初始{self.init_ddr_deep}')
        # print(f'初始list{self.buffer_pointer_list}')
        return self.init_ddr_deep + self.buffer_pointer_list[self.fd_index]
