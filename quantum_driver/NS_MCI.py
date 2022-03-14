import re

from core import RFSKit
from core.interface import DataTCPInterface, CommandTCPInterface

ip_match = r'^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.' \
           r'(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$'

# 参数修改后需要执行的指令
param_cmd_map = {
    ("ADC0增益",
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
     "DAC7衰减截止"): 'QMC配置',
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
     "DAC 奈奎斯特区"): 'RF配置',
}


class Driver:
    wave_file_name = 'wave_cache_file.dat'

    def __init__(self):
        self.rfs_kit = RFSKit(auto_load_icd=True,
                              auto_write_file=True,
                              cmd_interface=CommandTCPInterface,
                              data_interface=DataTCPInterface)
        self.data_interface_class = DataTCPInterface
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
        if len(ipaddr) >= 12 and re.match(ip_match, ipaddr):
            _port = ipaddr.split('.')[3][-2:]
            _port = int(_port[0] + '00' + _port[1])
            self.data_interface_class._local_port = _port

        self.rfs_kit = RFSKit(auto_load_icd=True,
                              auto_write_file=True,
                              cmd_interface=CommandTCPInterface,
                              data_interface=DataTCPInterface)
        # 此时会连接rfsoc的指令接收tcp server
        self.rfs_kit.start_command()
        # 系统开启前必须进行过一次RF配置
        self.rfs_kit.execute_command('RF配置')

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
        if name == 'Waveform':
            with open(self.wave_file_name, 'wb') as fp:
                fp.write(value)
            self.rfs_kit.set_param_value('DDS_RAM', channel)
            self.rfs_kit.execute_command('波形装载', file_name=self.wave_file_name)
        elif name == 'Amplitude':
            param_name = f'DAC{channel}增益'
            self.rfs_kit.set_param_value(param_name, value)
            self.rfs_kit.execute_command('QMC配置')
        elif name == 'Offset':
            param_name = f'DAC{channel}偏置'
            self.rfs_kit.set_param_value(param_name, value)
            self.rfs_kit.execute_command('QMC配置')
        elif name == 'Phase':
            param_name = f'DAC{channel}相位'
            self.rfs_kit.set_param_value(param_name, value)
            self.rfs_kit.execute_command('QMC配置')
        elif name == 'Output':
            # 目前没有各个通道的单独开关
            # 八个通道统一启停
            if value:
                self.rfs_kit.start_stream()
                self.rfs_kit.execute_command('QMC配置')
                # self.rfs_kit.execute_command('DDS配置')
                self.rfs_kit.execute_command('系统开启')
            else:
                self.rfs_kit.execute_command('系统停止')
                self.rfs_kit.stop_stream()

        elif name == 'PRFNum':
            # 采用内部PRF时，可以通过这个参数控制开启后prf的数量
            self.rfs_kit.set_param_value('基准PRF数量', value)

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
            data = self.rfs_kit.view_stream_data()
            # 这里也可以将数据解包后返回指定通道，未添加
            return data
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


if __name__ == '__main__':
    # 导入一个生成随机数字信号的函数
    from example_codes.random_digital_signal import random_gen

    driver = Driver()
    driver.open('127.0.0.1')

    for i in range(8):
        driver.set('Waveform', random_gen(40, '16', 40), channel=i)
        driver.set('Amplitude', 3, channel=i)
        driver.set('Offset', 3, channel=i)

    driver.set('Output', True)
