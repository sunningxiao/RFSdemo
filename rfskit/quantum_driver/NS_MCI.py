import numpy as np
import struct

from rfskit.tools.data_unpacking import UnPackage
from rfskit.basekit import RFSKit
from rfskit.interface import DataNoneInterface, CommandTCPInterface

# 参数修改后需要执行的指令
param_cmd_map = {
    ("系统参考时钟选择",
     "ADC采样率",
     "ADC PLL使能",
     "PLL参考时钟频率",
     "ADC 抽取倍数",
     "ADC NCO频率",
     "ADC 奈奎斯特区",
     "DAC采样率",
     "DAC PLL使能",
     "PLL参考时钟频率",
     "DAC 抽取倍数",
     "DAC NCO频率",
     "DAC 奈奎斯特区",
     "ADC0增益",
     "ADC0偏置",
     "ADC0相位",
     "ADC0增益步进",
     "ADC0增益截止",
     "ADC1增益",
     "ADC1偏置",
     "ADC1相位",
     "ADC1增益步进",
     "ADC1增益截止",
     "ADC2增益",
     "ADC2偏置",
     "ADC2相位",
     "ADC2增益步进",
     "ADC2增益截止",
     "ADC3增益",
     "ADC3偏置",
     "ADC3相位",
     "ADC3增益步进",
     "ADC3增益截止",
     "ADC4增益",
     "ADC4偏置",
     "ADC4相位",
     "ADC4增益步进",
     "ADC4增益截止",
     "ADC5增益",
     "ADC5偏置",
     "ADC5相位",
     "ADC5增益步进",
     "ADC5增益截止",
     "ADC6增益",
     "ADC6偏置",
     "ADC6相位",
     "ADC6增益步进",
     "ADC6增益截止",
     "ADC7增益",
     "ADC7偏置",
     "ADC7相位",
     "ADC7增益步进",
     "ADC7增益截止",
     "DAC0增益",
     "DAC0偏置",
     "DAC0相位",
     "DAC0衰减步进",
     "DAC0衰减截止",
     "DAC1增益",
     "DAC1偏置",
     "DAC1相位",
     "DAC1衰减步进",
     "DAC1衰减截止",
     "DAC2增益",
     "DAC2偏置",
     "DAC2相位",
     "DAC2衰减步进",
     "DAC2衰减截止",
     "DAC3增益",
     "DAC3偏置",
     "DAC3相位",
     "DAC3衰减步进",
     "DAC3衰减截止",
     "DAC4增益",
     "DAC4偏置",
     "DAC4相位",
     "DAC4衰减步进",
     "DAC4衰减截止",
     "DAC5增益",
     "DAC5偏置",
     "DAC5相位",
     "DAC5衰减步进",
     "DAC5衰减截止",
     "DAC6增益",
     "DAC6偏置",
     "DAC6相位",
     "DAC6衰减步进",
     "DAC6衰减截止",
     "DAC7增益",
     "DAC7偏置",
     "DAC7相位",
     "DAC7衰减步进",
     "DAC7衰减截止"): '初始化',
    ("基准PRF周期",
     "基准PRF数量"): '内部PRF产生',
}


