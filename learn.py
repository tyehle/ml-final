#!/usr/bin/env python
import os
import sys

import json

from scipy import ndimage
from scipy import misc
import matplotlib.pyplot as plt
import numpy

from seperate_staffs import *

def learn(filename):
    image = misc.imread(filename)
    plt.imshow(image)
    plt.show()

    image_counter = 0
    staffs = seperate_staffs(image)
    results = json.loads(open("learn/learn.json").read())
    image_counter = len(results) + 1
    
    for staff in staffs:
        transposed_staff = ndimage.rotate(staff, -90)
        notes = seperate_notes(transposed_staff)
        for i in range(len(notes)):
            filename = 'learn/{0}.jpg'.format(str(image_counter).zfill(5))
            misc.imsave(filename, notes[i])
            image_counter = image_counter + 1

            plt.imshow(ndimage.rotate(notes[i], 90))
            plt.ion()
            plt.show()
            
            thing = {}
            
            note_type = raw_input("Type?: ")
            while not note_type in ["note", "treble", "ignore", "bass", "time", "bar", "rest"]:
                note_type = raw_input("Retry Type?: ")
            thing["type"] = note_type

            if note_type == "note":
                note_pitch = raw_input("Pitch?: ")
                thing["pitch"] = int(note_pitch)
                note_length = raw_input("Length?: ")
                thing["length"] = float(note_length)
            if note_type == "rest":
                note_length = raw_input("Length?: ")
                thing["length"] = float(note_length)
            print({filename:thing})
            results.append({filename:thing})
            
            
    json_result = json.dumps(results)
    print json_result

    print "Number of results in learned database: {0}".format(len(results))
    open("learn/learn.json", 'w').write(json_result)


if __name__ == "__main__":
    filename = sys.argv[1]
    
    learn(filename)
