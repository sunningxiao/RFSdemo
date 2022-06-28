# tag: openmp
# cython: infer_types=True
# cython: language_level=3str
# cython: boundscheck=False
# cython: wraparound=False
# You can ignore the previous line.
# It's for internal testing of the cython documentation.

# distutils: extra_compile_args=-fopenmp
# distutils: extra_link_args=-fopenmp


import numpy as np
cimport cython
from cython.parallel import prange
from libc.math cimport sin, log, fmax, fmin, pow, M_PI
from libc.math cimport erf as _erf
from libc.math cimport cos as _cos
from libc.math cimport exp as _exp
from libc.string cimport memset
from libc.stdlib cimport malloc, free

cdef int THREAD_NUM = 6
DTYPE = np.float64
# cdef double pi = 3.141592653589793
cdef tuple _zero = ((), ())

# 线性运算函数**********************************************************************************
cdef int LINEAR = 1
ctypedef fused _linear_type:
    int
    double
    long long

cdef inline _linear_type linear(_linear_type x) nogil:
    return x

# 高斯运算函数**********************************************************************************
cdef int GAUSSIAN = 2
ctypedef fused _gaussian_type:
    int
    double
    long long

@cython.cdivision(True)
cdef inline _gaussian_type gaussian(_gaussian_type t, _gaussian_type std_sq2) nogil:
    """
    可并行的gaussian函数
    
    :param t: 
    :param std_sq2: 
    :return: 
    """
    return <_gaussian_type> _exp(-(t / std_sq2) * (t / std_sq2))

# erf运算函数**********************************************************************************
cdef int ERF = 3
ctypedef fused _erf_type:
    int
    double
    long long

@cython.cdivision(True)
cdef inline _erf_type erf(_erf_type t, _erf_type std_sq2) nogil:
    """
    可并行的erf函数

    :param t: 
    :param std_sq2: 
    :return: 
    """
    return <_erf_type> _erf(1/std_sq2*t)

# cos运算函数**********************************************************************************
cdef int COS = 4
ctypedef fused _cos_type:
    int
    double
    long long

cdef inline _cos_type cos(_cos_type t, _cos_type w) nogil:
    """
    可并行的cos函数

    :param t: 
    :param w: 
    :return: 
    """
    return <_cos_type> _cos(w*t)

# sinc运算函数**********************************************************************************
cdef int SINC = 5
ctypedef fused _sinc_type:
    int
    double
    long long

@cython.cdivision(True)
cdef inline _sinc_type sinc(_sinc_type x, _sinc_type bw=1) nogil:
    """
    可并行信号领域的sinc函数

    :param x: 
    :param bw:
    :return: 
    """
    if x == 0:
        return 1
    else:
        return <_sinc_type> (sin(M_PI * bw * x) / (M_PI * bw * x))

# exp运算函数**********************************************************************************
cdef int EXP = 6
ctypedef fused _exp_type:
    int
    double
    long long

cdef inline _exp_type exp(_exp_type t, _exp_type alpha) nogil:
    """
    可并行信号领域的exp函数

    :param t: 
    :param alpha:
    :return: 
    """
    return <_exp_type> _exp(alpha * t)

# interp运算函数**********************************************************************************
# INTERP = registerBaseFunc(lambda t, start, stop, points: np.interp(
#     t, np.linspace(start, stop, len(points)), points))
# TODO 当前插值算法与原版未成功匹配，np.arange与np.linspace两个函数行为不太一样
cdef int INTERP = 7

