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
    u4_data: "np.ndarray" = np.fromfile(file_name, dtype='>u4')
    res = np.zeros_like(data)[:f_size//2]
    print(res.shape)

    t_head = head_length//2
    for i in range(f_size//(pack_length*chnl_num)):
        p = i*(pack_length*chnl_num)//2
        # slice_head = slice(p//2, p//2+t_head//2)
        slice_head00 = slice(p//2, p//2+6//2)
        # slice_head_ = slice(p, p + t_head)
        slice_head00_ = slice(p, p + 6)
        slice_head01_ = slice(p + 6, p+t_head)
        data_head = u4_data[slice_head00]
        data_head[0] = int('0x18EFDC01', 16)
        data_head[1], data_head[2] = data_head[2], data_head[1]
        res[slice_head00_] = np.frombuffer(data_head.byteswap(), dtype='>u2')
        res[slice_head01_] = data[slice_head01_]

        if chnl_num >= 2:
            slice_head10 = slice(p//2+t_head//2, p//2+(t_head//2)+6//2)
            slice_head10_ = slice(p+t_head, p+t_head+6)
            slice_head11_ = slice(p+t_head+6, p+t_head*2)
            data_head = u4_data[slice_head10]
            data_head[0] = int('0x18EFDC01', 16)
            data_head[1], data_head[2] = data_head[2], data_head[1]
            res[slice_head10_] = np.frombuffer(data_head.byteswap(), dtype='>u2')
            res[slice_head11_] = data[slice_head11_]

        if chnl_num >= 3:
            slice_head20 = slice(p//2+(t_head//2)*2, p//2+(t_head//2)*2+6//2)
            slice_head20_ = slice(p+t_head*2, p+t_head*2+6)
            slice_head21_ = slice(p+t_head*2+6, p+t_head*3)
            data_head = u4_data[slice_head20]
            data_head[0] = int('0x18EFDC01', 16)
            data_head[1], data_head[2] = data_head[2], data_head[1]
            res[slice_head20_] = np.frombuffer(data_head.byteswap(), dtype='>u2')
            res[slice_head21_] = data[slice_head21_]

        if chnl_num >= 4:
            slice_head30 = slice(p//2+(t_head//2)*3, p//2+(t_head//2)*3+6//2)
            slice_head30_ = slice(p+t_head*3, p+t_head*3+6)
            slice_head31_ = slice(p+t_head*3+6, p+t_head*4)
            data_head = u4_data[slice_head30]
            data_head[0] = int('0x18EFDC01', 16)
            data_head[1], data_head[2] = data_head[2], data_head[1]
            res[slice_head30_] = np.frombuffer(data_head.byteswap(), dtype='>u2')
            res[slice_head31_] = data[slice_head31_]

        slice_data = slice(p+t_head*chnl_num, p+(pack_length*chnl_num)//2)
        data_wave: "np.ndarray" = data[slice_data]
        res[slice_data] = data_wave.byteswap() if switch else data_wave

    with open(os.path.split(file_name)[-1], 'wb') as fp:
        fp.write(res)
