"""
文件读取测试测试

"""

import time
import os


if __name__ == '__main__':
    file_path = input('请输入文件路径: ')
    speed = input('请输入目标读取速率(MB/s)')
    block_size = 4*1024**2
    sleep_time = block_size/(float(speed)*1024**2)

    while not os.path.exists(file_path):
        file_path = input('请重新输入文件路径: ')

    try:
        while True:
            fp = open(file_path, 'rb')
            data = fp.read(block_size)
            times = 0
            start_time = time.time()
            while len(data) == block_size:
                times += 1
                if times % 50 == 0:
                    _speed = block_size*times/1024**2/(time.time()-start_time)
                    print(f'读取速度: {_speed}MB/s')
                    start_time = time.time()
                    times = 0
                data = fp.read(block_size)
                time.sleep(sleep_time)
            fp.close()
            _speed = (block_size * times+len(data)) / 1024 ** 2 / (time.time() - start_time)
            print(f'读取速度: {_speed}MB/s')
            start_time = time.time()
    except KeyboardInterrupt as e:
        print('程序退出')
