import scipy.signal as sig
from scipy import linalg
import numpy as np
import copy


def get_db(data, freq, sample_rate=5e9):
    fft_res = np.fft.fft(data)
    fft_db: "np.ndarray" = 10*np.log10(np.abs(fft_res))
    return fft_db.max()


def get_snr(data, nHarmonics=6, samplerate=4e9):
    """获取信号的snr，信号功率，噪声功率

    :param data:
    :param nHarmonics:
    :param samplerate:
    :return: [snr, 带内信号功率dB，带内噪声功率dB]
    """
    faxis, ps = sig.periodogram(data, fs=samplerate,
                                window=('kaiser', 38))  # get periodogram, parametrized like in matlab
    fundBin = np.argmax(ps)  # estimate fundamental at maximum amplitude, get the bin number
    fundIndizes = getIndizesAroundPeak(ps, fundBin)  # get bin numbers around fundamental peak
    fundFrequency = faxis[fundBin]  # frequency of fundamental
    harmonicFs = getHarmonics(fundFrequency, samplerate, nHarmonics=nHarmonics, aliased=True)  # get harmonic

    harmonicBorders = np.zeros([2, nHarmonics], dtype=np.int16).T
    fullHarmonicBins = np.array([], dtype=np.int16)
    fullHarmonicBinList = []
    harmPeakFreqs = []
    harmPeaks = []
    for i, harmonic in enumerate(harmonicFs):
        searcharea = 0.1 * fundFrequency
        estimation = harmonic

        binNum, freq = getPeakInArea(ps, faxis, estimation, searcharea)
        harmPeakFreqs.append(freq)
        harmPeaks.append(ps[binNum])
        allBins = getIndizesAroundPeak(ps, binNum, searchWidth=1000)
        fullHarmonicBins = np.append(fullHarmonicBins, allBins)
        fullHarmonicBinList.append(allBins)
        harmonicBorders[i, :] = [allBins[0], allBins[-1]]

    fundIndizes.sort()
    pFund = bandpower(ps[fundIndizes[0]:fundIndizes[-1]])  # get power of fundamental
    fundRemoved = np.delete(ps, fundIndizes)  # remove the fundamental (start constructing the noise-only signal)
    fAxisFundRemoved = np.delete(faxis, fundIndizes)
    noisePrepared = copy.copy(ps)
    noisePrepared[fundIndizes] = 0
    noisePrepared[fullHarmonicBins] = 0
    noiseMean = np.median(noisePrepared[noisePrepared != 0])
    noisePrepared[fundIndizes] = noiseMean
    noisePrepared[fullHarmonicBins] = noiseMean
    noisePower = bandpower(noisePrepared)

    snr = 10 * np.log10(pFund / noisePower)

    return [snr, 10 * np.log10(pFund), 10 * np.log10(noisePower)]
    # return {'SNR': snr, 'SignalPower': 10*np.log10(pFund), 'NoisePower': 10*np.log10(noisePower)}


def bandpower(ps, mode='psd'):
    """
    estimate bandpower, see https://de.mathworks.com/help/signal/ref/bandpower.html
    """
    if mode == 'time':
        x = ps
        l2norm = linalg.norm(x) ** 2. / len(x)
        return l2norm
    elif mode == 'psd':
        return sum(ps)


def getIndizesAroundPeak(arr, peakIndex, searchWidth=1000):
    peakBins = []
    magMax = arr[peakIndex]
    curVal = magMax
    for i in range(searchWidth):
        newBin = peakIndex + i
        newVal = arr[newBin]
        if newVal > curVal:
            break
        else:
            peakBins.append(int(newBin))
            curVal = newVal
    curVal = magMax
    for i in range(searchWidth):
        newBin = peakIndex - i
        newVal = arr[newBin]
        if newVal > curVal:
            break
        else:
            peakBins.append(int(newBin))
            curVal = newVal
    return np.array(list(set(peakBins)))


