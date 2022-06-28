import numpy as np


if __name__ == '__main__':
    file_name = input('请输入文件名\n')
    with open(file_name, 'rb') as fp:
        data = fp.read()
        data = np.frombuffer(data, dtype='u4')

    data: np.ndarray
    _data = np.zeros(data.shape, dtype='u4')
    _data[0::4] = data[2::4]
    _data[1::4] = data[3::4]
    _data[2::4] = data[0::4]
    _data[3::4] = data[1::4]

    with open('trans_'+file_name, 'wb') as fp:
        fp.write(_data)
