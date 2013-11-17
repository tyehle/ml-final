#!/usr/bin/env python


from scipy import ndimage
from scipy import misc
import matplotlib.pyplot as plt
import numpy
import sys

image = misc.imread(sys.argv[1])


image = (image > image.mean()).astype(numpy.float)

plt.imshow(image)
plt.show()

hist = numpy.histogram(image)
plt.hist(hist)
plt.show()


whitespace_counts = []
for i in image:
    sum = 0
    for j in i:
        sum = sum + j
    whitespace_counts.append(sum[0])

plt.plot(whitespace_counts)
plt.plot([image.mean() * image.shape[1] for x in range(0,image.shape[0])])
plt.show()
        

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

print images

seperated_images = [image[x[0]:x[1], :] for x in images]

for i in seperated_images:
    plt.imshow(i)
    plt.show()
#plt.imshow(hist, cmap=plt.cm.gray)
#plt.show()
