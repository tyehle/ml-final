import numpy as np
import matplotlib.pyplot as plt

# The documentation for numpy
# http://docs.scipy.org/doc/numpy/reference

# A list of resources that have different linear algebra functions in numpy
# http://docs.scipy.org/doc/numpy/reference/routines.linalg.html

#zero matrix
zero_matrix = np.zeros( (2, 2) )

#ones array
one_array = np.ones( (2, 3) )

#np.empty will fill the array with junk data
empty_array = np.empty( (3, 3) )

#create an array by hand
hand_array = [ [1, 2, 3], [4, 5, 6] ]
hand_array = np.array(hand_array)

#range of values reshaped to an n x m matrix
range_array = np.arange(6, 12).reshape( (2, 3) )

#access an element in the matrix
print range_array[0, 0]

#transpose a matrix
transpose_matrix = np.transpose(range_array)

#Just like matlab, accessing a range of values is exactly the same way
print transpose_matrix[0, :]

#Also you can use numpy to create a matrix another way
matrix = np.mat('[1, 2; 3, 4]')
matrix.T  #Transpose

# learn more about how scipy adds on top of numpy
# http://docs.scipy.org/doc/scipy/reference/tutorial/index.html

## MatPlotLib

#basic line graph
plt.plot([1, 2, 3, 4])
plt.xlabel('X axis')
plt.ylabel('Y axis')
plt.title('Title')
plt.show()

#basic scatter plot
plt.plot([1, 2, 3, 4], [1, 4, 9, 16], 'ro')
plt.axis([0, 6, 0, 20])
plt.show()

t = np.arange(0., 5., 0.2)

#showing more than one plot
plt.plot(t, t, 'r--', t, t**2, 'bs')
plt.plot(t, t**3, 'g^')
plt.show()

# r-- is a red dash, bs is a blue square, and g^ is a green triangle


