from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import Binary
import numpy as np
from typing import Tuple

from NS_MCI.interface import DataNoneInterface, CommandTCPInterface
from NS_MCI import RFSKit
from NS_MCI.tools.data_unpacking import UnPackage
from NS_MCI.xdma import xdma_base


class RFSKitRPCServer(SimpleXMLRPCServer):
    fd_count = 1  # 10个颗粒度的缓存
    dma_size = 512*1024**2  # 2GB颗粒度
    ddr_in_address = 0x0
    ddr_out_address = 0x4
    ddr_deep_address = 0x8

    def __init__(self, rfs_addr='192.168.1.175', **kwargs):
        kwargs.update({'allow_none': True})
        super(RFSKitRPCServer, self).__init__(**kwargs)
        CommandTCPInterface._timeout = 10
        CommandTCPInterface._target_id = rfs_addr
        self.rfs_kit = RFSKit(auto_load_icd=True,
                              auto_write_file=False,
                              cmd_interface=CommandTCPInterface,
                              data_interface=DataNoneInterface)
        self.fd_index = 0
        self.fd_list = []
        self.buffer_pointer_list = []
        self.buffer_list = []
        self.ad_data = np.array([], dtype='u4')
        self.init_ddr_deep = 0
        self.has_data_flag = 0
        self.xdma_opening = False

    def init_dma(self):
        """
        初始化dma

        :return:
        """
        if self.xdma_opening:
            return
        xdma_base.fpga_open(0, poll_interval_ms=0)
        for i in range(self.fd_count):
            fd = xdma_base.fpga_alloc_dma(0, self.dma_size)
            self.fd_list.append(fd)
            self.buffer_list.append(xdma_base.fpga_get_dma_buffer(fd, self.dma_size))
            self.buffer_pointer_list.append(0)

        self.init_ddr_deep = self.__fpga_recv_count
        self.xdma_opening = True

        print('xdma初始化成功')

    def release_dma(self):
        """
        释放dma

        :return:
        """
        for i in range(self.fd_count):
            fd = self.fd_list[i]
            xdma_base.fpga_free_dma(fd)
        self.fd_list = []
        self.buffer_list = []
        self.buffer_pointer_list = []
        xdma_base.fpga_close(0)
        self.xdma_opening = False

        print('xdma释放成功')

    def clear_ad_cache(self):
        self.init_ddr_deep = self.__fpga_recv_count
        self.buffer_pointer_list = [0 for _ in self.buffer_pointer_list]
        self.ad_data = np.array([], dtype='u4')
        print('缓存清空')

    def get_adc_data(self, channel=0, unpack=True) -> Tuple[bytes, str, Tuple]:
        """
        通过pcie获取数据

        :param channel:
        :param unpack:
        :return:
        """
        self.__cache_dma_data()
        print('数据刷新完成')
        _data = self.ad_data
        if unpack:
            data = UnPackage.channel_data_filter(_data, [], [channel])
            # 将解包的结果转为一整个np.ndarray shape为 包数*单通道采样点数
            data = np.array([data[0][frame_idx][channel] for frame_idx in data[0]])

            return data.tobytes(), str(data.dtype), data.shape
        else:
            data = np.frombuffer(_data, dtype='uint32')
            # return data, data.reshape(int(len(data) / 2), 2).T
            return data.tobytes(), str(data.dtype), data.shape
        # data = _data
        # return data.tobytes(), str(data.dtype)

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

    def __cache_dma_data(self):
        """
        取空xdma

        :return:
        """
        while self.__fpga_recv_count > self.__agx_recv_count:
            fd = self.fd_list[self.fd_index]
            pointer = self.buffer_pointer_list[self.fd_index]
            current_deep = self.__fpga_recv_count - self.init_ddr_deep - pointer
            dma_size = current_deep - current_deep % 64
            if dma_size == 0:
                break

            print(f'dma数据量{dma_size}')

            recv_length = xdma_base.fpga_recv(0, 0, fd, 0, dma_size, offset=pointer, timeout=xdma_base.DMA_WAIT_FOR_EVER)
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

            self.fd_index += 1
            if self.fd_index >= self.fd_count:
                self.fd_index = 0

            if self.ad_data.size >= 1024**3:
                # 总长度大于4G直接退出
                break
        self.has_data_flag -= 1

    @property
    def __fpga_recv_count(self):
        """

        :return: 进入fpga ddr的数据计数，单位4Byte
        """
        return xdma_base.fpga_rd_lite(0, self.ddr_in_address)*8

    @property
    def __fpga_send_count(self):
        """

        :return: 从fpga ddr取出数据计数，单位4Byte
        """
        return xdma_base.fpga_rd_lite(0, self.ddr_out_address) * 8

    @property
    def __fpga_current_deep(self):
        """

        :return: fpga ddr的当前深度，单位4Byte  但当前深度为0时会被标成16
        """
        return xdma_base.fpga_rd_lite(0, self.ddr_deep_address) * 8

    @property
    def __agx_recv_count(self):
        return self.init_ddr_deep+self.buffer_pointer_list[self.fd_index]


if __name__ == '__main__':
    import sys
    with RFSKitRPCServer(rfs_addr='192.168.1.175', addr=("0.0.0.0", 10801), use_builtin_types=True) as server:
        server.register_instance(server.rfs_kit, allow_dotted_names=True)
        server.register_function(server.get_adc_data)
        server.register_function(server.clear_ad_cache)
        server.register_function(server.init_dma)
        server.register_function(server.release_dma)
        server.register_function(server.execute_command)
        server.register_function(lambda: None, name='close')

        server.register_multicall_functions()
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            sys.exit(0)
