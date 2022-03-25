from NS_MCI.tools.data_packing import Packing
import numpy as np


if __name__ == '__main__':
    packing = Packing()
    packing.channel_num = 8
    for i, chnl in enumerate(packing.channels):
        chnl.chnl_id = i

    data = np.array([], dtype='u4')
    for frq in range(2200, 3801, 10):
        signal = np.zeros((8, 32768), dtype='u4')
        for i in range(8):
            signal[i] = packing.signal_generate(frq*1e6, init_phase=i*30, sampling_rate=4e9, parallel_channels=1)
        signal = packing.packing_data(signal)
        data = np.hstack((data, signal))

    with open('a.dat', 'wb') as fp:
        fp.write(data)
