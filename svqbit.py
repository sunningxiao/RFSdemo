from numba import cuda
import numpy as np
from waveforms import cos, sin, gaussian
import math
from time import time


def coff_para(t=[], freq=200e6):
    coeff_list_I = np.array(cos(2 * np.pi * (freq))(t))
    coeff_list_Q = np.array(sin(2 * np.pi * (freq))(t))
    return coeff_list_I + 1j * coeff_list_Q


def demodCPU(y, coff_para=np.asarray([])):
    return y.dot(coff_para.T) / len(y)


class SolveQubit:
    def __init__(self, ADrate=4e9, DArate=6e9, chnl=8, shots=1000, pointnum=16e3):
        self.freqlist = {i: [] for i in range(chnl)}
        self.cofflist = {i: [] for i in range(chnl)}
        self.ADrate = ADrate
        self.DArate = DArate
        self.pointnum = pointnum
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
        self.tm = np.linspace(0, (self.pointnum - 1) / self.ADrate, int(self.pointnum))
        self.cofflist[chnl] = np.empty((len(freqlist), int(self.pointnum))).astype(complex)
        self.freqlist[chnl] = freqlist
        for i in range(len(freqlist)):
            self.cofflist[chnl][i] = coff_para(self.tm, freqlist[i])
        print("generate freq list " + str(time() - start))

    def calculateCPU(self, data, chnl, return_complex):
        result = np.empty((len(data), len(self.freqlist[chnl]))).astype(complex)
        start = time()
        for i in range(self.shots):
            for j in range(len(self.freqlist[chnl])):
                result[i][j] = demodCPU(data[i], self.cofflist[chnl][j])
        print("Calculate by CPU " + str(time() - start))
        if not return_complex:
            result = np.array([np.real(result), np.imag(result)])
        return result