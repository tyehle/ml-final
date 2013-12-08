import clustering
import json
import numpy, scipy
from scipy import misc


def get_classifier(file_location):
    file_data = open(file_location, 'r')
    image_files = json.load(file_data)

    label_map = []
    labels = []

    # Iterating through each image that the algorithm
    # can train on.
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
            label = data["length"]

        if label not in label_map:
            label_map.append(label)
            index = len(label_map) - 1
        else:
            index = label_map.index(label)
		labels.append(index)
        for row in file_name:
            #misc.iamread(file_name)

if __name__ == "__main__":
	get_classifier("test_json.txt")
