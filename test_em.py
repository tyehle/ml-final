#!/usr/bin/python

import numpy
import random
import math
import matplotlib.pyplot as mpl

import em


def zdist(d):
    return numpy.matrix([ random.normalvariate(0, 1) for _ in range(0, d) ]).T


def multi_gauss(mu, sig, n):
    dim = mu.shape[0]
    data = [ sig*zdist(dim) + mu for _ in range(0, n) ]
    return numpy.concatenate(data, axis=1)


def rand(max_val, min_val=0):
    return (random.random() * (max_val - min_val)) + min_val


if __name__ == '__main__':

    n = 1000
    m = 3
    colors = ['r+', 'g+', 'b+']
    data = []

    for i in range(0, m):
        # generate a random positive definite matrix
        a = rand(4,min_val=1)
        cov = rand(min_val=-1, max_val=1)
        b = rand(min_val=cov*cov/a, max_val=4)
        sig = numpy.matrix([[a, cov], [cov, b]])
        mu = numpy.matrix([[rand(20)], [rand(20)]])
        data.append(multi_gauss(mu, sig, n/m))

        mpl.plot(data[i][0, :], data[i][1, :], colors[i])

    mpl.show()

    data = numpy.concatenate(data, axis=1)
    print(data.shape)

    (w, phi, mu, sig) = em.em(data, 3, 20, 0.01)
