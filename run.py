#!/usr/bin/python2.7

""" Main script to digitize sheet music """

import clustering
import json
import numpy, scipy
from scipy import ndimage
from scipy import misc
import random

def mark_of_the_beast(image):
    """ Returns the row sums of brightness of the image. """
    features = numpy.array(0)

    image = ndimage.rotate(image, 90)

    for row in (image < image.mean()).astype(numpy.float):
        tmpSum = 0
        for pixel in row:
            tmpSum = tmpSum + pixel
        features = numpy.append(features, tmpSum)

    return features


def center(image):
    """ Finds the centeroid (geometric mean) """
    row_brightness = mark_of_the_beast(image)
    loc = 0
    for i in range(len(row_brightness)):
        loc = loc + i * row_brightness[i]
    return loc / len(row_brightness)**2


def get_type_classifier(file_location, get_features):
    """ Gets a classifier that can be used to find the type of a note. """
    file_data = open(file_location, 'r')
    image_files = json.load(file_data)

    label_map = []
    labels = []
    features = []

    # Iterating through each image that the algorithm can train on.
    for image in image_files:
        file_name = image.keys()[0]
        data = image[file_name]
        if data["type"] == "note":
            label = "note,{0}".format(data["length"])
        elif data["type"] == "rest":
            label = "rest,{0}".format(data["length"])
        elif data["type"] in ["ignore", "time", "bar"]:
            continue
        else:
            label = data["type"]

        # Add the label to the list if it is not already there,
        # and record the index of the label in the list of valid labels
        if label not in label_map:
            label_map.append(label)
            index = len(label_map) - 1
        else:
            index = label_map.index(label)

        # add the label for this image to the list of labels
        labels.append(index)

        # add the feature vector for this image to the list of data
        image = misc.imread(file_name)
        features.append(get_features(image))

    # stack the data correctly
    features = numpy.vstack(features).T

    print(features)

    # get the classifier
    (classer, phi, mu, sig) = clustering.gda(features, labels, len(label_map))
    print("label map")
    print(label_map)
    print("phi")
    print(phi)
    print("mu")
    print(mu)
    return classer, label_map


def get_pitch_classifier(file_location, get_features):
    """ Gets a classifier that can be used to find the pitch of a note. """
    file_data = open(file_location, 'r')
    image_files = json.load(file_data)

    label_map = []
    labels = []
    features = []

    # Iterating through each image that the algorithm can train on.
    for image in image_files:
        file_name = image.keys()[0]
        data = image[file_name]
        if data["type"] == "note":
            label = data["pitch"]
        else:
            continue

        # Add the label to the list if it is not already there,
        # and record the index of the label in the list of valid labels
        if label not in label_map:
            label_map.append(label)
            index = len(label_map) - 1
        else:
            index = label_map.index(label)

        # add the label for this image to the list of labels
        labels.append(index)

        # add the feature vector for this image to the list of data
        image = misc.imread(file_name)
        features.append(get_features(image))

    # stack the data correctly
    features = numpy.vstack(features).T

    print(features)

    # get the classifier
    (classer, phi, mu, sig) = clustering.gda(features, labels, len(label_map))
    print("label map")
    print(label_map)
    print("phi")
    print(phi)
    print("mu")
    print(mu)
    return classer, label_map


if __name__ == "__main__":
    # get_type_classifier("learn/learn.json", lambda img: img.mean())
    get_pitch_classifier("learn/learn.json", center)
