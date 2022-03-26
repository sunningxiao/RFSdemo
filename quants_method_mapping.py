"""
各参数对应的 设置/获取 方法映射
"""


def common_set(self, value, channel, param_fmt, cmd, execute):
    self.rfs_kit.set_param_value(param_fmt(channel), value)
    if execute:
        self.rfs_kit.execute_command(cmd)


def common_get(self, value, channel, param_fmt, cmd, execute):
    return self.rfs_kit.get_param_value(param_fmt(channel))


mapping = {
    # 驱动层名称: (配置函数，获取函数，param_format, cmd_name)
    'MixMode': (lambda: None, lambda: None, ''),
    'RefClock': (lambda: None, lambda: None, ''),
    'ADrate': (lambda: None, lambda: None, ''),
    'DArate': (lambda: None, lambda: None, ''),
    'Shot': (lambda: None, lambda: None, ''),
    'PointNumber': (lambda: None, lambda: None, ''),
    'TriggerDelay': (common_set, common_get, 'ADC{}延迟'.format, 'ADC配置'),
    'FrequencyList': (lambda: None, lambda: None, ''),
    'StartCapture': (lambda: None, lambda: None, ''),
    'TraceIQ': (lambda: None, lambda: None, ''),
    'IQ': (lambda: None, lambda: None, ''),
    'Waveform': (lambda: None, lambda: None, ''),
    'Delay': (lambda: None, lambda: None, ''),
    'Output': (lambda: None, lambda: None, ''),
    'GenerateTrig': (lambda: None, lambda: None, ''),
}
