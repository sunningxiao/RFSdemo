# import numpy as np
# import matplotlib.pyplot as plt
from gen_waveform import gen_wave
import numpy as np
from waveforms import *
from time import time, sleep
import threading

sample_rate = 6e9
width = 30e-9
width_all = 100e-6
frq = 4200e6
chnl_num = 24

line = np.arange(0, width_all, 1/sample_rate)

# %%
wave_lo = cos(2 * pi * frq)

wave_30 = [(square(width) >> (width / 2)) * wave_lo for i in range(chnl_num)]
for wave in wave_30:
    wave.start = 0
    wave.stop = width

wave_100 = [zero() for i in range(chnl_num)]
for index, wave in enumerate(wave_100):
    for i in range(int(300)):
        wave += (square(width) >> (width * 2 * i + width / 2)) * wave_lo
    wave.start = 0
    wave.stop = width_all
    wave_100[index] = wave


st = time()
for i in range(1):
    for wave in wave_30:
        gen_wave(wave, line)
print(f'{chnl_num}通道, 简单波形cy生成耗时: {(time() - st) / 1}')

st = time()
for i in range(1):
    for wave in wave_30:
        wave(line)
print(f'{chnl_num}通道, 简单波形生成耗时: {(time() - st) / 1}')


st = time()
for i in range(1):
    for wave in wave_100:
        gen_wave(wave, line)

print(f'{chnl_num}通道, 复杂波形cython生成耗时: {(time() - st) / 1}')


st = time()
for i in range(1):
    for wave in wave_100:
        wave(line)
print(f'{chnl_num}通道, 复杂波形生成耗时: {(time() - st) / 1}')