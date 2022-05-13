import numpy as np
import quantum_driver



dtrace = np.empty(shape=[0 ,ADPointNumber])
dIQ = np.empty(shape = [0 ,cntfreq, shots], dtype= complex)
time_start = time()
for i in range(chnls):
    driver.set('Waveform', wav_readout[i](DAtmspace), i+ 1)
    driver.set('FrequencyList', freqlist[i], i + 1)

driver.set('StartCapture')  # 启动指令
driver.set('GenerateTrig', period)

for i in range(chnls):
    dIQ = np.append(dIQ, [np.swapaxes(driver.get('IQ', channel=(i + 1)), 0, 1)], axis=0)
print(f'单次配置及硬解耗时：{time() - time_start}')

for i in range(chnls):
    dtrace = np.append(dtrace, [np.mean(driver.get('TraceIQ', channel=(i + 1)), axis=0)], axis=0)


