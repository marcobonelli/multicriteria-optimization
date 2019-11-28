#coding: utf-8

import sys
import copy
import math
import random
import operator

def distance_to_schools(students, students_axes, schools_axes, schools):

	distance = {}

	for i in schools:
		for j in students:
			distance[i, j] = math.sqrt(math.pow(schools_axes[i][0] - students_axes[j][0], 2) + math.pow(schools_axes[i][1] - students_axes[j][1], 2))

	return distance

def less_than_three(students, schools, distance):

	candidates = [[] for s in students]

	for s in students:
		for j in schools:
			if distance[j, s] <= 3.0:
				candidates[s].append(j)

	return candidates

def direct_allocation(students, candidates, vacancy_per_school):

	matching = matching = [-1 for s in students]
	not_allocated_more = []
	not_allocated_less = []

	for s in students:

		if len(candidates[s]) == 1:
			school = candidates[s][0]
			if vacancy_per_school[school] > 0:
				matching[s] = school
				vacancy_per_school[school] = vacancy_per_school[school] - 1
			else:
				candidates[s] = []
				not_allocated_less.append(s)

		elif len(candidates[s]) > 1:
			not_allocated_more.append(s)

		else:
			not_allocated_less.append(s)

	return matching, not_allocated_more, not_allocated_less, vacancy_per_school

def ranking_allocation(students, ranking, vacancy_per_school, matching):

	for s in list(range(len(students))):
		for (i, j) in ranking[s]:
			if vacancy_per_school[i] > 0:
				matching[students[s]] = i
				vacancy_per_school[i] = vacancy_per_school[i] - 1
				break

	return matching, vacancy_per_school
