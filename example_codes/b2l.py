import numpy as np
import os


if __name__ == '__main__':
    head_length = int(input(f'请输入包头长度：\n'))
    switch = bool(input(f'是否调整数据(0/1)：\n'))
    file_name = ''
    if not os.path.exists(file_name):
        file_name = input(f'请输入文件路径：\n')

    pack_length = int(input(f'请输入包长(Byte)：\n'))
    chnl_num = int(input(f'请输入通道数：\n'))
    f_size = os.path.getsize(file_name)
    f_size = f_size//pack_length*pack_length
    data: "np.ndarray" = np.fromfile(file_name, dtype='>u2')
    u4_data: "np.ndarray" = np.fromfile(file_name, dtype='>u2')
    res = np.zeros_like(data)[:f_size//2]
    print(res.shape)

    t_head = 6
    for i in range(f_size//pack_length):
        p = i*pack_length//2
        slice_head = slice(p//2, p//2+t_head//2)
        slice_data = slice(p+t_head, p+pack_length//2)

        data_head = u4_data[slice_head]
        data_head[0] = int('0x18EFDC01', 16)
        data_head[1], data_head[2] = data_head[2], data_head[1]
        data_wave: "np.ndarray" = data[slice_data]
        res[slice_head] = np.frombuffer(data_head.byteswap(), dtype='u2')
        res[slice_data] = data_wave.byteswap() if switch else data_wave

    with open(os.path.split(file_name)[-1], 'wb') as fp:
        fp.write(res)
