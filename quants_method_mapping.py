"""
各参数对应的 设置/获取 方法映射
"""
from functools import wraps


device_chnl_num = 8


def config_multi_chnl(chnl_num=8):
    """
    多通道同时配置

    :param chnl_num:
    :return:
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if args[1] == chnl_num:
                _args = list(args)
                for i in range(chnl_num):
                    _args[1] = i
                    func(*_args, **kwargs)
            else:
                func(*args, **kwargs)

        return wrapper

    return decorator


def common_set(self, value, channel, param_fmt, cmd, execute):
    """
    通用配置函数

    :param self:
    :param value:
    :param channel:
    :param param_fmt:
    :param cmd:
    :param execute:
    :return:
    """
    self.rfs_kit.set_param_value(param_fmt(channel), value)
    if execute:
        self.rfs_kit.execute_command(cmd)


def common_get(self, value, channel, param_fmt, cmd, execute):
    """
    通用取值函数

    :param self:
    :param value:
    :param channel:
    :param param_fmt:
    :param cmd:
    :param execute:
    :return:
    """
    return self.rfs_kit.get_param_value(param_fmt(channel))


def generate_trig_set(self, value, channel, param_fmt, cmd, execute):
    #
    self.rfs_kit.set_param_value('基准PRF周期', value)
    self.rfs_kit.set_param_value('基准PRF数量', self.qubit_solver.shots)
    if execute:
        self.rfs_kit.execute_command(cmd)


mapping = {
    # 驱动层名称: (配置函数，获取函数，param_format, cmd_name)
    'MixMode': (lambda: None, lambda: None, ''),
    'RefClock': (lambda: None, lambda: None, ''),
    'ADrate': (lambda: None, lambda: None, ''),
    'DArate': (lambda: None, lambda: None, ''),
    'Shot': (lambda: None, lambda: None, ''),
    'PointNumber': (lambda: None, lambda: None, ''),
    'TriggerDelay': (config_multi_chnl(device_chnl_num)(common_set), common_get, 'ADC{}延迟'.format, 'ADC配置'),
    'FrequencyList': (lambda: None, lambda: None, ''),
    'StartCapture': (lambda: None, lambda: None, ''),
    'TraceIQ': (lambda: None, lambda: None, ''),
    'IQ': (lambda: None, lambda: None, ''),
    'Waveform': (lambda: None, lambda: None, ''),
    'GenWave': (lambda: None, lambda: None, ''),
    'GenWaveIQ': (lambda: None, lambda: None, ''),
    'Delay': (lambda: None, lambda: None, ''),
    'Output': (lambda: None, lambda: None, ''),
    'GenerateTrig': (generate_trig_set, lambda: None, ''.format, '内部PRF产生'),
}
