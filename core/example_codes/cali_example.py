import os
import time
from ui.附加功能.utils import Custom
from core.tools.data_unpacking import UnPackage

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def fmt_csv(data: np.ndarray, fmt_str='chnl_{}'.format):
    _data = pd.DataFrame(data)
    _data.columns = ['f/Hz'] + [fmt_str(i) for i in range(data.shape[1]-1)]
    if data.dtype == np.complex_:
        for title in _data.columns:
            if title == 'f/Hz':
                _data[title] = _data[title].apply(abs).apply(int)
            else:
                _data[title] = _data[title].apply(str).str.replace(r'\(|\)', '', regex=True)
    return _data


if __name__ == '__main__':
    task_id = input('请输入任务号（默认为0）\n>>>')
    task_id = int(task_id) if task_id else 0
    start = int(input('起始频率MHz\n>>>'))
    stop = int(input('终止频率MHz\n>>>'))
    step = int(input('步进MHz\n>>>'))
    bw = int(input('带宽MHz\n>>>'))
    if bw != 0:
        tw = float(input('脉宽ns\n>>>'))
    else:
        tw = 0
    filename = input('文件名\n>>>')
    with open(filename, 'rb') as fp:
        data: np.ndarray = np.frombuffer(fp.read(), dtype='u4')

    frq_num = (stop-start)//step+1
    _data = UnPackage.channel_data_filter(data, list(range(frq_num)), list(range(8)))

    assert _data, '解包失败'
    chnl_num = len(_data[0][0])

    # amp = np.zeros([chnl_num, frq_num], dtype=np.float64)
    # phase = np.zeros([chnl_num, frq_num], dtype=np.float64)
    # delay = np.zeros([chnl_num, frq_num], dtype=np.float64)
    # real_amp = np.zeros([chnl_num, frq_num], dtype=np.float64)
    # real_phase = np.zeros([chnl_num, frq_num], dtype=np.float64)
    res = {}
    for index, frq in enumerate(range(start, stop+1, step)):
        cali_data = _data[0][index]
        cali_data = np.array([cali_data[i] for i in range(8)])
        if bw != 0:
            result = Custom.get_chirp_coherence(cali_data, {'fs': 4e9, 'fc': frq*1e6, 'Bw': bw*1e6, 'Tp': tw*1e-9})
            print(frq, result)
            for name, value in result.items():
                if name not in res:
                    res[name] = np.zeros([chnl_num, frq_num], dtype=np.float64)
                res[name][:, index] = value
        else:
            result = Custom.get_coherence(cali_data, {'fs': 4e9, 'fc': frq*1e6, 'GenCaliFactorEn': 1})
            for name, value in result.items():
                if name not in res:
                    dtype = value.dtype
                    res[name] = np.zeros([chnl_num, frq_num], dtype=dtype)
                res[name][:, index] = value
            # amp[:, index] = result[:, 0]
            # phase[:, index] = result[:, 1]
            # delay[:, index] = result[:, 2]
            # real_amp[:, index] = result[:, 3]
            # real_phase[:, index] = result[:, 4]
    if not os.path.exists(f'./{task_id}'):
        os.mkdir(f'{task_id}')
    time_str = time.strftime('%Y-%M-%d_%H-%M-%S')
    for name, value in res.items():
        fmt_csv(np.vstack([list(np.arange(start, stop + 1, step)*1e6), value]).T).to_csv(f'./{task_id}/{task_id}_{name}_{time_str}.csv',
                                                                                 index=False)

    plt.title('Amplitude/dB')
    lines = plt.plot(res['peak_amp_uniform'].T)
    plt.legend(handles=lines, labels=list(range(8)))
    plt.show()
    plt.title('phase/°')
    lines = plt.plot(res['peak_phase_uniform'].T)
    plt.legend(handles=lines, labels=list(range(8)))
    plt.show()
    plt.title('delay/ps')
    lines = plt.plot(res['delay_uniform'].T)
    plt.legend(handles=lines, labels=list(range(8)))
    plt.show()

    # fmt_csv(np.vstack([list(range(start, stop+1, step)), amp]).T, 'chnl_{}/dB'.format).to_csv('amplitude.csv', index=False)
    # fmt_csv(np.vstack([list(range(start, stop+1, step)), phase]).T).to_csv('phase.csv', index=False)
    # fmt_csv(np.vstack([list(range(start, stop+1, step)), delay]).T, 'chnl_{}/ps'.format).to_csv('delay.csv', index=False)
    # fmt_csv(np.vstack([list(range(start, stop+1, step)), real_amp]).T, 'chnl_{}/dBm'.format).to_csv('real_amplitude.csv', index=False)
    # fmt_csv(np.vstack([list(range(start, stop+1, step)), real_phase]).T).to_csv('real_phase.csv', index=False)
    # np.savetxt('Amplitude.csv', amp.T, delimiter=',', fmt='%.18f')
    # np.savetxt('phase.csv', phase.T, delimiter=',', fmt='%.18f')
    # np.savetxt('delay.csv', delay.T, delimiter=',', fmt='%.18f')
