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
    return numpy.array([loc / len(row_brightness)**2])


def get_type_classifier_subset(train_ratio, file_location, get_features):
    print("-- Training Type Classifier --")
    file_data = open(file_location, 'r')
    image_files = json.load(file_data)

    notes = []
    # filter out anything that isn't a note
    for image in image_files:
        file_name = image.keys()[0]
        data = image[file_name]
        if data["type"] not in ["ignore", "time", "bar"]:
            notes.append(image)

    # separate out images to test on
    test_images = []
    for _ in range(int((1.0 - train_ratio) * len(notes))):
        index = int(random.random() * len(notes))
        test_images.append(notes.pop(index))

    print("training on %i images" % len(notes))
    print("testing on %i images" % len(test_images))

    (classer, label_map) = get_type_classifier(notes, get_features, verbose=True)

    num_correct = 0
    for image in test_images:
        file_name = image.keys()[0]
        data = image[file_name]
        if data["type"] == "note":
            expected_label = "note,{0}".format(data["length"])
        elif data["type"] == "rest":
            expected_label = "rest,{0}".format(data["length"])
        else:
            expected_label = data["type"]
        features = get_features(misc.imread(file_name))
        actual_label = label_map[classer(features)]
        if actual_label == expected_label:
            num_correct = num_correct + 1
        else:
            print("Features")
            print(features)
            print("Expected %s, got %s" % (expected_label, actual_label))

    print("Accuracy %f (%i / %i)" % ((float(num_correct) / len(test_images)), num_correct, len(test_images)))


def get_type_classifier(image_files, get_features, verbose=False):
    """ Gets a classifier that can be used to find the type of a note. """
    label_map = []
    labels = []
    file_names = []

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
        file_names.append(file_name)

    classer = train_classifier(file_names, labels, len(label_map), get_features, verbose)
    if verbose:
        print("Label map:")
        print(label_map)
    return classer, label_map


def get_pitch_classifier_subset(train_ratio, file_location, get_features):
    print("-- Training Pitch Classifier --")
    file_data = open(file_location, 'r')
    image_files = json.load(file_data)

    notes = []
    # filter out anything that isn't a note
    for image in image_files:
        file_name = image.keys()[0]
        data = image[file_name]
        if data["type"] == "note":
            notes.append(image)

    # separate out images to test on
    test_images = []
    for i in range(int((1.0 - train_ratio) * len(notes))):
        index = int(random.random() * len(notes))
        test_images.append(notes.pop(index))

    print("training on %i images" % len(notes))
    print("testing on %i images" % len(test_images))

    (classer, label_map) = get_pitch_classifier(notes, get_features, verbose=True)

    num_correct = 0
    for image in test_images:
        file_name = image.keys()[0]
        data = image[file_name]
        expected_label = data["pitch"]
        features = get_features(misc.imread(file_name))
        actual_label = label_map[classer(features)]
        if actual_label == expected_label:
            num_correct = num_correct + 1
        else:
            print("Features")
            print(features)
            print("Expected %s, got %s" % (expected_label, actual_label))

    print("Accuracy %f (%i / %i)" % ((float(num_correct) / len(test_images)), num_correct, len(test_images)))


def get_pitch_classifier(image_files, get_features, verbose=False):
    """ Gets a classifier that can be used to find the pitch of a note. """
    label_map = []
    labels = []
    file_names = []

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
        file_names.append(file_name)

    classer = train_classifier(file_names, labels, len(label_map), get_features, verbose)
    if verbose:
        print("Label map:")
        print(label_map)
    return classer, label_map


def train_classifier(image_files, labels, m, get_features, verbose=False):
    """ Trains a classifier using the given images files and labels.
        Uses the given function to extract a feature vector from the image file.
    """
    features = []
    for file_name in image_files:
        image = misc.imread(file_name)
        features.append(get_features(image))

    # stack the data correctly
    features = numpy.vstack(features).T

    # get the classifier
    (classer, phi, mu, sig) = clustering.gda(features, labels, m)
    if verbose:
        print("Data:")
        print(features)
        print("phi:")
        print(phi)
        print("mu:")
        print(mu)
        print("sigma:")
        print(sig)
    return classer


if __name__ == "__main__":
    train_ratio = .9
    get_type_classifier_subset(train_ratio, "learn/learn.json", lambda img: numpy.array([img.mean()]))
    get_pitch_classifier_subset(train_ratio, "learn/learn.json", center)
