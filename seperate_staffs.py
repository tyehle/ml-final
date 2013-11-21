#!/usr/bin/env python
from scipy import ndimage
from scipy import misc
import matplotlib.pyplot as plt
import numpy
import sys

def seperate_staffs(image):

    #filter out any small noise and force any gray in the image to be
    #pure black or white depending if it is above or below the mean of the image
    image = (image > image.mean()).astype(numpy.float)

    #count up the whitespace in each row
    whitespace_counts = []
    for i in image:
        sum = 0
        for j in i:
            sum = sum + j
        whitespace_counts.append(sum[0])
            
    #split the image based on whitespace
    in_image = False
    images = []
    threshold = image.shape[1] - 5;
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
    filtered_images = filter(lambda x: x.mean()<.85, seperated_images)
    return filtered_images

if __name__ == "__main__":
    image = misc.imread(sys.argv[1])
    plt.imshow(image)
    plt.show()

    staffs = seperate_staffs(image)
    for i in staffs:
        plt.imshow(i)
        plt.show()

