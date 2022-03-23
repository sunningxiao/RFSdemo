from rfskit.quantum_driver.MCIbase import DriverAchieve, Quantity


class Driver(DriverAchieve):
    quants = [
        # 微波源(MW)
        Quantity('Frequency', value=0, ch=1, unit='Hz'),  # 频率
        Quantity('Power', value=0, ch=1, unit='dBm'),  # 功率
        Quantity('Output', value='OFF', ch=1),  # 输出开关

        # 任意波形发生器(AWG)
        Quantity('Amplitude', value=0, ch=1, unit='Vpp'),  # 振幅
        Quantity('Offset', value=0, ch=1, unit='V'),  # 偏置
        Quantity('Phase', value=0, ch=1, unit='°'),
        Quantity('AWG', value={'period': 0, 'count': 1000}, ch=1),
        Quantity('Waveform', value=[], ch=1),  # 波形

        Quantity('TraceIQ', value=[], ch=1),  # 时域采样
        Quantity('IQ', value=[], ch=1),  # 解调后数据
        Quantity('SIQ', value=[], ch=1),
        Quantity('TriggerDelay', value=0, ch=1, unit='point'),  # 采样延迟
        Quantity('PointNumber', value=1000),  # ADC门宽
        Quantity('Freqlist', value=[]),  # 通道解调频率

        Quantity('Reset', value=0),  # 系统复位
        Quantity('MixMode', value=1),  # DAC 奈奎斯特区
        Quantity('RefClock', value=1),  # 系统参考时钟选择
    ]

    def __init__(self, addr: str = '', timeout: float = 3.0, **kw):
        super(Driver, self).__init__(addr, timeout, **kw)

    def open(self, **kw):
        """
        输入IP打开设备，配置默认超时时间为5秒
        打开设备时配置RFSoC采样时钟，采样时钟以参数定义
        """
        super(Driver, self).open(**kw)

    def close(self, **kw):
        """
        关闭设备
        """
        super(Driver, self).close(**kw)

    def write(self, name: str, value, **kw):
        channel = kw.get('channel', 1)
        return self.set(name, value, channel)

    def read(self, name: str, **kw):
        channel = kw.get('channel', 1)
        return self.get(name, channel)


if __name__ == '__main__':
    # 导入一个生成随机数字信号的函数
    from rfskit.example_codes.random_digital_signal import random_gen

    driver = Driver('127.0.0.1', 3)

    for i in range(8):
        driver.set('Waveform', random_gen(40, '16', 40), channel=i)
        driver.set('Amplitude', 3, channel=i)
        driver.set('Offset', 3, channel=i)

    driver.set('Output', True)