@cython.cdivision(True)
cdef inline double[::1] interp(double[::1] t, double start, double stop, tuple _y, double[::1] out):
    cdef Py_ssize_t ny = len(_y)
    cdef Py_ssize_t nt = t.shape[0]
    # cdef double[::1] x = np.linspace(start, stop, ny)
    cdef Py_ssize_t index, j
    cdef double step = (stop-start)/ny
    cdef double* y_p = <double*>malloc(ny*sizeof(double))
    cdef double[::1] y = <double[:ny]>y_p
    for j in range(ny):
        y[j] = _y[j]

    print(ny, nt, step, np.asarray(t))

    j = 0
    for j in prange(nt, nogil=True, num_threads=THREAD_NUM):
        if t[j]<=start:
            # out[j] = y[0]
            out[j] = 0
        elif t[j]>=stop:
            # out[j] = y[ny-1]
            out[j] = ny-1
        else:
            index = int((t[j]-start)//step)
            # out[j] = (y[index+1]-y[index])/step*(t[j]-start-index*step)
            out[j] = index
    free(y_p)
    return out


# linear_chirp运算函数**********************************************************************************
cdef int LINEARCHIRP = 8
ctypedef fused _linear_chirp_type:
    int
    double
    long long

@cython.cdivision(True)
cdef inline _linear_chirp_type linear_chirp(_linear_chirp_type t,
                                            _linear_chirp_type f0, _linear_chirp_type f1,
                                            _linear_chirp_type T, _linear_chirp_type phi0) nogil:
    """
    可并行的linear_chirp函数
    """
    # phi0 + 2 * np.pi * ((f1 - f0) / (2 * T) * t ** 2 + f0 * t)
    return <_linear_chirp_type> sin(phi0 + 2 * M_PI * ((f1 - f0) / (2 * T) * pow(t, 2) + f0 * t))

# exponential_chirp运算函数**********************************************************************************
cdef int EXPONENTIALCHIRP = 9
ctypedef fused _exponential_chirp_type:
    int
    double
    long long

@cython.cdivision(True)
cdef inline _exponential_chirp_type exponential_chirp(_exponential_chirp_type t,
                                                      _exponential_chirp_type f0,
                                                      _exponential_chirp_type alpha,
                                                      _exponential_chirp_type phi0) nogil:
    """
    可并行的exponential_chirp函数
    """
    return <_exponential_chirp_type> sin(phi0 + 2 * M_PI * f0 * (_exp(alpha * t) - 1) / alpha)

# hyperbolic_chirp运算函数**********************************************************************************
cdef int HYPERBOLICCHIRP = 10
ctypedef fused _hyperbolic_chirp_type:
    int
    double
    long long

@cython.cdivision(True)
cdef inline _hyperbolic_chirp_type hyperbolic_chirp(_hyperbolic_chirp_type t,
                                                    _hyperbolic_chirp_type f0,
                                                    _hyperbolic_chirp_type k,
                                                    _hyperbolic_chirp_type phi0) nogil:
    """
    可并行的hyperbolic_chirp函数
    """
    return <_hyperbolic_chirp_type>sin(phi0 + 2 * M_PI * f0 / k * log(1 + k * t))


cdef double[::1] array_clip(double[::1] _wave, double min_value, double max_value) nogil:
    cdef Py_ssize_t x_max = _wave.shape[0]
    cdef Py_ssize_t x

    for x in prange(x_max, nogil=True, num_threads=THREAD_NUM):
        _wave[x] = fmin(fmax(_wave[x], min_value), max_value)
    return _wave


# cdef double[::1] array_pow(double[::1] _wave, double _p) nogil:
#     """
#     一维数组乘方
#
#     :param _wave:
#     :param p:
#     :return:
#     """
#     cdef Py_ssize_t x_max = _wave.shape[0]
#     cdef Py_ssize_t x
#
#     for x in prange(x_max, nogil=True, num_threads=THREAD_NUM):
#         _wave[x] = pow(_wave[x], _p)
#
#     return _wave
#
#
# cdef double[::1] array_muli(double[::1] _wave, double[::1] _a) nogil:
#     """
#     一维数组按位相乘
#
#     :param _wave:
#     :param _a:
#     :return:
#     """
#     cdef Py_ssize_t x_max = _wave.shape[0]
#     cdef Py_ssize_t x
#
#     for x in prange(x_max, nogil=True, num_threads=THREAD_NUM):
#         _wave[x] = _a[x]*_wave[x]
#
#     return _wave
#
# cdef double[::1] array_muli_double(double[::1] _wave, double _a) nogil:
#     """
#     一维数组按位相乘
#
#     :param _wave:
#     :param _a:
#     :return:
#     """
#     cdef Py_ssize_t x_max = _wave.shape[0]
#     cdef Py_ssize_t x
#
#     for x in prange(x_max, nogil=True, num_threads=THREAD_NUM):
#         _wave[x] = _a*_wave[x]
#
#     return _wave
#
#
# cdef double[::1] array_add(double[::1] _wave, double[::1] _a) nogil:
#     """
#     一维数组按位相加
#
#     :param _wave:
#     :param _a:
#     :return:
#     """
#     cdef Py_ssize_t x_max = _wave.shape[0]
#     cdef Py_ssize_t x
#
#     for x in prange(x_max, nogil=True, num_threads=THREAD_NUM):
#         _wave[x] = _a[x]+_wave[x]
#
#     return _wave


cdef double[::1] wave_add(double[::1] _wave, double[::1] _a, double _m) nogil:
    """
    一维数组按位相加

    :param _wave: 
    :param _a: 
    :param _m: 
    :return: 
    """
    cdef Py_ssize_t x_max = _wave.shape[0]
    cdef Py_ssize_t x

    for x in prange(x_max, nogil=True, num_threads=THREAD_NUM):
        _wave[x] = _a[x]+_wave[x]*_m

    return _wave


cdef double[::1] compute_func(tuple mt, double[::1] array, double[::1] _m, double _p=1):
    cdef int Type
    cdef list args
    cdef double shift
    cdef Py_ssize_t x_max = array.shape[0]
    cdef Py_ssize_t i = 0
    out = np.zeros((array.shape[0],), dtype=DTYPE)
    cdef double[::1] out_view = out
    Type, *args, shift = mt

    # 预先定义传入的参数
    cdef double para_0, para_1, para_2, para_3, para_4, para_5, para_6
    cdef tuple points

    if Type == LINEAR:
        for i in prange(x_max, nogil=True, num_threads=THREAD_NUM):
            out_view[i] = _m[i]*pow(linear(array[i]-shift), _p)
    elif Type == GAUSSIAN:
        para_0 = <double>args[0]
        for i in prange(x_max, nogil=True, num_threads=THREAD_NUM):
            out_view[i] = _m[i]*pow(gaussian(array[i] - shift, para_0), _p)
    elif Type == ERF:
        para_0 = <double> args[0]
        for i in prange(x_max, nogil=True, num_threads=THREAD_NUM):
            out_view[i] = _m[i]*pow(erf(array[i] - shift, para_0), _p)
    elif Type == COS:
        para_0 = <double> args[0]
        for i in prange(x_max, nogil=True, num_threads=THREAD_NUM):
            out_view[i] = _m[i]*pow(cos(array[i] - shift, para_0), _p)
    elif Type == SINC:
        para_0 = <double> args[0]
        for i in prange(x_max, nogil=True, num_threads=THREAD_NUM):
            out_view[i] = _m[i]*pow(sinc(array[i] - shift, para_0), _p)
    elif Type == EXP:
        para_0 = <double> args[0]
        for i in prange(x_max, nogil=True, num_threads=THREAD_NUM):
            out_view[i] = _m[i]*pow(exp(array[i] - shift, para_0), _p)
    elif Type == INTERP:
        para_0, para_1, points = args[0], args[1], args[2]
        out_view = interp(array, para_0, para_1, points, out_view)
    elif Type == LINEARCHIRP:
        para_0, para_1, para_2, para_3 = args[0], args[1], args[2], args[3]
        for i in prange(x_max, nogil=True, num_threads=THREAD_NUM):
            out_view[i] = _m[i]*pow(linear_chirp(array[i], para_0, para_1, para_2, para_3), _p)
    elif Type == EXPONENTIALCHIRP:
        para_0, para_1, para_2 = args[0], args[1], args[2]
        for i in prange(x_max, nogil=True, num_threads=THREAD_NUM):
            out_view[i] = _m[i] * pow(exponential_chirp(array[i], para_0, para_1, para_2), _p)
    elif Type == HYPERBOLICCHIRP:
        para_0, para_1, para_2 = args[0], args[1], args[2]
        for i in prange(x_max, nogil=True, num_threads=THREAD_NUM):
            out_view[i] = _m[i] * pow(hyperbolic_chirp(array[i], para_0, para_1, para_2), _p)

    return out_view


@cython.boundscheck(False)
@cython.wraparound(False)
def gen_wave(object wave, double[::1] x):
    cdef double wave_min = wave.min
    cdef double wave_max = wave.max
    cdef tuple seq = wave.seq
    out = np.zeros((x.shape[0], ), dtype=DTYPE)
    cdef double[::1] out_view = out

    cdef long[::1] range_list = np.searchsorted(x, wave.bounds)
    cdef Py_ssize_t _size = range_list.size
    cdef Py_ssize_t i = 0

    cdef Py_ssize_t start = 0
    cdef Py_ssize_t stop = 0
    cdef double[::1] _wave, _x
    cdef double[::1] __ret

    # 预先申请好
    # cdef double *__zero = <double*>malloc(x.shape[0]*sizeof(double))
    # memset(__zero, 0, x.shape[0]*sizeof(double))
    # cdef double[::1] zero = <double[:x.shape[0]*sizeof(double)]>__zero

    # cdef double *__ones = <double*>malloc(x.shape[0]*sizeof(double))
    # memset(__ones, 1, x.shape[0]*sizeof(double))
    # cdef double[::1] ones = <double[:x.shape[0]*sizeof(double)]>__ones

    for i in range(_size):
        stop = <Py_ssize_t>range_list[i]
        if start < stop and seq[i] != _zero:
            _wav = seq[i]
            _x = x[start:stop]
            # _wave = zero[start:stop]
            _wave = np.zeros((_x.shape[0],), dtype=DTYPE)
            for t, v in zip(*_wav):
                # __ret = ones[start:stop]
                __ret = np.ones((_x.shape[0],), dtype=DTYPE)
                for mt, n in zip(*t):
                    # if mt not in lru_cache:
                    #     # Type, *args, shift = mt
                    #     lru_cache[mt] = compute_func(mt, _x)
                    #     # print(lru_cache)
                    __ret = compute_func(mt, _x, __ret, n)
                _wave = wave_add(__ret, _wave, v)
            out_view[start:stop] = array_clip(_wave, wave_min, wave_max)
        start = stop
    # free(__zero)
    # free(__ones)
    return out
#
#
# @cython.boundscheck(False)
# @cython.wraparound(False)
# def compute_sinc(_sinc_type[:] array_1):
#
#     cdef Py_ssize_t x_max = array_1.shape[0]
#
#     if _sinc_type is int:
#         dtype = np.intc
#     elif _sinc_type is double:
#         dtype = np.double
#     elif _sinc_type is cython.longlong:
#         dtype = np.longlong
#
#     result = np.zeros((x_max, ), dtype=dtype)
#     cdef _sinc_type[:] result_view = result
#
#     cdef Py_ssize_t x
#
#     # We use prange here.
#     for x in prange(x_max, nogil=True, num_threads=THREAD_NUM):
#         result_view[x] = erf(array_1[x], 2)
#
#     return result
