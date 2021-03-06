import numpy
from math import ceil
import matplotlib.pylab as pl

mu = 0.01  # Convergence factor


def lms(x1: numpy.array, x2: numpy.array, N: int):
    # Verify argument shape.
    s1, s2 = x1.shape, x2.shape
    if len(s1) != 1 or len(s2) != 1 or s1[0] != s2[0]:
        raise Exception("Argument shape invalid, in 'lms' function")
    l = s1[0]

    # Coefficient matrix
    W = numpy.mat(numpy.zeros([1, 2 * N + 1]))
    # Coefficient (time) matrix
    Wt = numpy.mat(numpy.zeros([l, 2 * N + 1]))
    # Feedback (time) matrix
    y = numpy.mat(numpy.zeros([l, 1]))
    # Error (time) matrix
    e = numpy.mat(numpy.zeros([l, 1]))

    # Traverse channel data
    for i in range(N, l-N):
        x1_vec = numpy.asmatrix(x1[i-N:i+N+1])
        y[i] = x1_vec * numpy.transpose(W)
        e[i] = x2[i] - y[i]
        W += mu * e[i] * x1_vec
        Wt[i] = W

    # Find the coefficient matrix which has max maximum.
    Wt_maxs = numpy.max(Wt, axis=1)
    row_idx = numpy.argmax(Wt_maxs)
    max_W = Wt[row_idx]
    delay_count = numpy.argmax(max_W) - N

    # Plot
    time_range = numpy.arange(0, l)
    pl.figure(1)
    pl.subplot(221)
    pl.plot(time_range, x1)
    pl.title("Input signal")
    pl.subplot(222)
    pl.plot(time_range, x2, c="r")
    pl.plot(time_range, y, c="b")
    pl.title("Reference signal")
    pl.subplot(223)
    pl.plot(time_range, e, c="r")
    pl.title("Noise")
    pl.xlabel("time")

    pl.figure(2)
    time_range2 = numpy.arange(-N, N + 1)
    pl.plot(time_range2, numpy.transpose(max_W))
    pl.title("Maximal coefficient vector")

    pl.show()

    return delay_count


def fst_delay_snd(fst, snd, sampling, max_delay):
    min_N = int(ceil(max_delay * sampling))
    return float(lms(fst, snd, min_N)) / sampling