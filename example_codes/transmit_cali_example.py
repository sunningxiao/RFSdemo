from ui.附加功能.utils import Custom
from tools.data_unpacking import UnPackage

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def fmt_csv(data: np.ndarray, fmt_str='chnl_{}'.format):
    _data = pd.DataFrame(data)
    _data.columns = ['f/MHz'] + [fmt_str(i) for i in range(data.shape[1]-1)]
    return _data


if __name__ == '__main__':
    start = int(input('起始频率MHz\n>>>'))
    stop = int(input('终止频率MHz\n>>>'))
    step = int(input('步进MHz\n>>>'))
    bw = int(input('带宽MHz\n>>>'))
    if bw != 0:
        tw = int(input('脉宽ns\n>>>'))
    else:
        tw = 0
    data = []
    filename = input('文件名(直接回车停止输入)\n>>>')
    while filename != '':
        fp = open(filename, 'rb')
        data.append(fp)
        filename = input('文件名(直接回车停止输入)\n>>>')

    cali_chnl = int(input('采集通道号\n>>>'))

    chnl_num = len(data)
    # data = np.array(data, dtype='u4')
    frq_num = (stop-start)//step+1
    _data = UnPackage.channel_data_filter(data, list(range(frq_num)), list(range(8)))

    for file in data:
        file.close()

    amp = np.zeros([chnl_num, frq_num], dtype=np.float64)
    phase = np.zeros([chnl_num, frq_num], dtype=np.float64)
    delay = np.zeros([chnl_num, frq_num], dtype=np.float64)
    real_amp = np.zeros([chnl_num, frq_num], dtype=np.float64)
    real_phase = np.zeros([chnl_num, frq_num], dtype=np.float64)
    for index, frq in enumerate(range(start, stop+1, step)):
        cali_data = np.array([_data[data[chnl]][index][cali_chnl] for chnl in range(chnl_num)])
        if bw != 0:
            result = Custom.get_chirp_coherence(cali_data, {'fs': 4e9, 'fc': frq*1e6, 'Bw': bw*1e6, 'Tp': tw*1e-9})
            print(frq, result)
            delay[:, index] = result
        else:
            result = Custom.get_coherence(cali_data, {'fs': 4e9, 'fc': frq*1e6})
            amp[:, index] = result[:, 0]
            phase[:, index] = result[:, 1]
            delay[:, index] = result[:, 2]
            real_amp[:, index] = result[:, 3]
            real_phase[:, index] = result[:, 4]

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
    fmt_csv(np.vstack([list(range(start, stop+1, step)), amp]).T, 'chnl_{}/dB'.format).to_csv('amplitude.csv', index=False)
    fmt_csv(np.vstack([list(range(start, stop+1, step)), phase]).T).to_csv('phase.csv', index=False)
    fmt_csv(np.vstack([list(range(start, stop+1, step)), delay]).T, 'chnl_{}/ps'.format).to_csv('delay.csv', index=False)
    fmt_csv(np.vstack([list(range(start, stop+1, step)), real_amp]).T, 'chnl_{}/dBm'.format).to_csv('real_amplitude.csv', index=False)
    fmt_csv(np.vstack([list(range(start, stop+1, step)), real_phase]).T).to_csv('real_phase.csv', index=False)
    # np.savetxt('Amplitude.csv', amp.T, delimiter=',', fmt='%.18f')
    # np.savetxt('phase.csv', phase.T, delimiter=',', fmt='%.18f')
    # np.savetxt('delay.csv', delay.T, delimiter=',', fmt='%.18f')
