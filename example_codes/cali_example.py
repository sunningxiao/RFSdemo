from ui.附加功能.utils import Custom
from tools.data_unpacking import UnPackage

import numpy as np
import matplotlib.pyplot as plt


if __name__ == '__main__':
    start = int(input('起始频率MHz\n>>>'))
    stop = int(input('终止频率MHz\n>>>'))
    step = int(input('步进MHz\n>>>'))
    bw = int(input('带宽MHz\n>>>'))
    if bw != 0:
        tw = int(input('脉宽ns\n>>>'))
    else:
        tw = 0
    filename = input('文件名\n>>>')
    with open(filename, 'rb') as fp:
        data: np.ndarray = np.frombuffer(fp.read(), dtype='u4')

    frq_num = (stop-start)//step+1
    _data = UnPackage.channel_data_filter(data, list(range(frq_num)), list(range(8)))

    amp = np.zeros([8, frq_num], dtype=np.float64)
    phase = np.zeros([8, frq_num], dtype=np.float64)
    delay = np.zeros([8, frq_num], dtype=np.float64)
    for index, frq in enumerate(range(start, stop+1, step)):
        cali_data = _data[0][index]
        cali_data = np.array([cali_data[i] for i in range(8)])
        if bw != 0:
            result = Custom.get_chirp_coherence(cali_data, {'fs': 4e9, 'fc': frq*1e6, 'Bw': bw*1e6, 'Tp': tw*1e-9})
            print(frq, result)
            delay[:, index] = result
        else:
            result = Custom.get_coherence(cali_data, {'fs': 4e9, 'fc': frq*1e6})
            amp[:, index] = result[:, 0]
            phase[:, index] = result[:, 1]
            delay[:, index] = result[:, 2]

    plt.title('Amplitude/dB')
    lines = plt.plot(amp.T)
    plt.legend(handles=lines, labels=list(range(8)))
    plt.show()
    plt.title('phase/°')
    lines = plt.plot(phase.T)
    plt.legend(handles=lines, labels=list(range(8)))
    plt.show()
    plt.title('delay/ps')
    lines = plt.plot(delay.T)
    plt.legend(handles=lines, labels=list(range(8)))
    plt.show()
    np.savetxt('Amplitude.csv', amp, delimiter=',', fmt='%.18f')
    np.savetxt('phase.csv', phase, delimiter=',', fmt='%.18f')
    np.savetxt('delay.csv', delay, delimiter=',', fmt='%.18f')