class Driver:
    wave_file_name = 'wave_cache_file.dat'
    recv_block_size = 1024

    def __init__(self):
        self.rfs_kit = RFSKit(auto_load_icd=True,
                              auto_write_file=False,
                              cmd_interface=CommandTCPInterface,
                              data_interface=DataNoneInterface)
        self.data_interface_class = DataNoneInterface
        self.cmd_interface_class = CommandTCPInterface

    def open(self, ipaddr: str, timeout=5):
        """
        输入IP打开设备，配置默认超时时间为5秒
        打开设备时配置RFSoC采样时钟，采样时钟以参数定义

        :param ipaddr: RFS的ip地址
        :param timeout: 指令发送超时时间
        """
        # 修改指令interface的目标ip地址
        self.rfs_kit.close()
        self.cmd_interface_class._target_id = ipaddr
        self.cmd_interface_class._timeout = timeout
        # 接收数据时本机为tcp server端
        # 修改数传interface的本地端口，存在一个此端口跟随rfsoc的ip改变的规则
        # 例如rfsoc的ip为192.168.1.171，则接收数据的本地端口为7001
        # if len(ipaddr) >= 12 and re.match(ip_match, ipaddr):
        #     _port = ipaddr.split('.')[3][-2:]
        #     _port = int(_port[0] + '00' + _port[1])
        #     self.data_interface_class._local_port = _port

        self.rfs_kit = RFSKit(auto_load_icd=True,
                              auto_write_file=False,
                              cmd_interface=CommandTCPInterface,
                              data_interface=DataNoneInterface)
        # 此时会连接rfsoc的指令接收tcp server
        self.rfs_kit.start_command()
        # 系统开启前必须进行过一次初始化
        self.rfs_kit.execute_command('初始化')

    def close(self):
        """
        关闭设备
        """
        self.rfs_kit.close()

    def set(self, name, value, channel=1):
        """
        设置设备属性
        :param name: 属性名
                "Waveform"| "Amplitude" | "Offset"| "Output"
        :param value: 属性值
                "Waveform" --> 1d np.ndarray & -1 <= value <= 1
                "Amplitude"| "Offset"| "Phase" --> float    dB | dB | °
                “PRFNum”   采用内部PRF时，可以通过这个参数控制开启后prf的数量
                "Output" --> bool
        :param channel：通道号
        """
        channel = channel - 1
        self.rfs_kit.set_param_value('DAC通道选择', channel)
        if name == 'Waveform':
            with open(self.wave_file_name, 'wb') as fp:
                fp.write(value)
            self.rfs_kit.execute_command('DAC数据更新', file_name=self.wave_file_name)
            param_name = f'DAC{channel}门宽'
            sample_rate = 6  #GHz
            self.rfs_kit.set_param_value(param_name, len(value)/sample_rate)
            self.rfs_kit.execute_command('DAC配置')
        elif name == 'Delay':
            param_name = f'DAC{channel}延迟'
            self.rfs_kit.set_param_value(param_name, value)
            self.rfs_kit.execute_command('DAC配置')
        elif name == 'AWG':
            # value = {'period': xx(ns), 'count': xxx}

            self.rfs_kit.set_param_value('基准PRF周期', value['period'])
            self.rfs_kit.set_param_value('基准PRF数量', value['count'])
            self.rfs_kit.execute_command('内部PRF产生')

        elif name == 'Output':
            param_name = f'DAC{channel}使能'
            tmp = 1 if value else 0
            self.rfs_kit.execute_command(param_name, tmp)
        elif name == 'Reset':
            self.rfs_kit.execute_command('复位')

        else:
            # 参数名透传，直接根据icd.json中的参数名配置对应值
            # 如果在param_cmd_map中找到了对应参数配置后要执行的指令，则执行相应指令
            self.rfs_kit.set_param_value(name, value)
            for params, cmd in param_cmd_map.items():
                if name in params:
                    self.rfs_kit.execute_command(cmd)

    def get(self, name, channel=1):
        """
        查询设备属性，获取数据

        """
        if name == 'Data':
            # 返回快视数据
            return self.__get_adc_data(channel)
        elif name == 'Amplitude':
            param_name = f'DAC{channel}增益'
            return self.rfs_kit.get_param_value(param_name)
        elif name == 'Offset':
            param_name = f'DAC{channel}偏置'
            return self.rfs_kit.get_param_value(param_name)
        elif name == 'Phase':
            param_name = f'DAC{channel}相位'
            return self.rfs_kit.get_param_value(param_name)
        else:
            return self.rfs_kit.get_param_value(name)

    def __get_adc_data(self, channel=0) -> np.ndarray:
        """
        通过网络获取一包数据

        :param channel: 通道号
        :return:
        """
        # 下发指令
        self.rfs_kit.execute_command('ADC数据获取', need_feedback=False)
        # 判断反馈指令长度
        _feedback = self.rfs_kit.cmd_interface.recv_cmd(16)
        total_length = struct.unpack('I', _feedback[12:])[0] - 16
        recv_length = 0
        _data = b''
        # 接收全部反馈数据
        # 每次接收一个self.recv_block_size
        while total_length-recv_length > self.recv_block_size:
            _data += self.rfs_kit.cmd_interface.recv_cmd(self.recv_block_size)
            recv_length += self.recv_block_size
        else:
            # 收尾
            _data += self.rfs_kit.cmd_interface.recv_cmd(total_length-recv_length)
            recv_length += total_length-recv_length
        # 解包获取对应通道的数据
        if recv_length == total_length:
            data = UnPackage.channel_data_filter(_data, [0], [channel])
            return data[0][0][channel]


if __name__ == '__main__':
    # 导入一个生成随机数字信号的函数
    from rfskit.example_codes.random_digital_signal import random_gen

    driver = Driver()
    driver.open('127.0.0.1')

    for i in range(8):
        driver.set('Waveform', random_gen(40, '16', 40), channel=i)
        driver.set('Amplitude', 3, channel=i)
        driver.set('Offset', 3, channel=i)

    driver.set('Output', True)
