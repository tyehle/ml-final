""" Main script to digitize sheet music """

import clustering
import json
import numpy, scipy
from scipy import misc
import random


def get_classifier(file_location, get_features):
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
        elif data["type"] == "ignore":
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

    # get the classifier
    (classer, phi, mu, sig) = clustering.gda(features, labels, len(label_map))
    return classer


if __name__ == "__main__":
    get_classifier("learn/learn.json", lambda img: random.random())
