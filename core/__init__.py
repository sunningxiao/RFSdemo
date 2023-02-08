from typing import Union, IO, List
import time
import struct
from threading import Event
import numpy as np

from core.data_solve import DataSolve
from core import interface
from core.icd_parser import ICDParams

from tools.printLog import *
from tools.utils import SingletonType, APIBaseType

__all__ = ['RFSKit']


class __RFSDevelopKit(APIBaseType, SingletonType):
    _METHODS = frozenset({
        "load_icd", "save_icd", "execute_command", "set_param_value", "get_param_value",
        "start_command", "start_stream", "stop_stream", "close",
        "append_stream_data", "view_stream_data", "get_stream_data", "upload_status", "download_status",
    })
    _ATTRS = {}


class RFSKit(metaclass=__RFSDevelopKit, _root=True):
    def __init__(self, *args, **kwargs):
        """
        RFS二次开发Python套件

        :param args:
        :param kwargs:
        """

        self.icd_param = ICDParams()
        self._stop_event = Event()
        self._connected = False
        self.__icd_loaded = False

        if kwargs.get('auto_load_icd', False):
            self.load_icd()
        self._auto_write_file = kwargs.get('auto_write_file', True)
        cmd_interface = kwargs.get('cmd_interface', interface.CommandTCPInterface)
        data_interface = kwargs.get('data_interface', interface.DataTCPInterface)

        self.cmd_interface = cmd_interface()
        self.data_interface = data_interface()
        self._data_solve = DataSolve(self, self.data_interface, self._stop_event)

    def close(self):
        self._stop_event.set()
        self.save_icd()
        self.cmd_interface.close()
        self.data_interface.close()

    def load_icd(self, reload=False):
        self.__icd_loaded = self.icd_param.load_icd(reload)
        return self.__icd_loaded

    def save_icd(self, path=''):
        return self.icd_param.save_icd(path)

    def start_command(self, target=None, target_param=tuple()):
        try:
            self.cmd_interface.accept(target, *target_param)

            self._connected = True
            for command in self.icd_param.after_connection:
                self.execute_command(command)
            return True
        except ConnectionRefusedError as e:
            return False

    def start_stream(self, auto_write_file=None, filepath=None, write_file=True, file_name=''):
        """
        开启上下行流程

        :return:
        """
        if auto_write_file is not None:
            self._auto_write_file = auto_write_file
        return self._data_solve.start_solve(self._auto_write_file, filepath, write_file, file_name)

    def stop_stream(self):
        self._stop_event.set()
        # self.save_icd()
        # self.cmd_interface.close()
        self.data_interface.close()

    def view_stream_data(self) -> Union[bool, np.ndarray]:
        """
        获取最新的一包DMA数据，且不对上行队列造成影响

        :return:
        """
        return self.data_interface.lookup_data()

    def get_stream_data(self) -> Union[bool, np.ndarray]:
        """
        从上行队列中获取一包DMA数据

        :return:
        """
        if self._auto_write_file:
            raise RuntimeError('开启自动写盘，此接口不可用')
        return self.data_interface.read_data()

    def upload_status(self):
        """
        获取上行状态信息

        :return: list(上行速度，写盘速度，上行数据量)
        """
        return self._data_solve.upload_status()

    def download_status(self):
        return [0]

    def execute_command(self, button_name: str,
                        need_feedback=True, file_name=None, check_feedback=True,
                        callback=lambda *args: True, wait: int = 0):
        """
        发送指令组

        :param button_name:
        :param need_feedback:
        :param file_name:
        :param check_feedback:
        :param callback:
        :param wait:
        :return:
        """
        status = ''
        if not self._connected:
            printWarning('未连接板卡')
            status = '未连接板卡'
            return [status, '', '']
        # self.server: CommandInterface
        _commands = self.icd_param.button.get(button_name, None)
        if _commands is None:
            printWarning(f'没有此按钮 {button_name}')
            status = f'没有此按钮 {button_name}'
            return [status, '', '']
        for _command_name in _commands:
            if _command_name not in self.icd_param.command:
                printWarning(f'指令{_command_name}未找到')
                status = f'指令{_command_name}未找到'
                return [status, '', '']
            command_bak = command = self.icd_param.fmt_command(_command_name, file_name)
            command_len = len(command)
            try:
                while command_len > 0:
                    sent = self.cmd_interface.send_cmd(command)
                    command = command[sent:]
                    command_len -= sent
                    # printColor(f'未发送{command_len}字节', 'green')
            except interface.CmdInterfaceBusy as e:
                printColor(e, 'yellow')
                status = e
                return [status, '', '']
            except Exception as e:
                printException(e, f'指令({_command_name})发送失败')
                status = f'指令({_command_name})发送失败'
                return [status, '', '']
            printInfo(f'指令({_command_name})已发送')
            try:
                if need_feedback:
                    time.sleep(wait)
                    _feedback = self.cmd_interface.recv_cmd(16)
                    _feedback_result = self.cmd_interface.recv_cmd(struct.unpack('=I', _feedback[12:16])[0]-16)
                    if check_feedback:
                        # if not _feedback.startswith(self.icd_param.recv_header):
                        #     printWarning('返回指令包头错误')
                        #     return False
                        # if command_bak[4:8] != _feedback[4:8]:
                        #     printWarning('返回指令ID错误')
                        #     return False
                        # _feedback = struct.unpack(self.icd_param.fmt_mode + 'IIIII', _feedback)
                        # if _feedback[4] != 0:
                        #     printWarning('指令成功下发，但执行失败')
                        #     return False
                        if not _feedback.startswith(self.icd_param.recv_header):
                            printWarning('返回指令包头错误')
                            status += '返回指令包头错误'
                        if command_bak[4:8] != _feedback[4:8]:
                            printWarning('返回指令ID错误')
                            status += '返回指令ID错误'
                        return [status, _feedback, _feedback_result]
            except Exception as e:
                printException(e, f'指令({_command_name})无应答')
                status = f'指令({_command_name})无应答'
                return [status, '', '']
        printColor(f'成功执行指令{_commands}', 'green')
        # # 优化回调机制，防止出现在其他线程操作qtimer的情况
        callback()
        return True

    def set_param_value(self, param_name: str, value, fmt_type=int):
        if not self.__icd_loaded:
            return False
        return self.icd_param.set_param(param_name, value, fmt_type)

    def get_param_value(self, param_name: str, default=0, fmt_type=int):
        if not self.__icd_loaded:
            return False
        return self.icd_param.get_param(param_name, default, fmt_type)

    @property
    def icd_loaded(self):
        return self.__icd_loaded
