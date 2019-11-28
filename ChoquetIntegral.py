#coding: utf-8

import sys
import copy
import math
import random
import operator

def get_performance_matrix(student, schools, distance, student_want, parents_want, school_want):

	distance_column = [distance[s, student] for s in schools]
	student_column = [0.0 for s in schools]
	school_column = [0.0 for s in schools]
	parents_column = [0.0 for s in schools]

	performance_matrix = [[0.0 for j in list(range(4))] for i in schools]

	max_distance = max(distance_column)
	min_distance = min(distance_column)
	for s in schools:
#		distance_column[s] = float((max_distance - distance_column[s]) / (max_distance - min_distance))
		if distance[s, student] <= 3.0:
			distance_column[s] = 1.0
		else:
			distance_column[s] = 0.0

		(i_set, w_set) = student_want[student]
		if s in i_set:
			for i in list(range(len(i_set))):
				if i_set[i] == s:
					student_column[s] = w_set[i]
					break

		(i_set, w_set) = parents_want[student]
		if s in i_set:
			for i in list(range(len(i_set))):
				if i_set[i] == s:
					parents_column[s] = w_set[i]
					break

		(i_set, w_set) = school_want[s]
		if student in i_set:
			for i in list(range(len(i_set))):
				if i_set[i] == student:
					school_column[s] = w_set[i]
					break

	for s in schools:
		performance_matrix[s] = [distance_column[s], student_column[s], parents_column[s], school_column[s]]

	return performance_matrix

def choquet_integral(performance_matrix, weight, schools):

	ranking = []

	for s in schools:

		rank = 0.0
		
		while True:

			columns = []
			min_ = 1000.0

			for j in list(range(len(performance_matrix[s]))):
				if performance_matrix[s][j] > 0.0:
					columns.append(j)
					if performance_matrix[s][j] < min_:
						min_ = performance_matrix[s][j]

			if len(columns) > 0:

				for j in columns:
					performance_matrix[s][j] = performance_matrix[s][j] - min_

				rank = rank + min_ * weight['{}'.format(columns)]

			if sum(performance_matrix[s]) <= 0.0:
				ranking.append((s, rank))
				break

	ranking.sort(key = operator.itemgetter(1), reverse = True)

	return ranking
