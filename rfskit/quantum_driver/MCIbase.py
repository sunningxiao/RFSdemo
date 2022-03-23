import numpy as np
import struct
from typing import List

from rfskit.tools.data_unpacking import UnPackage
from rfskit.basekit import RFSKit
from rfskit.interface import DataNoneInterface, CommandTCPInterface
from waveforms import sin, cos
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


def coff_para(t=None, freq=200e6):
    if t is None:
        t = []
    coeff_list_I = np.array(cos(2*np.pi*(freq))(t))
    coeff_list_Q = np.array(sin(2*np.pi*(freq))(t))
    return coeff_list_I+1j*coeff_list_Q


def getTraceIQ(y,coff_para=np.asarray([])):
    return np.abs(y).dot(coff_para.T)/len(y)


class Quantity(object):
    def __init__(self, name: str, value=None, ch: int = 1, unit: str = ''):
        self.name = name
        self.default = dict(value=value, ch=ch, unit=unit)


class DriverAchieve:
    wave_file_name = 'wave_cache_file.dat'
    recv_block_size = 1024

    quants: List[Quantity] = []

    def __init__(self, addr: str = '', timeout: float = 3.0, **kw):
        self.model = 'NS_MCI'  # 默认为设备名字
        self.ADrate = 4e9  # ns
        self.DArate = 6e9  # ns
        self.srate = self.DArate  # 设备采样率

        self.rfs_kit = RFSKit(auto_load_icd=True,
                              auto_write_file=False,
                              cmd_interface=CommandTCPInterface,
                              data_interface=DataNoneInterface)
        self.handle = self.rfs_kit
        self.addr = addr
        self.timeout = timeout

        self.data_interface_class = DataNoneInterface
        self.cmd_interface_class = CommandTCPInterface
        self.Freqlist = {i:[] for i in range(8)}
        self.Cofflist = {i:[] for i in range(8)}
        self.PointNumber = 1000

    def open(self, **kw):
        self._open()

    def close(self, **kw):
        """
        关闭设备
        """
        self.rfs_kit.close()

    # -----------------------------------------------------------------

    def _open(self):
        """
        输入IP打开设备，配置默认超时时间为5秒
        打开设备时配置RFSoC采样时钟，采样时钟以参数定义

        :param ipaddr: RFS的ip地址
        :param timeout: 指令发送超时时间
        """
        # 修改指令interface的目标ip地址
        self.rfs_kit.close()
        self.cmd_interface_class._target_id = self.addr
        self.cmd_interface_class._timeout = self.timeout

        self.rfs_kit = RFSKit(auto_load_icd=True,
                              auto_write_file=False,
                              cmd_interface=CommandTCPInterface,
                              data_interface=DataNoneInterface)
        # 此时会连接rfsoc的指令接收tcp server
        self.rfs_kit.start_command()
        # 系统开启前必须进行过一次初始化
        self.rfs_kit.execute_command('初始化')
        self.rfs_kit.execute_command('DAC配置')
        self.rfs_kit.execute_command('ADC配置')

    def set(self, name, value=0, channel=1):
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
            bit = 16
            value = (2 ** (bit - 1) - 1) * value
            value = value.astype('int16')
            with open(self.wave_file_name, 'wb') as fp:
                fp.write(value)
            self.rfs_kit.execute_command('DAC数据更新', file_name=self.wave_file_name)
            '''
            param_name = f'DAC{channel}门宽'
            sample_rate = 6  #GHz
            self.rfs_kit.set_param_value(param_name, len(value)/sample_rate)
            print('数据时长', len(value)/sample_rate, 'ns')
            self.rfs_kit.execute_command('DAC配置')
            '''
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
            if value == 'OFF':
                value = False
            elif value == 'ON':
                value
            tmp = 1 if value else 0
            self.rfs_kit.execute_command(param_name, tmp)
        elif name == 'Reset':
            self.rfs_kit.execute_command('复位')
        elif name == 'MixMode':
            self.rfs_kit.set_param_value('DAC 奈奎斯特区', value)
            self.rfs_kit.execute_command('初始化')
        elif name == 'RefClock':
            tmp = 4
            if value == 'out':
                tmp = 3
            self.rfs_kit.set_param_value('系统参考时钟选择', tmp)
            self.rfs_kit.execute_command('初始化')
        elif name == 'PointNumber':
            param_name = f'ADC{channel}门宽'
            self.rfs_kit.set_param_value(param_name, value)
            self.rfs_kit.execute_command('ADC配置')
            # 转为16ns倍数对应的点数
            tmp = self.ADrate * 1e-9 * value
            self.PointNumber = int(tmp//16*16)
        elif name == 'TriggerDelay':
            param_name = f'ADC{channel}延迟'
            self.rfs_kit.set_param_value(param_name, value)
            self.rfs_kit.execute_command('ADC配置')
        elif name == 'Freqlist':
            self.Freqlist[channel] = value
            tm = np.linspace(0, (self.PointNumber - 1) * (1/self.ADrate), self.PointNumber)
            self.Cofflist[channel] = []
            for i in range(len(value)):
                self.Cofflist[channel].append(coff_para(tm, value[i]))
                param_name = f'解调频率{i}'
                self.rfs_kit.set_param_value(param_name, value[i])
            self.rfs_kit.set_param_value('解调通道', channel)
            self.rfs_kit.execute_command('量子解调配置')

        else:
            # 参数名透传，直接根据icd.json中的参数名配置对应值
            # 如果在param_cmd_map中找到了对应参数配置后要执行的指令，则执行相应指令
            self.rfs_kit.set_param_value(name, value)
            for params, cmd in param_cmd_map.items():
                if name in params:
                    self.rfs_kit.execute_command(cmd)

    def setValue(self, name, value=0, channel=1):
        self.set(name, value, channel)

    def get(self, name, channel=1):
        """
        查询设备属性，获取数据

        """
        channel = channel - 1
        if name == 'TraceIQ':
            # 返回快视数据
            self.rfs_kit.set_param_value('获取内容', 0)
            return self.__get_adc_data(channel)
        elif name == 'IQ':
            self.rfs_kit.set_param_value('获取内容', 1)
            return self.__get_adc_data(channel, False)
        elif name == 'SIQ':
            self.rfs_kit.set_param_value('获取内容', 0)
            data = self.__get_adc_data(channel)
            sdlist = []
            for i in range(len(self.Cofflist[channel])):
                sd = [getTraceIQ(data[j, :], self.Cofflist[channel][i]) for j in range(len(data))]
                sdlist.append(sd)
            return sdlist
        # elif name == 'Waveform':
        #     return self.__get_adc_data(channel, True)

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

    def getValue(self, name, channel=1):
        self.get(name, channel)

    def __get_adc_data(self, channel=0, unpack=True) -> np.ndarray:
        """
        通过网络获取一包数据

        :param channel: 通道号
        :return:
        """
        # 下发指令
        self.rfs_kit.execute_command('ADC数据获取', need_feedback=False)
        # 判断反馈指令长度
        _feedback = self.rfs_kit.cmd_interface.recv_cmd(20)
        total_length = struct.unpack('I', _feedback[12:16])[0] - 20
        if total_length == 0:
            print('未获取到数据')
            return
        recv_length = 0
        _data = b''
        # 接收全部反馈数据
        # 每次接收一个self.recv_block_size
        while total_length-recv_length > self.recv_block_size:
            _data += self.rfs_kit.cmd_interface.recv_cmd(self.recv_block_size)
            recv_length = len(_data)
        else:
            # 收尾
            while len(_data) != total_length:
                _data += self.rfs_kit.cmd_interface.recv_cmd(total_length-len(_data))
            recv_length = len(_data)
        # 解包获取对应通道的数据
        print('接收数据字节', total_length)
        print('接收数据长度', total_length/2)
        print('recv长度', recv_length)
        print('_data长度', len(_data))
        if recv_length == total_length:
            # np.save('./adc_data.npy',_data)
            # return data
            if unpack:
                data = UnPackage.channel_data_filter(_data, [], [channel])

                # 将解包的结果转为一整个np.ndarray shape为 包数*单通道采样点数
                data = np.array([data[0][frame_idx][channel] for frame_idx in data[0]])
                return data
            else:
                data = np.frombuffer(_data, dtype='int32')
                return data, data.reshape(int(len(data)/2),2).T
        else:
            print('数量接收不匹配')
            return
