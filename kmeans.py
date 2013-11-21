import numpy
import random as rand
import math

#
# This method will take in an array and return the mean value.
#
def mean(arr):
        sum = 0.
        length = len(arr)

        for i in arr:
                sum += i[0]

        return sum/length

#
# This method will take in an array and return the index of the minimum value.
#
def min_index(arr):
        index = 0

        for i in range(1, len(arr)):
                result = arr[i, 0] < arr[index, 0]
                if result[0] and result[1]:
                        index = i

        return index

#
# This method takes in a set of data and the number of clusters that 
# the algoirthm wants to find (m). This will then return the data with
# a cluster label.
#
def kmeans(data, m):
	
        cur_means = numpy.zeros( (m, 2) )

        length = len(data)
        labels = numpy.zeros( (length, 1) )

        #randomize means
        for i in range(0,m):

                index = math.floor(length * rand.random());

                cur_means[i, 0] = data[index, 0];
                cur_means[i, 1] = data[index, 1];
        
        converged = False

        while not converged:
                #This will go through each point and find the closest mean and label it.
                for i in range(0,length):
                        # Go through each cluster
                        distance = numpy.zeros( (m, 1) );
                        for j in range(0, m):
                                distance[j, 0] = math.sqrt((data[i, 0] - cur_means[i, 0])**2 - (data[i, 1] - cur_means[j, 1]**2));
                        index = min_index(distance)
                        labels[i] = index

                prev_means = cur_means

                #This will re-evaluate each mean
                for j in range(0, m):
                        label_array = numpy.zeros(0, 1)
                        for i in range(0, length):
                                if labels[i] == j:
                                        label_array = numpy.vstack( (label_array, data[i, :]) )
                        tmp = mean(label_array)
                        cur_means[j, 0] = tmp[0, 0]
                        cur_means[j, 1] = tmp[0, 1]

                result = cur_means == prev_means
                converged = result[0] and result[1]
        
        final_data = numpy.zeros( (length, 3) )

        for i in range(0, length):
                final_data[i, 0] = data[i, 0]
                final_data[i, 1] = data[i, 1]
                final_data[i, 2] = labels[i]

        return (means, final_data)
