#!/usr/bin/python

""" Contains tests for the em algorithm
"""

# disable variable name warnings
# pylint: disable=C0103

import numpy
import random
import math
import matplotlib.pyplot as mpl
import itertools

import clustering


def zdist(d):
    """ Returns a d dimensional vector according to the standard multivariate
        normal distribution.
    """
    return numpy.matrix([ random.normalvariate(0, 1) for _ in range(0, d) ]).T


def multi_gauss(mu, sig, n):
    """ Returns a matrix of n data points distributed according to the
        multivariate gaussian defined by mu and sig.
    """
    dim = mu.shape[0]
    dev = numpy.asmatrix(numpy.linalg.cholesky(sig))
    data = [ dev*zdist(dim) + mu for _ in range(0, n) ]
    return numpy.concatenate(data, axis=1)


def rand(max_val, min_val=0):
    """ Returns a random float between the min and max vals. """
    return (random.random() * (max_val - min_val)) + min_val


def unit_circle(i, n):
    """ Returns the ith point of an n length sequence of evenly spaced points
        on the unit circle.
    """
    theta = math.pi*2 * i/n
    return numpy.array([[math.cos(theta)], [math.sin(theta)]])


def plot_contour(mu, sig, plot):
    """ Plots the one sigma contour of the gaussian defined by mu and sig on
        the given plot.
    """
    n = 100
    contour = [ numpy.asmatrix(sig) * unit_circle(i, n) + mu \
                for i in range(0, n+1) ]
    contour = numpy.asarray(numpy.concatenate(contour, axis=1))
    return plot.plot(contour[0, :], contour[1, :], 'k-')


def accuracy(perm, in_labels, out_labels):
    """ Determines the accuracy of the in_labels to the out_labels transformed
        by the given permutation.
    """
    num_correct = 0.0
    for i in range(len(in_labels)):
        if in_labels[i] == perm[out_labels[i]]:
            num_correct += 1.0
    return num_correct/len(in_labels)

def run_em_test():
    """ Runs the test on the em algorithm. """
    n = 1000
    m = 3
    colors = ['r+', 'g+', 'b+']
    data = []
    labels = []

    fig = mpl.figure()
    genplot = fig.add_subplot(1, 2, 1)
    for i in range(0, m):
        # generate a random positive definite matrix
        a = rand(4, min_val=1)
        cov = rand(min_val=-1, max_val=1)
        b = rand(min_val=cov*cov/a, max_val=4)
        sig = numpy.matrix([[a, cov], [cov, b]])
        mu = numpy.matrix([[rand(20)], [rand(20)]])
        data.append(multi_gauss(mu, sig, n/m))
        labels.extend([ i for _ in range(0, n/m) ])

        genplot.plot(data[i][0, :], data[i][1, :], colors[i])
        plot_contour(mu, sig, genplot)

    genplot.set_title('Input Data')

    # redefine n to be the number of data points we have
    n = n/m*m

    classes = m
    input_data = numpy.concatenate(data, axis=1)
    (w, _, mu, sig) = clustering.em(input_data, classes, 40, 0.01)

    out_labels = [ int(numpy.argmax(w[:, i])) \
                   for i in range(input_data.shape[1]) ]

    outplot = fig.add_subplot(1, 2, 2)

    # plot the data
    if m == classes: # colorize misclassed points and print accuracy
        # find the best permutation of mu on the initial set of means
        perms = list(itertools.permutations(range(0, m)))
        # Note: a permutation maps the found mus to the generated mus
        best_perm = perms[0]
        best_acc = accuracy(perms[0], labels, out_labels)
        for i in range(1, len(perms)):
            acc = accuracy(perms[i], labels, out_labels)
            if acc >= best_acc:
                best_acc = acc
                best_perm = perms[i]

        correct = [ input_data[:, i] for i in range(n) \
                    if labels[i] == best_perm[out_labels[i]] ]
        correct = numpy.concatenate(correct, axis=1)
        outplot.plot(correct[0, :], correct[1, :], 'b+')

        incorrect = [ input_data[:, i] for i in range(n) \
                      if labels[i] != best_perm[out_labels[i]] ]
        if incorrect:
            incorrect = numpy.concatenate(incorrect, axis=1)
            outplot.plot(incorrect[0, :], incorrect[1, :], 'ro')

        print("Accuracy: %.3f (%i / %i)" % (best_acc, len(correct.T), n))

    else: # plot the points with their new classes
        for j in range(0, m):
            outplot.plot(data[j][0, :], data[j][1, :], colors[j])


    # compute the validity of this set of clusters
    validity = clustering.dunn_index(input_data, out_labels, mu)
    print("Validity: %.4f" % validity)

    # plot the one sigma contours
    for i in range(0, classes):
        outplot.plot(mu[0, i], mu[1, i], 'ko')
        plot_contour(numpy.asmatrix(mu[:, i]).T, sig[:, :, i], outplot)

    outplot.set_title('Fitted Parameters')

    mpl.show()


