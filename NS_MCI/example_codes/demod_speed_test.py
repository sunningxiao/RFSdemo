# %matplotlib notebook
import numpy as np
import torch
# import matplotlib.pyplot as plt
from waveforms import *
from time import time, sleep


def coff_para(t, freq=200e6, phase=0):
    coeff_list_I = cos(2 * np.pi * freq)(t)
    coeff_list_Q = sin(2 * np.pi * freq)(t)
    return coeff_list_I + 1j * coeff_list_Q


def demodMatrix(y, coff_para):
    return y.dot(coff_para) / y.shape[1]


def demodTensor(y, coff_para):
    return np.einsum('abc,acd->abd', y, coff_para) / y.shape[2]
    # return y.dot(coff_para) / y.shape[2]

def demodTorch(y, coff_para):
    return (torch.bmm(y, coff_para) / y.shape[2]).numpy()
    # return y.dot(coff_para) / y.shape[2]


def test(chnl_num, frq_num, shots):
    sample_rate = 4e9
    width = 4e-6
    # chnl_num = 1
    # frq_num = 1
    # shots = 1

    freqlist = [[4550e6 + j*300e6 for j in range(frq_num)] for i in range(chnl_num)]
    cofflist = {i:[] for i in range(chnl_num)}

    wav_readout = [zero() for i in range(chnl_num)]
    for i in range(chnl_num):
        for j in range(len(freqlist[i])):
            wav_readout[i] = wav_readout[i] + cos(2*np.pi*freqlist[i][j])*(square(width) >> width/2)
            # wav_readout[i] = wav_readout[i] + (square(width) >> width/2+1e-6)
        wav_readout[i] = wav_readout[i]/frq_num
        wav_readout[i].start = 0
        wav_readout[i].stop = width
        wav_readout[i] = (2**15-1)*wav_readout[i].sample(sample_rate).reshape((1, round(width*sample_rate)))
        wav_readout[i] = np.vstack([wav_readout[i] for _ in range(shots)])
    wav_readout = torch.tensor(np.array(wav_readout, dtype='int16'), dtype=torch.int16).to(torch.complex64)

    tm = np.linspace(0, width, round(width*sample_rate))
    for chnl in range(chnl_num):
        _freqlist = freqlist[chnl]
        cofflist[chnl] = np.empty((len(_freqlist), round(width*sample_rate))).astype(complex)
        for i in range(len(_freqlist)):
            cofflist[chnl][i] = coff_para(tm, _freqlist[i], 0)
        cofflist[chnl] = cofflist[chnl].T
    cofflist = torch.tensor([i for i in cofflist.values()], dtype=torch.complex64)

    st = time()
    for i in range(10):
        _ = demodTorch(wav_readout, cofflist)
    print(f'{chnl_num}通道, {frq_num}频点, {shots}shots, 硬解耗时: {(time()-st)/10}')


if __name__ == '__main__':
    for chnl in [1, 8]:
        for frq in [1, 6, 12]:
            for shots in [1, 512, 1024]:
                # print(chnl, frq, shots)
                test(chnl, frq, shots)
    # test(1, 1, 1)
