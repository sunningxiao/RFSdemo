import os

with open(r'\\192.168.1.185\share\存储阵列\57_记录仪测试_21-11-19_10-18-03\数据通道_0.data', 'rb') as fp:
    size = os.path.getsize(r'\\192.168.1.185\share\存储阵列\57_记录仪测试_21-11-19_10-18-03\数据通道_0.data')
    print(f'getsize换算包数：{size/1050624}')
    fp.seek(size-1050624)
    data = fp.read()
    length = len(data)
    print(f'读取数据长度{length}')
