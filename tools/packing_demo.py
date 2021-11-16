import json
import os
import struct
import time

import pandas as pd

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
    "double": float,
    "file": str
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


class ICDParams:
    def __init__(self, file_name='icd.json'):
        self._connected = False
        self._file_name = file_name
        self.icd_data = {}
        self.button = {}
        self.param = {}
        self.command = {}
        self.sequence = {}
        self.after_connection = []
        self.data_server = self.server = None
        self.recv_header = b''
        self.data_solve = None

    def load_icd(self, reload=False):
        file_path = self._file_name.split('.')[0] + '_run.json' \
            if os.path.isfile(self._file_name.split('.')[0] + '_run.json') and not reload \
            else self._file_name
        with open(file_path, 'r', encoding='utf-8') as fp:
            try:
                self.icd_data = json.load(fp)
            except json.decoder.JSONDecodeError as e:
                print('icd.json文件不可用')
        self.button = self.icd_data['button']
        self.param = self.icd_data['param']
        self.command = self.icd_data['command']
        self.sequence = self.icd_data['sequence']
        self.recv_header = struct.pack(_fmt_mode + 'I', int(self.icd_data['recv_header'], 16))

    def save_icd(self, path=''):
        path = path + '\\' if path else path
        with open(path + self._file_name.split('.')[0] + '_run.json', 'w', encoding='utf-8') as fp:
            # 按utf-8的格式格式化并写入文件
            json.dump(self.icd_data, fp, ensure_ascii=False, indent=4)
            print('参数保存成功')
        return True

    def get_param(self, param_name: str, default=0, fmt_type=int):
        param = self.param.get(param_name, None)
        if param is None:
            print(f'未找到参数：{param_name}')
            self.param.update({param_name: [param_name, 'uint32', default]})
            return fmt_type(default)
        return fmt_type(param[2])

    def set_param(self, param_name: str, value, fmt_type=int):
        param = self.param.get(param_name, [param_name, 'uint32', value])
        if isinstance(value, str) and value.startswith('0x'):
            param[2] = int(value, 16)
        elif isinstance(value, str) and value.startswith('0b'):
            param[2] = int(value, 2)
        else:
            param[2] = value_python[param[1]](value)
        self.param.update({param_name: param})

    def send_command(self, button_name: str,
                     need_feedback=True, file_name=None, check_feedback=True,
                     callback=lambda *args: True, wait: int = 0) -> bool:
        pass

    def _fmt_command(self, command_name, file_name=None) -> bytes:
        file_data = command = b''
        file_length = 0
        if isinstance(file_name, str):
            file_data, file_length = self.__get_file(file_name)
        try:
            target_bytes = b''
            if command_name in self.sequence:
                sequence_data: pd.DataFrame = pd.read_excel(file_name)
                sequence_cmd = self.sequence[command_name]
                for row in range(sequence_data.shape[0]):
                    for register in sequence_cmd:
                        if isinstance(register, str):
                            _reg = self.param.get(register, None)
                            assert _reg, f'未找到参数{register}'
                            if register in sequence_data:
                                value = sequence_data[register][row]
                            else:
                                value = _reg[2]
                        else:
                            _reg = register
                            value = _reg[2]
                        value, _fmt = self.__fmt_register(_reg, value)
                        target_bytes += struct.pack(_fmt_mode + _fmt, value)

            for register in self.command[command_name]:
                if isinstance(register, list):
                    value, _fmt = self.__fmt_register(register, register[2])
                    command += struct.pack(_fmt_mode + _fmt, value)
                elif isinstance(register, str):
                    if register == file_context_flag:
                        command += file_data
                    elif register == file_length_flag:
                        command += struct.pack(_fmt_mode + 'I', file_length)
                    elif register in self.param:
                        value, _fmt = self.__fmt_register(self.param[register], self.param[register][2])
                        command += struct.pack(_fmt_mode + _fmt, value)
                    elif register == f'{{{{{command_name}}}}}':
                        command += target_bytes
                    else:
                        print(f'指令({command_name})的({register})不存在')
                else:
                    print(f'指令({command_name})的({register})格式不正确')
        except Exception as e:
            print(e, '指令转码失败')
        assert len(command) >= 16, f'指令({command_name})不正确'
        return command[0: 12] + struct.pack(_fmt_mode + 'I', len(command)) + command[16:]

    @staticmethod
    def __fmt_register(register: list, value):
        try:
            if isinstance(value, str) and value.startswith('0x'):
                value = int(value, 16)
            if isinstance(value, str) and value.startswith('0b'):
                value = int(value, 2)
            if len(register) > 3:
                # 发送时做参数计算
                x = value
                value = eval(register[-1])
            fmt_str = value_type[register[1]]
            return value_python[register[1]](value), fmt_str
        except Exception as e:
            print(e, f'寄存器({register[0]})有误')
        return 0, 'I'

    @staticmethod
    def __get_file(file_name):
        try:
            with open(file_name, 'rb') as fp:
                data = fp.read()
            return data, len(data)
        except Exception as e:
            print(e, '文件读取失败')
        return b'', 0


if __name__ == '__main__':
    sequence = pd.read_excel('工作参数配置.xlsx')
    icd = ICDParams()
    icd.load_icd()
    chnl_id = input('请输入目标通道号:\n')
    file_name = input('请输入excel文件名:\n')
    icd.set_param('工作参数配置槽位号', chnl_id)
    data = icd._fmt_command('工作参数配置', file_name)
    with open(f'{file_name.split(".")[0]}_chnl{chnl_id}_{len(sequence)}_{time.strftime("%Y-%m-%d_%H-%M-%S")}.seq', 'wb') as fp:
        fp.write(data)
    print('生成成功')
    input('按回车退出程序')
