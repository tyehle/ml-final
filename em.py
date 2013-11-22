""" Defines Gaussian Discriminant Analysis em algorithm.
"""

# disable variable name warnings
# pylint: disable=C0103

import numpy
import math
import random

# This is just a self reminder to try and do arrays so that a single element
# of data is contained in a column.  This means that the input data array
# should be in R(a x n), and the array of means should be in R(a x m).

def em(data, m, iteration_cap, tolerance):
    """ Runs the em algorithm """
    n = data.shape[1]
    a = data.shape[0]

    # pick initial values for phi to be equal
    phi = numpy.ones(m) / m

    # pick inital mu's randomly from the data
    mu = numpy.array([data[:, int(random.random() * n)] for _ in range(0, m)])

    # set sigma as the identity matrix for starters
    sig = numpy.dstack([numpy.eye(a) for _ in range(0, m)])

    for i in range(0, iteration_cap):
        w = _e_step(data, m, phi, mu, sig)
        (new_phi, new_mu, new_sig) = _m_step(data, m, w)

        diff = (new_mu - mu)*(new_mu - mu)

        phi = new_phi
        mu = new_mu
        sig = new_sig

        if diff[numpy.argmax(diff)] < tolerance:
            print("Broke: " + i)
            break


    return (w, phi, mu, sig)


def _e_step(data, m, phi, mu, sig):
    """ Does the estimation step of the em algorithm.

        The data should be a an array with n columns with a single data point in
        each column. Data points can be any dimension vector.
    """

    n = data.shape[1]
    w = numpy.zeros((m, n))

    for i in range(0, n):

        # find w
        # w_{ij} = \frac{ \mathcal{N}(\mu_j, \Sigma_j) \phi_j }
        #          { \sum_{k=1}^m \mathcal{N}(\mu_k, \Sigma_k) \phi_k }

        nums = [_gauss(data[:, k], mu[:, k], sig[:, :, k])*phi[k] \
                for k in range(0, m)]
        denom = sum(nums)

        # nomalize so the sum of all nums is 1
        # zero case check
        if denom is 0:
            # probabilities should be equal
            nums = numpy.ones((m)) / m
        else:
            nums = numpy.array(nums) / denom

        # for all j set w_{ij}
        w[:, i] = nums

    return w


def _m_step(data, m, w):
    """ Does the maximization step of the em algoithm """
    n = data.shape[1]
    a = data.shape[0]

    phi = numpy.zeros(m)
    mu = numpy.zeros(a, m)
    sig = numpy.zeros(a, a, m)

    for j in range(0, m):
        # \phi_j = \frac{1}{n} \sum_{i=1}^n w_{ij}
        # \mu_j = \frac{ \sum_{i=1}^n w_{ij} x_i } { \sum_{i=1}^n w_{ij} }
        # \Sigma_j = \frac { \sum_{i=1}^n w_{ij} (x_i - \mu_j)(x_i - \mu_j)^T }
        #            { \sum_{i=1}^n w_{ij} }

        # find the sum of the wi's and mu_j
        mu_j = numpy.zeros(a)
        sum_wij = 0
        for i in range(0, n):
            sum_wij += w[j, i]
            mu_j += w[j, i] * data[:, i]
        mu_j = 1.0/sum_wij * mu_j

        # find sig_j
        sig_j = numpy.zeros(a, a)
        for i in range(0, n):
            diff = numpy.array([(data[:, i] - mu_j)])
            sig_j += w[j, i] * diff.T*diff
        sig_j = 1.0/sum_wij * sig_j

        # store the results in the arrays to return
        phi[j] = 1.0/n * sum_wij
        mu[:, j] = mu_j
        sig[:, :, j] = sig_j

    return (phi, mu, sig)


def _gauss(x, mu, sig):
    """ Finds the probability of the point x being drawn from the normal
        distribution defined by mu and sig.
    """
    a = x.shape[0]
    return 1.0/math.sqrt((2*math.pi)**a * numpy.linalg.det(sig)) * \
        math.exp(-0.5 * (x-mu).T*sig**-1*(x-mu))
