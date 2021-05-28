import json

from printLog import *


class ICDParams:
    def __init__(self, file_name='icd.json'):
        self._file_name = file_name
        self.icd_data = {}
        self.button = {}
        self.param = {}
        self.command = {}

    def load_icd(self):
        with open(self._file_name, 'r', encoding='utf-8') as fp:
            try:
                self.icd_data = json.load(fp)
            except json.decoder.JSONDecodeError as e:
                printWarning('icd.json文件不可用')
        self.button = self.icd_data['button']
        self.param = self.icd_data['param']
        self.command = self.icd_data['command']

    def save_icd(self):
        with open(self._file_name.split('.')[0] + '_run.json', 'w', encoding='utf-8') as fp:
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
        param[2] = fmt_type(value)
        self.param.update({param_name: param})
