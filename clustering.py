""" Contains methods for finding clusters in data """

# pylint: disable=C0103

import numpy
import math

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
