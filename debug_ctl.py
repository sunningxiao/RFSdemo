from cmd_package import *
from sim_ctl import *
from printLog import *
from utils import simulation
from netconn import MessageUdpServer, CommandUdpServer
import binascii
import datetime
import numpy as np
import threading


class DebugControl:

    def __init__(self, update_record_status=lambda x: x):
        self._record_status_event = threading.Event()
        # threading.Thread(target=update_record_status, args=(self._record_status_event, ), daemon=True).start()
        self.cmd_udp_server = CommandUdpServer()
        self.message_udp_server = MessageUdpServer()

    def start_get_record_status(self):
        self._record_status_event.set()

    def stop_get_record_status(self):
        self._record_status_event.clear()

    @simulation(simulation_ctl, sim_connect)
    def connect(self, pthread=None):
        return connect(self.cmd_udp_server)

    @simulation(simulation_ctl, sim_start_record)
    def start_record(self, params: list, pthread=None):
        """ 采集启动 """
        # 获取当前年 月日 时分
        str_time = datetime.datetime.now().strftime("%Y %m%d %H%M")
        str_time = [int(i) for i in str_time.split()]
        # str_time = [int(binascii.b2a_hex(i.encode())) for i in str_time.split()]
        return start_record(self.cmd_udp_server, *params, str_time)

    @simulation(simulation_ctl, sim_stop_record)
    def stop_record(self, pthread=None):
        """ 采集停止 """
        return stop_record(self.cmd_udp_server)

    @simulation(simulation_ctl, sim_update_status)
    def record_status(self):
        """ 更新状态与回波数据 """
        try:
            result = status_echo_data(self.message_udp_server)
            if not isinstance(result, tuple):
                return False, 0, 0
            t, info = result
            state = {}
            echo_data = []
            if t:
                state = {'state': info[0], 'mode': info[1], 'chnl_count': info[2], 'left': info[3],
                         'bandwidth': info[4],
                         'round_number': info[-2], 'fpga_temperature': info[-1]}
            else:
                echo_data = info
            return True, state, echo_data
        except AssertionError as e:
            printWarning(e)
        except Exception as e:
            printException(e)

    @simulation(simulation_ctl, sim_update_coe)
    def update_coe(self, filename, coe_count, pthread=None):
        data_gen = self._read_file(filename, coe_count, pthread)
        return filtering_factor_issue(self.cmd_udp_server, coe_count, data_gen)

    @staticmethod
    def _read_file(filename, coe_count, pthread):
        block_size = send_block_size // 4
        coe_size = coe_count * 2
        left_size = coe_size % block_size
        loop_count = coe_size // block_size + 1 if left_size else coe_size // block_size

        with open(filename, "rb") as file:
            for i in range(loop_count):
                if left_size and i == loop_count - 1:
                    block_size = left_size
                data = np.fromfile(file, dtype="f4", count=block_size)
                if pthread.stopped() or not len(data):
                    break
                flag = yield data
                pthread.updatePGvalue((i + 1) / loop_count * 100)
                if flag:
                    yield
                    break
