#!/usr/bin/env python
from scipy import ndimage
from scipy import misc
import matplotlib.pyplot as plt
import numpy
import sys

import json

def seperate_staffs(image):

    #filter out any small noise and force any gray in the image to be
    #pure black or white depending if it is above or below the mean of the image
    image = (image > image.mean()).astype(numpy.float)
    threshold = image.shape[1] - 5

    #count up the whitespace in each row
    whitespace_counts = []
    for i in image:
        whitespace_sum = 0
        for j in i:
            whitespace_sum = whitespace_sum + j
        whitespace_counts.append(whitespace_sum[0])

    plt.plot(whitespace_counts)
    plt.plot([threshold for x in range(1, image.shape[0])])
    plt.title("Horizontal Sumations for Sample Sheet Music")
    plt.xlabel("Row number")
    plt.ylabel("Horizontal Summation of Whitespace")
    plt.show()

    #split the image based on whitespace
    in_image = False
    images = []
    row_number = 0
    for row in whitespace_counts:
        if in_image:
            if row > threshold:
                in_image = False
                images[-1] = (images[-1][0], row_number)
        else:
            if row < threshold:
                in_image = True
                images.append((row_number, 0))
        row_number = row_number + 1

    seperated_images = [image[x[0]:x[1], :] for x in images]
    staff_threshold = sum([x.mean() for x in seperated_images])/len(seperated_images)
    filtered_images = [x for x in seperated_images if x.mean() < staff_threshold]
    return filtered_images


def seperate_notes(image):
    #filter out any small noise and force any gray in the image to be
    #pure black or white depending if it is above or below the mean of the image
    image = (image > image.mean()).astype(numpy.float)
    #count up the whitespace in each row
    whitespace_counts = []
    for i in image:
        whitespace_sum = 0
        for j in i:
            whitespace_sum = whitespace_sum + j
        whitespace_counts.append(whitespace_sum[0])


    threshold = numpy.median(whitespace_counts) - 1

    plt.plot(whitespace_counts)
    plt.plot([threshold for x in range(1, image.shape[0])])
    plt.show()

    #split the image based on whitespace
    in_image = False
    images = []
    row_number = 0
    for row in whitespace_counts:
        if in_image:
            if row > threshold:
                in_image = False
                images[-1] = (images[-1][0], row_number)
        else:
            if row <= threshold:
                in_image = True
                images.append((row_number, 0))
        row_number = row_number + 1

    seperated_images = [image[x[0]:x[1], :] for x in images]
    return seperated_images

if __name__ == "__main__":
    print "do not run this file yet"
