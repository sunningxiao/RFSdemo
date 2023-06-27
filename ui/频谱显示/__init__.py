from typing import TYPE_CHECKING
import pyqtgraph as pg
import numpy as np
from numpy import fft
# from scipy.signal import windows

from PyQt5 import QtCore, QtGui, QtWidgets

from ui.频谱显示 import spectrum_ui

if TYPE_CHECKING:
    from ui import RFSControl


class SpectrumScreen(QtWidgets.QDialog, spectrum_ui.Ui_Dialog):
    def __init__(self, ui_parent):
        super(SpectrumScreen, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('谱快视')
        self.ui_parent: "RFSControl" = ui_parent
        self.plot_win = pg.GraphicsLayoutWidget()
        self.wave_show_win.addWidget(self.plot_win)
        self.plots = []
        # 频谱展示
        self.spectrum_plot = self.append_plot('回波谱分析')
        self.channel_plots = [self.spectrum_plot.plot(name=f'chnl{i}') for i in range(8)]

    def append_plot(self, name, axis=None):
        if axis:
            plot = self.plot_win.addPlot(axisItems={'bottom': axis})
        else:
            plot = self.plot_win.addPlot()
        plot.setLabel('top', name)
        self.plots.append(plot)
        plot.setLabel('bottom', 'Freq', 'Hz')
        return plot

    def show_data(self, index, need_show, data=(), _pen='w'):
        if need_show:
            window = np.hamming(len(data))
            wdata = window*data
            srate = self.ui_parent.rfs_kit.get_param_value('ADC采样率')*1e6
            multi = self.ui_parent.rfs_kit.get_param_value('ADC 抽取倍数')
            _rate = srate/multi
            self.channel_plots[index].setData(
                x=np.fft.fftshift(np.fft.fftfreq(len(data), 1/_rate)),
                y=20*np.log10(np.abs(np.fft.fftshift(fft.fft(data)))),
                pen=_pen
            )
            self.channel_plots[index].show()
        else:
            self.channel_plots[index].hide()
