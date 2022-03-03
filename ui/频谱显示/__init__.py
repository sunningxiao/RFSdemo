import pyqtgraph as pg
import numpy as np
from numpy import fft
from scipy.signal import windows

from PyQt5 import QtCore, QtGui, QtWidgets

from ui.频谱显示 import spectrum_ui


class SpectrumScreen(QtWidgets.QDialog, spectrum_ui.Ui_Dialog):
    def __init__(self, ui_parent):
        super(SpectrumScreen, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('频谱快视')
        self.ui_parent = ui_parent
        self.plot_win = pg.GraphicsLayoutWidget()
        self.wave_show_win.addWidget(self.plot_win)
        self.plots = []
        # 频谱展示
        self.spectrum_plot = self.append_plot('回波频谱(dB)')
        self.channel_plots = [self.spectrum_plot.plot(name=f'chnl{i}') for i in range(8)]

    def append_plot(self, name, axis=None):
        if axis:
            plot = self.plot_win.addPlot(axisItems={'bottom': axis})
        else:
            plot = self.plot_win.addPlot()
        plot.setLabel('top', name)
        self.plots.append(plot)
        return plot

    def show_data(self, index, need_show, data=(), _pen='w'):
        if need_show:
            window = windows.hamming(len(data))
            # chirp = data * fft.ifftshift(window)   # 加窗
            self.channel_plots[index].setData(20*np.log10(np.abs(fft.fftshift(fft.fft(data*window)))), pen=_pen)
            self.channel_plots[index].show()
        else:
            self.channel_plots[index].hide()
