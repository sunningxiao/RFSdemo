import zlib

if __name__ == '__main__':
    read_fp = open(r'F:\数据通道_1.data', 'rb')
    data = read_fp.read()
    read_fp.close()
    fp = open(r'F:\data.data', 'wb')
    c = zlib.compressobj(5)
    length = 1024**2*60
    for i in range(0, len(data), length):
        _data = c.compress(data[i: i+length])
        print(len(_data))
        fp.write(_data)

    fp.close()
