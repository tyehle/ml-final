""" Contains methods for finding clusters in data """

# pylint: disable=C0103

import numpy
import math
import random as rand

def dunn_index(data, labels, mu):
    """ Computes the Dunn index for the given set of clusters. """
    n = len(labels)
    m = mu.shape[1]
    data = numpy.asarray(data)

    # group data in to classes
    classes = []
    for i in range(m):
        classes.append([ data[:, j] for j in range(n) if labels[j] == i ])

    # find min distance between any two means
    min_dist = float("inf")
    for i in range(m):
        for j in range(m):
            if i >= j:
                continue
            diff = numpy.asmatrix(mu[:, i] - mu[:, j])
            dist = math.sqrt(diff * diff.T)
            if dist < min_dist:
                min_dist = dist

    # find max distance between any two data points in the same cluster
    max_dist = 0.0
    for i in range(m):
        points = len(classes[i])
        for a in range(points):
            for b in range(points):
                if a >= b:
                    continue
                diff = numpy.asmatrix(classes[i][a] - classes[i][b])
                dist = math.sqrt(diff * diff.T)
                if dist > max_dist:
                    max_dist = dist

    return min_dist / max_dist


def mean(arr):
    """ This method will take in an array and return
        the mean point of any n dimensional matrix. """
    sums = numpy.zeros( (1, len(arr[0])) )
    length = len(arr)

    for row in range(length):
        for col in range(0, len(sums[0])):
            sums[0, col] += arr[row, col]

    for i in range(len(sums[0])):
        sums[0, i] /= length

    return sums

def min_index(arr):
    """ This method will take in an array and return the index
        of the minimum value. """
    index = 0

    for i in range(1, len(arr)):
        if arr[i, 0] < arr[index, 0]:
            index = i

    return index

def kmeans(data, num_clusters):
    """ This method will take in a set of data dn the number of clusters
        that the algorithm wants to find (m). This will then return the
        data witha cluster label.

        The input data should be a 2D array as defined by numpy.zeros. """
    # If the data structure that is recieved is numpy.matrix,
	# this will convert it to numpy.array.
    if(type(data) == numpy.matrix):
        data = numpy.asarray(data)

    # How many data points there are
    length = len(data)
    # The dimension of the data point
    dim = len(data[0])
    # The label that is assigned to.
    labels = numpy.zeros( (length, 1) )

    cur_means = numpy.zeros( (num_clusters, dim) )

    #randomize means by choosing 3 points from the data at random.
    for i in range(num_clusters):
        index = math.floor(length * rand.random())
        cur_means[i, :] = data[index, :]

    converged = False

    while not converged:
        # Relabel each data point by its closest mean.
        labels = relabel_data(data, num_clusters, cur_means)

        prev_means = numpy.copy(cur_means)

        # Re-evaluate each mean by taking the mean of the cluster.
        cur_means = reevaluate_means(data, num_clusters, labels)

        # This will check for convergence by seeing if the difference
        # between the previous means and the current means have changed.
        result = cur_means == prev_means
        converged = result.all()

    # Combine the labels and the data together and return
    # it with each cluster mean.
    final_data = numpy.zeros( (length, dim + 1) )

    final_data[:, 0:dim] = data[:, :]
    final_data[:, dim] = labels[:, 0]

    return (cur_means, final_data)

def relabel_data(data, num_clusters, cur_means):
    """ Go through each data point and relabel it based on
        its closest mean. """
    labels = numpy.zeros( (len(data), 1) )
    for i in range(len(data)):
        # Go through each cluster
        distance = numpy.zeros( (num_clusters, 1) )
        for j in range(num_clusters):
            for k in range(0, len(data[0])):
                distance[j, 0] += (data[i, k] - cur_means[j, k])**2
            distance[j, 0] = math.sqrt(distance[j, 0])
        index = min_index(distance)
        labels[i] = index

    return labels

