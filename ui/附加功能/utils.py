"""
%正弦幅相一致性指标分析函数
%
%by chen lu
%2021.12.1
"""
import numpy as np
from scipy.fftpack import fft, ifft
import matplotlib.pyplot as plt


class Custom:
    """
        base
    """

    @classmethod
    def get_coherence(cls, sig, para) -> np.ndarray:
        """
        处理正弦信号，获取幅相一致性指标并生成校正因子
        输入：
        信号sig为按行排布的二维数组
        para为字典，存储信号参数，字典中必须有：fs,fc
        para = {
            'fs': 4e9,                      # 采样率
            'fc': 1950e6,                   # 信号频率
            'RefChannel': 0,                # 参考通道,默认为通道0
            'GenCaliFactorEn': 1,           # 生成校正因子使能，默认不使能
        }
        输出：uniform，一致性指标，3列数组，分别为幅度一致性/dB、相位一致性/°和延迟一致性/ps

        """
        nc = sig.shape[0]           # 获取信号通道数
        nr = sig.shape[1]

        # 正弦信号整周期截取
        fs = para['fs']
        fc_orig = para['fc']
        fc = cls.if_sample_freq(fc_orig, fs)
        n_min = cls.non_leakage_min_number(abs(fc), fs)
        if n_min:
            if n_min <= nr:
                nr = int(nr - nr % n_min)    # 当可以整周期截断防止频谱泄露时取最大的Nr值
                sig = sig[:, :nr]       # 整周期截取
        spec = fft(sig, nr)     # 做FFT
        n_spec = int(nr / 2)
        if fc < 0:
            amp = abs(spec[:, -n_spec:])     # 找负频谱
        else:
            amp = abs(spec[:, :n_spec])      # 找正频谱
        max_index = np.argmax(amp) % n_spec
        if max_index == 0:
            amp_expect_zero = np.vstack((np.empty((nc, 10)), amp[:, -n_spec+10:]))      # 去除零频附近10个点
            max_index = np.argmax(amp_expect_zero) % n_spec
        if fc < 0:
            max_index = max_index + n_spec
            if (nr % 2) == 1:
                max_index = max_index+1
        peak_amp = cls.mag2db(spec[:, max_index])           # 各通道提取同一频率处的值
        peak_phase = np.angle(spec[:, max_index])
        f = cls.freq(fs, nr)
        fmax = f[max_index]
        if para.get('RefChannel'):
            ref_channel = para['RefChannel']
        else:
            ref_channel = 0          # 默认不生成校正因子

        peak_amp_uniform = peak_amp-peak_amp[ref_channel]                               # 幅度一致性，以参考通道作为基准
        peak_phase_uniform = peak_phase-peak_phase[ref_channel]
        peak_phase_uniform = np.angle(np.exp(1j * peak_phase_uniform))
        delay_uniform = -peak_phase_uniform / (2 * np.pi * fc_orig / 1e12)               # 延迟需要用原始频率计算,单位ps
        peak_phase_uniform = np.degrees(peak_phase_uniform)                             # 用角度表示相位一致性
        uniform = np.vstack((peak_amp_uniform, peak_phase_uniform, delay_uniform)).T      # 一致性指标

        # 生成校正因子
        if para.get('GenCaliFactorEn'):
            gen_cali_factor_en = para['GenCaliFactorEn']
        else:
            gen_cali_factor_en = 0          # 默认不生成校正因子
        if gen_cali_factor_en:
            peak_amp_uniform = peak_amp_uniform-max(peak_amp_uniform)
            cali_factor = 10**(peak_amp_uniform/20)*np.exp(1j*peak_phase_uniform/180*np.pi)      # 各通道福相因子
            cali_factor = 1/cali_factor
            cali_factor_uint, cali_factor = cls.float_complex_2qi(cali_factor)
            cali_factor_hex = [0] * nc
            for i in range(nc):
                cali_factor_hex[i] = hex(int(cali_factor_uint[i]))          # 16进制校正因子
        return uniform

    @classmethod
    def get_chirp_coherence(cls, chirp, para):
        """
        处理正弦信号，获取延迟一致性
        输入：
        信号chirp为按行排布的二维数组
        para为字典，存储信号参数，字典中必须有：fs,fc
        para = {
            'fs': 4e9,                      # 采样率/Hz
            'fc': 0,                        # 信号中心频率/Hz
            'Bw': 1.8e9                     # 带宽/Hz
            'Tp':10e-6                      # 脉宽/s
            'RefChannel': 0,                # 参考通道,默认为通道0
            'InterpNum': 1,                 # FFT插值倍数，默认为100
        }
        输出：uniform：延迟一致性/ns
        """
        fs = para['fs']
        fc = para['fc']
        bw = para['Bw']
        tp = para['Tp']
        nc = chirp.shape[0]
        nr = chirp.shape[1]
        # window_en = bool(para['WindowEn'])

        kr = bw / tp
        # 生成mf因子并进行匹配滤波
        t_mf = np.arange(int(fs * tp)) / fs
        mf = np.exp(1j * np.pi * kr * (t_mf - tp / 2) ** 2 + 1j * 2 * np.pi * fc * t_mf)
        mf = np.conjugate(fft(mf, nr))  # 原信号频谱取共轭是mf因子
        spec = fft(chirp, nr)
        chirp = mf * spec  # 匹配滤波
        # 窗函数
        # if window_en:
        #     n_bw = round(bw / fs * nr)          # 根据频谱计算窗的长度
        #     window_type = para['WindowType']    # 加窗的类型，如果不是hamming且加窗使能，那么默认加kaiser窗
        #     if window_type == 'hamming':
        #         window = windows.hamming(n_bw)
        #     else:
        #         window = windows.kaiser(n_bw, 2.5)
        #     window = np.concatenate((np.zeros(int((nr - n_bw) / 2)), window, np.zeros(int((nr - n_bw) / 2))), axis=0)
        #     chirp = chirp * ifftshift(window)   # 加窗
        chirp = ifft(chirp, nr)  # 转成时域信号

        # 插值
        if para.get('InterpNum'):
            m = int(para['InterpNum'])  # 获取插值倍数
        else:
            m = 100  # 默认fft插值100点
        sig = cls.interpft(chirp, nr * m)  # 进行m倍fft插值
        fs = fs * m  # 插值信号后的采样率
        # print('时间精度：%fps' % (1 / fs * 1e12))
        nr = sig.shape[1]  # 插值后信号的点数
        t = np.arange(nr) / fs
        sig_db = cls.mag2db(abs(sig))
        sig_db = sig_db - sig_db.max()  # 脉压结果(统一归一化）
        # 统计延时
        max_index = sig_db.argmax(axis=1)  # 找出sig_db每行最大值的位置
        delay = t[max_index]
        delay = delay * 1e9  # 原始延迟/ns
        if para.get('RefChannel'):
            ref_channel = para['RefChannel']
        else:
            ref_channel = 0  # 默认参考通道为0
        uniform = delay - delay[ref_channel]
        return uniform

    @classmethod
    def float_complex_2qi(cls, complex_data, n_bit=16):
        """ 对浮点复数进行定点处理，并转换为QI形式"""
        max_value = max(abs(complex_data))
        complex_data = complex_data / max_value
        complex_data = np.around(complex_data * (2 ** (n_bit - 1) - 1))  # 量化
        data_real = np.real(complex_data)
        data_imag = np.imag(complex_data)
        data_real = data_real + (data_real < 0) * 2 ** n_bit  # 补码对应的无符号数
        data_imag = data_imag + (data_imag < 0) * 2 ** n_bit
        data_qi = data_imag * (2 ** n_bit) + data_real  # 虚部在高位
        return data_qi, complex_data

    @classmethod
    def float_complex_2QI(cls, fc_orig, fs):
        """ 计算中频采样频率"""
        fc = fc_orig
        if fc_orig > fs / 2:
            fc = fc_orig % fs
            if fc > fs / 2:
                fc = fc - fs
        return fc

    @classmethod
    def non_leakage_min_number(cls, fc, fs):
        """ 计算没有频谱泄漏的最小点数"""
        n_min = []
        for k in range(10000):
            if fs / fc * (k + 1) == int(fs / fc * (k + 1)):
                n_min = fs / fc * (k + 1)  # 保证没有泄露的最小采样点数
                break
        return n_min

    @classmethod
    def if_sample_freq(cls, fc_orig, fs):
        fc = fc_orig
        if fc_orig > fs / 2:
            fc = fc_orig % fs
            if fc > fs / 2:
                fc = fc - fs
        return fc

    @classmethod
    def freq(cls, fs, n):
        """ 模拟频率轴构造,该频率轴与做完fft的信号对应,第一点为零频"""
        f = np.arange(n)
        f = f / n * fs
        mod = n % 2
        if mod == 0:
            n = int(n / 2)
            f[-n:] = f[-n:] - fs
        else:
            n = int(-(n + 1) / 2)
            f[-n] = f[-n] - fs
        return f

    @classmethod
    def interpft(cls, x, ny):
        """对按行排列的数组进行FFT插值  x: 原始信号 ny: 插值后的点数"""
        na = x.shape[0]
        nr = x.shape[1]
        a = fft(x, nr)
        nyqst = int(np.ceil((nr + 1) / 2))
        b = np.hstack((a[:, 0:nyqst], np.zeros((na, ny - nr)), a[:, nyqst:nr]))
        b[:, nyqst - 1] = b[:, nyqst - 1] / 2
        b[:, nyqst + ny - nr - 1] = b[:, nyqst - 1]
        y = ifft(b, ny)
        y = y * ny / nr
        return y

    @classmethod
    def mag2db(cls, y):
        """同matlab的mag2db，为防止输入非正数调用失败，负数取模，0取0.000001,即-120dB"""
        y = abs(y)
        y[y == 0] = 0.000001
        ydb = 20 * np.log10(y)
        return ydb
