import numpy as np

from tools.data_unpacking import UnPackage

_pd = 17
_td = 8
_data = []

with open(r"C:\Users\56585\Downloads\data-adda_0.data", 'rb') as fp:
    data: np.ndarray = np.frombuffer(fp.read(), dtype='u4')
unpack_data = UnPackage.channel_data_filter(data, list(range(_pd)), list(range(_td)))
for pd in range(_pd):
    td_list = []
    for td in range(_td):
        td_list.append(unpack_data[0][pd][td])
    _data.append(td_list)
_data = np.array(_data)

print(_data.shape)


def csv(X, fmt='%.18e', delimiter=' ', newline='\n', header='', footer='', comments='# ', encoding=None):
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
