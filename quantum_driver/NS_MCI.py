import waveforms
import numpy as np

from MCIbase import DriverAchieve, Quantity


class Driver(DriverAchieve):
    quants = [
        # 采集运行参数
        Quantity('Shot', value=1024, ch=1),  # set/get,运行次数
        Quantity('PointNumber', value=16384, unit='point'),  # set/get,AD采样点数
        Quantity('TriggerDelay', value=0, ch=1, unit='point'),  # set/get,AD采样延时
        Quantity('FrequencyList', value=[], ch=1, unit='Hz'),  # set/get,解调频率列表，list，单位Hz
        Quantity('StartCapture'),  # set,开启采集（执行前复位）
        Quantity('TraceIQ', ch=1),  # get,获取原始时域数据
                                    # 返回：array(shot, point)
        Quantity('IQ', ch=1),  # get,获取解调后数据,默认复数返回
                               # 系统参数，宏定义修改，open时下发
                               # 复数返回：array(shot,frequency)
                               # 实数返回：array(IQ,shot,frequency)

        # 任意波形发生器
        Quantity('Waveform', value=np.array([]), ch=1),  # set/get,下发原始波形数据
        Quantity('Delay', value=0, ch=1),  # set/get,播放延时
        Quantity('Output', value=True, ch=1),  # set/get,播放通道开关设置
        Quantity('GenWave', value=waveforms.Waveform(), ch=1),  # set/get, 设备接收waveform对象，根据waveform对象直接生成波形
        # set/get, 设备接收IQ分离的waveform对象列表，根据waveform对象列表直接生成波形
        Quantity('GenWaveIQ', value=[waveforms.Waveform(), waveforms.Waveform()], ch=1),

        # 内触发
        Quantity('GenerateTrig', value=1e7, unit='ns'),  # set/get,触发周期单位ns，触发数量=shot
    ]

    SystemParameter = {'MixMode': 1,  # Mix模式，1：第一奈奎斯特去； 2：第二奈奎斯特区
                       'RefClock': 'out',  # 参考时钟选择： ‘out’：外参考时钟；‘in’：内参考时钟
                       'ADrate': 4e9,  # AD采样率，单位Hz
                       'DArate': 6e9,  # DA采样率，单位Hz
                       'DAC抽取倍数': 1,  # DA内插比例，1,2,4,8
                       'DAC本振频率': 0,  # DUC本振频率，单位MHz
                       'ADC抽取倍数': 1,  # AD抽取比例，1,2,4,8
                       'ADC本振频率': 0  # DDC本振频率，单位MHz
                       }

    def __init__(self, addr: str = '', timeout: float = 10.0, **kw):
        super(Driver, self).__init__(addr, timeout, **kw)

    def open(self, **kw):
        """
        输入IP打开设备，配置默认超时时间为5秒
        打开设备时配置RFSoC采样时钟，采样时钟以参数定义
        """
        self._open()

    def close(self, **kw):
        """
        关闭设备
        """
        self._close(**kw)

    def write(self, name: str, value, **kw):
        channel = kw.get('channel', 1)
        return self.set(name, value, channel)

    def read(self, name: str, **kw):
        channel = kw.get('channel', 1)
        return self.get(name, channel)


if __name__ == '__main__':
    # 导入一个生成随机数字信号的函数
    from NS_MCI.example_codes.random_digital_signal import random_gen

    driver = Driver('127.0.0.1', 3)

    for i in range(8):
        driver.set('Waveform', random_gen(40, '16', 40), channel=i)
        driver.set('Amplitude', 3, channel=i)
        driver.set('Offset', 3, channel=i)

    driver.set('Output', True)
