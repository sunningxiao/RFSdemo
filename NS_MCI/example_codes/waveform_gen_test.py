# import numpy as np
# import matplotlib.pyplot as plt
from waveforms import *
from time import time, sleep

sample_rate = 6e9
width = 30e-9
width_all = 100e-6
frq = 4200e6
chnl_num = 24

#%%
wave_lo = cos(2*pi*frq)

wave_30 = [(square(width)>>(width/2))*wave_lo for i in range(chnl_num)]
for wave in wave_30:
    wave.start = 0
    wave.stop = width

wave_100 = [zero() for i in range(chnl_num)]
for index, wave in enumerate(wave_100):
    for i in range(int(300)):
        wave += (square(width)>>(width*2*i+width/2))*wave_lo
    wave.start = 0
    wave.stop = width_all
    wave_100[index] = wave

st = time()
for i in range(100):
    for wave in wave_30:
        wave.sample(sample_rate)
print(f'{chnl_num}通道, 简单波形生成耗时: {(time()-st)/100}')

st = time()
for i in range(10):
    for wave in wave_100:
        wave.sample(sample_rate)
print(f'{chnl_num}通道, 复杂波形生成耗时: {(time()-st)/10}')

