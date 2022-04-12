from numba import cuda
import numpy as np
from waveforms import cos, sin, gaussian
import math
from time import time


def coff_para(t, freq=200e6, phase=0):
    coeff_list_I = cos(2 * np.pi * freq)(t)
    coeff_list_Q = sin(2 * np.pi * freq)(t)
    return coeff_list_I + 1j * coeff_list_Q


def demodCPU(y, coff_para=np.asarray([])):
    return y.dot(coff_para.T) / len(y)


class SolveQubit:
    def __init__(self, ADrate=4e9, DArate=6e9, chnl=8, shots=1000, pointnum=16e3):
        self.freqlist = {i: [] for i in range(chnl)}
        self.phaselist = {i: [] for i in range(chnl)}
        self.cofflist = {i: [] for i in range(chnl)}
        self.ADrate = ADrate
        self.DArate = DArate
        self.pointnum = pointnum
        self.dac_points = {i: 179 for i in range(chnl)}
        self.shots = shots

    def setshots(self, shots):
        self.shots = shots

    def setpointnum(self, pointnum):
        self.pointnum = pointnum

    def setfreqlist(self, freqlist, chnl):
        if not isinstance(freqlist, list):
            print('输入非频率列表，请检查格式')
            return
        start = time()
        self.tm = np.linspace(0, (self.pointnum - 1) / self.ADrate, int((self.pointnum + 63) // 64 * 64))
        self.cofflist[chnl] = np.empty((len(freqlist), int((self.pointnum + 63) // 64 * 64))).astype(complex)
        self.freqlist[chnl] = freqlist
        for i in range(len(freqlist)):
            phase = self.phaselist[i] if len(self.phaselist) == len(freqlist) else 0
            self.cofflist[chnl][i] = coff_para(self.tm, freqlist[i], phase)
        print("generate freq list " + str(time() - start))

    def setphaselist(self, phaselist, chnl):
        if not isinstance(phaselist, list):
            print('输入非频率列表，请检查格式')
            return
        start = time()
        self.tm = np.linspace(0, (self.pointnum - 1) / self.ADrate, int((self.pointnum + 63) // 64 * 64))
        self.cofflist[chnl] = np.empty((len(phaselist), int((self.pointnum + 63) // 64 * 64))).astype(complex)
        self.phaselist[chnl] = phaselist
        for i in range(len(phaselist)):
            freq = self.freqlist[i] if len(self.freqlist) == len(phaselist) else 0
            self.cofflist[chnl][i] = coff_para(self.tm, freq, phaselist[i])
        print("generate freq list " + str(time() - start))

    def calculateCPU(self, data, chnl, no_complex=False):
        # print(f'进入{data}')
        result = np.empty((len(data), len(self.freqlist[chnl]))).astype(complex)
        # print(f'第一步{result}')
        start = time()
        for i in range(len(data)):
            for j in range(len(self.freqlist[chnl])):
                # print(f'第二步{result}')
                result[i][j] = demodCPU(data[i], self.cofflist[chnl][j])
        print("Calculate by CPU " + str(time() - start))
        if no_complex:
            # print(f'第三步{result}')
            result = np.array([np.real(result), np.imag(result)])
        return result

    def calculate_matrix(self, data, chnl, no_complex=False):
        start = time()
        try:
            result = demodCPU(data, self.cofflist[chnl])
        except AttributeError as e:
            result = np.array([], dtype=np.complex)
        print("Calculate by CPU " + str(time() - start))
        if no_complex:
            # print(f'第三步{result}')
            result = np.array([np.real(result), np.imag(result)])
        return result