def freqToBin(fAxis, Freq):
    return np.argmin(abs(fAxis - Freq))


def getPeakInArea(psd, faxis, estimation, searchWidthHz=10):
    """
    returns bin and frequency of the maximum in an area
    """
    binLow = freqToBin(faxis, estimation - searchWidthHz)
    binHi = freqToBin(faxis, estimation + searchWidthHz)
    peakbin = binLow + np.argmax(psd[binLow:binHi])
    return peakbin, faxis[peakbin]


def getHarmonics(fundFrequency, sr, nHarmonics=6, aliased=False):
    harmonicMultipliers = np.arange(2, nHarmonics + 2)
    harmonicFs = fundFrequency * harmonicMultipliers
    if not aliased:
        harmonicFs[harmonicFs > sr / 2] = -1
        harmonicFs = np.delete(harmonicFs, harmonicFs == -1)
    else:
        nyqZone = np.floor(harmonicFs / (sr / 2))
        oddEvenNyq = nyqZone % 2
        harmonicFs = np.mod(harmonicFs, sr / 2)
        harmonicFs[oddEvenNyq == 1] = (sr / 2) - harmonicFs[oddEvenNyq == 1]
    return harmonicFs


def to_csv(X, fmt='%.18e', delimiter=' ', newline='\n', header='', footer='', comments='# ', encoding=None):
    def asstr(s):
        if isinstance(s, bytes):
            return s.decode('latin1')
        return str(s)

    if isinstance(fmt, bytes):
        fmt = asstr(fmt)
    delimiter = asstr(delimiter)

    data_list = []

    X = np.asarray(X)

    # Handle 1-dimensional arrays
    if X.ndim == 0 or X.ndim > 2:
        raise ValueError(
            "Expected 1D or 2D array, got %dD array instead" % X.ndim)
    elif X.ndim == 1:
        # Common case -- 1d array of numbers
        if X.dtype.names is None:
            X = np.atleast_2d(X).T
            ncol = 1

        # Complex dtype -- each field indicates a separate column
        else:
            ncol = len(X.dtype.names)
    else:
        ncol = X.shape[1]

    iscomplex_X = np.iscomplexobj(X)
    # `fmt` can be a string with multiple insertion points or a
    # list of formats.  E.g. '%10.5f\t%10d' or ('%10.5f', '$10d')
    if type(fmt) in (list, tuple):
        if len(fmt) != ncol:
            raise AttributeError('fmt has wrong shape.  %s' % str(fmt))
        format = asstr(delimiter).join(map(asstr, fmt))
    elif isinstance(fmt, str):
        n_fmt_chars = fmt.count('%')
        error = ValueError('fmt has wrong number of %% formats:  %s' % fmt)
        if n_fmt_chars == 1:
            if iscomplex_X:
                fmt = [' (%s+%sj)' % (fmt, fmt), ] * ncol
            else:
                fmt = [fmt, ] * ncol
            format = delimiter.join(fmt)
        elif iscomplex_X and n_fmt_chars != (2 * ncol):
            raise error
        elif ((not iscomplex_X) and n_fmt_chars != ncol):
            raise error
        else:
            format = fmt
    else:
        raise ValueError('invalid fmt: %r' % (fmt,))

    if len(header) > 0:
        header = header.replace('\n', '\n' + comments)
        data_list.append(comments + header + newline)
    if iscomplex_X:
        for row in X:
            row2 = []
            for number in row:
                row2.append(number.real)
                row2.append(number.imag)
            s = format % tuple(row2) + newline
            data_list.append(s.replace('+-', '-'))
    else:
        for row in X:
            try:
                v = format % tuple(row) + newline
            except TypeError as e:
                raise TypeError("Mismatch between array dtype ('%s') and "
                                "format specifier ('%s')"
                                % (str(X.dtype), format)) from e
            data_list.append(v)

    if len(footer) > 0:
        footer = footer.replace('\n', '\n' + comments)
        data_list.append(comments + footer + newline)
    return ''.join(data_list)