def run_kmeans_test():
    """ Runs a comprehensive test on the kmeans algorithm. """
    n = 1000
    m = 3
    colors = ['r+', 'g+', 'b+']
    data = []
    labels = []

    fig = mpl.figure()
    genplot = fig.add_subplot(1, 2, 1)
    for i in range(0, m):
        # generate a random positive definite matrix
        a = rand(4, min_val=1)
        cov = 0
        b = rand(min_val=0, max_val=4)
        sig = numpy.matrix([[a, cov], [cov, b]])
        mu = numpy.matrix([[rand(20)], [rand(20)]])
        data.append(multi_gauss(mu, sig, n/m))
        labels.extend([ i for _ in range(0, n/m) ])

        genplot.plot(data[i][0, :], data[i][1, :], colors[i])
        plot_contour(mu, sig, genplot)

    genplot.set_title('Input Data')
    print("testing done")


def run_gda_test():
    """ Runs a comprhensive test on the GDA algoithm. """
    n = 1000
    m = 3
    colors = ["r+", "g+", "b+"]
    data = []
    labels = []

    fig = mpl.figure()
    genplot = fig.add_subplot(1, 2, 1)
    for i in range(m):
        # generate a random + def matrix
        a = rand(4, min_val=1)
        cov = rand(min_val=-1, max_val=1)
        b = rand(min_val=cov*cov/a, max_val=4)
        sig = numpy.matrix([[a, cov], [cov, b]])
        mu = numpy.matrix([[rand(20)], [rand(20)]])
        data.append(multi_gauss(mu, sig, n/m))
        labels.extend([ i for _ in range(0, n/m) ])

        genplot.plot(data[i][0, :], data[i][1, :], colors[i])
        plot_contour(mu, sig, genplot)

    genplot.set_title('Input Data')

    data = numpy.concatenate(data, axis=1)

    # redefine n to be the number of data points we now have
    n = n/m*m
    # shuffle data and labels
    for i in range(n):
        tmp = numpy.copy(data[:, i])
        tmp_l = labels[i]
        index = int(random.random() * n)
        data[:, i] = data[:, index]
        labels[i] = labels[index]
        data[:, index] = tmp
        labels[index] = tmp_l

    (classer, phi, mu, sig) = clustering.gda(data, labels, m)

    out_labels = [ classer(numpy.asarray(data)[:, i]) for i in range(n) ]

    outplot = fig.add_subplot(1, 2, 2)

    # plot the data
    # colorize misclassed points and print accuracy

    correct = [ data[:, i] for i in range(n) if labels[i] == out_labels[i] ]
    correct = numpy.concatenate(correct, axis=1)
    outplot.plot(correct[0, :], correct[1, :], 'b+')

    incorrect = [ data[:, i] for i in range(n) if labels[i] != out_labels[i] ]
    if incorrect:
        incorrect = numpy.concatenate(incorrect, axis=1)
        outplot.plot(incorrect[0, :], incorrect[1, :], 'ro')

    acc = accuracy(range(m), labels, out_labels)
    print("Accuracy: %.3f (%i / %i)" % (acc, len(correct.T), n))

    # compute the validity of this set of clusters
    validity = clustering.dunn_index(data, out_labels, mu)
    print("Validity: %.4f" % validity)

    # plot the one sigma contours
    for i in range(m):
        outplot.plot(mu[0, i], mu[1, i], 'ko')
        plot_contour(numpy.asmatrix(mu[:, i]).T, sig[:, :, i], outplot)

    outplot.set_title('Fitted Parameters')

    mpl.show()


if __name__ == '__main__':
    print("Running em test")
    run_em_test()

    print("Running k-means test")
    run_kmeans_test()
