"""
生成随机数字信号
"""

import numpy as np


bit_width_dict = {
    '16': np.uint16,
    '8': np.uint8,
    '32': np.uint32
}


def random_gen(size, bit_width, repeat, amplitude=1):
    """
    生成随机数字信号

    :param size: 波形数量
    :param bit_width: 采样点位宽
    :param repeat: 单波形点数
    :param amplitude: 信号幅值
    :return:
    """
    signal = np.random.randint(2, size=size, dtype=bit_width_dict[bit_width])
    signal = signal.repeat(repeat)
    signal = amplitude * signal
    signal.dtype = bit_width_dict[bit_width]
    return signal


if __name__ == '__main__':
    _size = int(input('请输入波形数量: '))
    _repeat = int(input('请输入单波形点数: '))
    width = input('请输入采样点位宽(8/16/32)(默认16): ')
    amp = input('请输入信号幅值(默认1): ')

    width = width if width != '' else '16'
    amp = int(amp) if amp != '' else 1

    data = random_gen(_size, width, _repeat, amp)

    with open(f'signal_{_size}_{_repeat}_{width}_{amp}.dat', 'wb') as fp:
        fp.write(data)
