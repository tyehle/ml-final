#!/usr/bin/env python
import os
import sys
from numpy import *

from scipy import ndimage
from scipy import misc
import matplotlib.pyplot as plt
import numpy
import math

#Transforms and image into a histogram of oriented gradients
#image - image to be transformed (expects dtype of float32)
#num_of_orientations - number of bins to sort the orientations
#returns a list of numbers corresponding to each bin
def hog(image, num_of_orientations=36):
    dx_filter = numpy.array([[0,0,0], [1, 0, -1], [0,0,0]])
    dx = ndimage.convolve(image, dx_filter, mode='constant', cval=0.0)

    dy_filter = numpy.array([[0,1,0], [0, 0, 0], [0,-1,0]])
    dy = ndimage.convolve(image, dy_filter, mode='constant', cval=0.0)

    return arccos(dx)
#    return numpy.histogram(dx, bins=num_of_orientations)

if __name__ == '__main__':
    image = misc.imread(sys.argv[1], flatten=True).astype(numpy.uint8)
    image = (image > image.mean()).astype(numpy.uint8)
    
    plt.imshow(hog(image), cmap=plt.cm.gray)
    plt.show()


