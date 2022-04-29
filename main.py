from waveforms import Waveform
import numpy as np


class TestWaveform(Waveform):
    def __call__(self, x, frag=False, out=None):
        range_list = np.searchsorted(x, self.bounds)
        return range_list
