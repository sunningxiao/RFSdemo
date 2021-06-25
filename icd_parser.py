import json
import os
import struct
import time
from netconn import CommandTCPServer, DataTCPServer
from sim_ctl import sim_connect
from utils import simulation, solve_exception
from data_solve import DataSolve, us_signal


from printLog import *

file_context_flag = '__file__'
file_length_flag = '__filelength__'
COMMAND_LENGTH = slice(12, 16)

_fmt_mode = "="  # pack/unpack 大小端模式

value_type = {
    "uint8": "B",
    "int8": "b",
    "uint16": "H",
    "int16": "h",
    "uint32": "I",
    "int32": "i",
    "float": "f",
    "double": "d"
}

value_python = {
    "uint8": int,
    "int8": int,
    "uint16": int,
    "int16": int,
    "uint32": int,
    "int32": int,
    "float": float,
    "double": float
}

type_size = {
    "uint8": 1,
    "int8": 1,
    "uint16": 2,
    "int16": 2,
    "uint32": 4,
    "int32": 4,
    "float": 4,
    "double": 8
}

feedback_value_fmt = {
    "uint8": "%#x",
    "int8": "%d",
    "uint16": "%#x",
    "int16": "%d",
    "uint32": "%#x",
    "int32": "%d",
    "float": "%f",
    "double": "%f"
}


class ICDParams:
    def __init__(self, file_name='icd.json'):
        self._connected = False
        self._file_name = file_name
        self.icd_data = {}
        self.button = {}
        self.param = {}
        self.command = {}
        self.after_connection = []
        self.data_server = self.server = None
        self.recv_header = b''
        self.data_solve = None

    @simulation(simulation_ctl, sim_connect)
    @solve_exception()
    def connect(self, ip=None, pthread=None):
        if ip is not None:
            CommandTCPServer._conn_ip = ip
            DataTCPServer._conn_ip = ip
        self.data_server = DataTCPServer()
        self.server = CommandTCPServer()
        self.data_solve = DataSolve(self.data_server)
        # self.data_solve.start_solve()
        self._connected = True
        for command in self.after_connection:
            self.send_command(command)
        return True

    def load_icd(self, reload=False):
        file_path = self._file_name.split('.')[0] + '_run.json' \
            if os.path.isfile(self._file_name.split('.')[0] + '_run.json') and not reload \
            else self._file_name
        with open(file_path, 'r', encoding='utf-8') as fp:
            try:
                self.icd_data = json.load(fp)
            except json.decoder.JSONDecodeError as e:
                printWarning('icd.json文件不可用')
        try:
            self.button = self.icd_data['button']
            self.param = self.icd_data['param']
            self.command = self.icd_data['command']
            self.after_connection: list = self.icd_data['after_connection']
            CommandTCPServer._remote_port = self.icd_data['remote_command_port']
            CommandTCPServer._conn_ip = self.icd_data['remote_ip']
            DataTCPServer._local_port = self.icd_data['remote_data_port']
            DataTCPServer._conn_ip = self.icd_data['remote_ip']
            self.recv_header = struct.pack(_fmt_mode + 'I', int(self.icd_data['recv_header'], 16))
            printInfo('参数载入成功')
        except Exception as e:
            printException(e, f'{file_path}不可用')

    def save_icd(self, path=''):
        path = path + '\\' if path else path
        with open(path + self._file_name.split('.')[0] + '_run.json', 'w', encoding='utf-8') as fp:
            # 按utf-8的格式格式化并写入文件
            json.dump(self.icd_data, fp, ensure_ascii=False, indent=4)
            printInfo('参数保存成功')
        return True

    def get_param(self, param_name: str, default=0, fmt_type=int):
        param = self.param.get(param_name, None)
        if param is None:
            printWarning(f'未找到参数：{param_name}')
            self.param.update({param_name: [param_name, 'uint32', default]})
            return fmt_type(default)
        return fmt_type(param[2])

    def set_param(self, param_name: str, value, fmt_type=int):
        param = self.param.get(param_name, [param_name, 'uint32', value])
        if isinstance(value, str) and value.startswith('0x') and param[1] not in ['float', 'double']:
            param[2] = value
        else:
            param[2] = value_python[param[1]](value)
        self.param.update({param_name: param})

    @simulation(simulation_ctl, sim_connect)
    def send_command(self, button_name: str,
                     need_feedback=True, file_name=None, check_feedback=True,
                     callback=lambda *args: True, wait: int = 0) -> bool:
        if not self._connected:
            printWarning('未连接板卡')
            return False
        self.server: CommandTCPServer
        _commands = self.button.get(button_name, None)
        if _commands is None:
            printWarning(f'没有此按钮')
            return False
        for _command_name in _commands:
            if _command_name not in self.command:
                printWarning(f'指令{_command_name}未找到')
                return False
            command_bak = command = self._fmt_command(_command_name, file_name)
            command_len = len(command)
            try:
                while command_len > 0:
                    sent = self.server.send(command)
                    command = command[sent:]
                    command_len -= sent
            except Exception as e:
                printException(e, f'指令({_command_name})发送失败')
                return False
            printInfo(f'指令({_command_name})已发送')
            try:
                if need_feedback:
                    time.sleep(wait)
                    _feedback = self.server.recv()
                    if check_feedback:
                        if not _feedback.startswith(self.recv_header):
                            printWarning('返回指令包头错误')
                            return False
                        if command_bak[4:8] != _feedback[4:8]:
                            printWarning('返回指令ID错误')
                            return False
                        _feedback = struct.unpack(_fmt_mode + 'IIIII', _feedback)
                        if _feedback[4] != 0:
                            printWarning('指令成功下发，但执行失败')
                            return False
            except Exception as e:
                printException(e, f'指令({_command_name})无应答')
                return False
        printColor(f'成功执行指令{_commands}', 'green')
        # 优化回调机制，防止出现在其他线程操作qtimer的情况
        us_signal.status_trigger.emit((1, 3, callback))
        return True

    def _fmt_command(self, command_name, file_name=None) -> bytes:
        file_data = command = b''
        file_length = 0
        if isinstance(file_name, str):
            file_data, file_length = self.__get_file(file_name)
        try:
            for register in self.command[command_name]:
                if isinstance(register, list):
                    value, _fmt = self.__fmt_register(register)
                    command += struct.pack(_fmt_mode + _fmt, value)
                elif isinstance(register, str):
                    if register == file_context_flag:
                        command += file_data
                    elif register == file_length_flag:
                        command += struct.pack(_fmt_mode + 'I', file_length)
                    elif register in self.param:
                        value, _fmt = self.__fmt_register(self.param[register])
                        command += struct.pack(_fmt_mode + _fmt, value)
                    else:
                        printWarning(f'指令({command_name})的({register})不存在')
                else:
                    printWarning(f'指令({command_name})的({register})格式不正确')
        except Exception as e:
            printException(e, '指令转码失败')
        assert len(command) >= 16, f'指令({command_name})不正确'
        return command[0: 12] + struct.pack(_fmt_mode + 'I', len(command)) + command[16:]

    @staticmethod
    def __fmt_register(register: list):
        try:
            value = register[2]
            if isinstance(value, str) and value.startswith('0x'):
                value = int(value, 16)
            fmt_str = value_type[register[1]]
            return value_python[register[1]](value), fmt_str
        except Exception as e:
            printException(e, f'寄存器({register[0]})有误')
        return 0, 'I'

    @staticmethod
    def __get_file(file_name):
        try:
            with open(file_name, 'rb') as fp:
                data = fp.read()
            return data, len(data)
        except Exception as e:
            printException(e, '文件读取失败')
        return b'', 0