def reevaluate_means(data, num_clusters, labels):
    """ This will recompute each mean based on the mean of the new cluster
        of the data. """
    means = numpy.zeros( (num_clusters, len(data[0])) )
    for j in range(num_clusters):
        label_array = numpy.zeros( (0, len(data[0])) )
        for i in range(len(data)):
            if labels[i] == j:
                label_array = numpy.vstack( (label_array, data[i, :]) )
        means[j, :] = mean(label_array)[0, :]
    return means


# This is just a self reminder to try and do arrays so that a single element
# of data is contained in a column.  This means that the input data array
# should be in R(a x n), and the array of means should be in R(a x m).

def em(data, m, iteration_cap, tolerance):
    """ Runs the em algorithm """
    data = numpy.asarray(data) # convert data to an array
    n = data.shape[1]
    a = data.shape[0]

    # pick initial values for phi to be equal
    phi = numpy.ones(m) / m

    # pick inital mu's randomly from the data
    mu = numpy.array([data[:, int(rand.random() * n)] for _ in range(0, m)]).T

    # set sigma as the identity matrix for starters
    sig = numpy.dstack([numpy.eye(a) for _ in range(0, m)])

    for i in range(0, iteration_cap):
        w = _e_step(data, m, phi, mu, sig)
        (new_phi, new_mu, new_sig) = _m_step(data, m, w)

        print(i)

        diff = _get_max([(new_mu - mu), (new_sig - sig), (new_phi - phi)])

        phi = new_phi
        mu = new_mu
        sig = new_sig

        if diff < tolerance:
            print("Converged: %i" % i)
            break


    return (w, phi, mu, sig)


def _get_max(arrays):
    """ Gets the maximum absolute value out of the given array of arrays or
        matrices.
    """
    maximum = 0
    for i in range(0, len(arrays)):
        vals = arrays[i].flatten()
        for j in range(0, len(vals)):
            if abs(vals[j]) > maximum:
                maximum = abs(vals[j])

    return maximum


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

        nums = [_gauss(data[:, i], mu[:, k], sig[:, :, k])*phi[k] \
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
    mu = numpy.zeros((a, m))
    sig = numpy.zeros((a, a, m))

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
        sig_j = numpy.zeros((a, a))
        for i in range(0, n):
            diff = numpy.matrix([(data[:, i] - mu_j)])
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
    diff = numpy.asmatrix(x - mu)
    return 1.0/math.sqrt((2*math.pi)**a * numpy.linalg.det(sig)) * \
        math.exp(-0.5 * (diff * numpy.linalg.inv(sig) * diff.T)[0,0])


def gda(data, labels, m):
    """ Expects data as a numpy array with a single data point in a column.
        Expects labels to be in [0, m) as a list.
    """
    data = numpy.asarray(data)
    a = data.shape[0]
    n = data.shape[1]

    # compute phi
    phi = numpy.array([ 1.0/n * _occurrences(j, labels) for j in range(m) ])

    # compute mu
    mu = numpy.zeros((a, m))
    for i in range(n):
        j = labels[i]
        mu[:, j] = mu[:, j] + data[:, i]
    for j in range(m):
        mu[:, j] = 1.0/_occurrences(j, labels) * mu[:, j]

    # compute sigma
    sig = numpy.zeros((a, a, m))
    for i in range(n):
        j = labels[i]
        diff = numpy.asmatrix(data[:, i] - mu[:, j])
        sig[:, :, j] = sig[:, :, j] + diff.T * diff
    for j in range(m):
        sig[:, :, j] = 1.0/_occurrences(j, labels) * sig[:, :, j]

    # return a function that classifies new data
    def classify(x):
        """ Classifies the data point x using the learned parameters. """
        label = 0
        prob = _gauss(x, mu[:, 0], sig[:, :, 0]) * phi[0]
        for j in range(1, m):
            new_prob = _gauss(x, mu[:, j], sig[:, :, j]) * phi[j]
            if new_prob > prob:
                label = j
                prob = new_prob
        return label
        
    return classify, phi, mu, sig


def _occurrences(item, items):
    """ Returns the number of occurrences of item in the list of items. """
    n = 0
    for e in items:
        if e is item:
            n = n + 1

    return n
