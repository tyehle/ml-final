import numpy
import random as rand
import math

#
# This method will take in an array and return the mean point of any n dimensional matrix.
#
def mean(arr):
	sums = numpy.zeros( (1, len(arr[0])) );
	length = len(arr)
	
	for row in range(0, length):
		for col in range(0, len(sums[0])):
			sums[0, col] += arr[row, col]

	for i in range(0, len(sums[0])):
		sums[0, i] /= length

	return sums

#
# This method will take in an array and return the index of the minimum value.
#
def min_index(arr):
	index = 0

	for i in range(1, len(arr)):
		if arr[i, 0] < arr[index, 0]:
			index = i

	return index

#
# This method takes in a set of data and the number of clusters that 
# the algoirthm wants to find (m). This will then return the data with
# a cluster label.
#
def kmeans(data, m):
	# If the data structure that is recieved is numpy.matrix,
	# this will convert it to numpy.array.
	if(type(data) == numpy.matrix):
		data = numpy.asarray(data)

	# How many data points there are
	length = len(data)
	# The dimension of the data point
	dim = len(data[0]);
	# The label that is assigned to.
	labels = numpy.zeros( (length, 1) )

	cur_means = numpy.zeros( (m, dim) );

	#randomize means by choosing 3 points from the data at random.
	for i in range(0,m):
		index = math.floor(length * rand.random());
		cur_means[i, :] = data[index, :];
        
	converged = False

	while not converged:
		# Relabel each data point by its closest mean.
		labels = relabel_data(data, m, cur_means)

		prev_means = numpy.copy(cur_means)

		# Re-evaluate each mean by taking the mean of the cluster.
		cur_means = reevaluate_means(data, m, labels)
		
		# This will check for convergence by seeing if the difference
		# between the previous means and the current means have changed.
		result = cur_means == prev_means
		converged = result.all();

	# Combine the labels and the data together and return 
	# it with each cluster mean.
	final_data = numpy.zeros( (length, dim + 1) )

	final_data[:, 0:dim] = data[:, :]
	final_data[:, dim] = labels[:, 0]
 
	return (cur_means, final_data)

#
# Go through each data point and relabel it based on its
# closest mean.
#
def relabel_data(data, m, cur_means):
	labels = numpy.zeros( (len(data), 1) )
	for i in range(0,len(data)):
		# Go through each cluster
		distance = numpy.zeros( (m, 1) );
		for j in range(0, m):
			for k in range(0, len(data[0])):
				distance[j, 0] += (data[i, k] - cur_means[j, k])**2
			distance[j, 0] = math.sqrt(distance[j, 0]);
		index = min_index(distance)
		labels[i] = index

	return labels

#
# This will recompute each mean based on the mean of the new cluster 
# of data.
#
def reevaluate_means(data, m, labels):
	means = numpy.zeros( (m, len(data[0])) )
	for j in range(0, m):
		label_array = numpy.zeros( (0, len(data[0])) )
		for i in range(0, len(data)):
			if labels[i] == j:
				label_array = numpy.vstack( (label_array, data[i, :]) )
		means[j, :] = mean(label_array)[0, :]
	return means
