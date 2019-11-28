#coding: utf-8

import sys
import copy
import math
import random
import operator
import statistics

import numpy as np

def easy_knapsack(utility, school, students, capacity, u):

	cost = 0.0
	candidates = []

	for s in students:
		candidates.append((s, utility[school, s] - u[s]))

	candidates.sort(key = operator.itemgetter(1), reverse = True)
	candidates = candidates[:capacity]

	for (s, w) in candidates:
		cost = cost + w

	return candidates, cost

def get_allocation(schools, students, candidates):

	allocation = [[] for s in students]

	for s in schools:
		for (i, w) in candidates[s]:
			allocation[i].append(s)

	return allocation

def solve_subgradient(students, allocation):

	lambda_ = [1.0 - len(allocation[s]) for s in students]

	return lambda_

def solve_stepsize(best_primal, z_dual, lambda_):

	stepsize = (best_primal - z_dual) / math.pow(np.linalg.norm(lambda_), 2)

	return stepsize

def multipliers_update(students, u, stepsize, lambda_):

	for s in students:
		if u[s] + stepsize * lambda_[s] < 0.0:
			u[s] = 0.0
		elif u[s] + stepsize * lambda_[s] < 1.0:
			u[s] = u[s] + stepsize * lambda_[s]
		else:
			u[s] = 1.0

	return u

def solve_primal(lambda_, students, schools, allocation, utility, ranking, u):

	increase = []
	matching = [-1.0 for s in students]
	cost = 0.0

	gap = [0 for s in schools]

	for s in students:

		if lambda_[s] > 0.0:
			increase.append(s)

		elif lambda_[s] == 0.0:
			matching[s] = allocation[s][0]

		elif lambda_[s] < 0.0:
			max_w = -1.0
			max_i = -1.0

			for i in allocation[s]:
				gap[i] = gap[i] + 1.0
				if max_w < utility[i, s]:
					max_w = utility[i, s]
					max_i = i

			matching[s] = i
			gap[i] = gap[i] - 1.0

	increase = random.sample(increase, len(increase))
	for s in increase:
		for i in ranking[s]:
			if gap[i] > 0.0:
				matching[s] = i
				gap[i] = gap[i] - 1.0
				break

	for s in students:
		if matching[s] > -1:
			cost = cost + utility[matching[s], s]

	return matching, cost

def solve_lagrangian_dual(students, schools, vacancy, utility, ranking):

	best_dual = 1000000.0
	best_primal = -1000000.0
	primal_solution = []
	dual_solution = []

	primal_ = []
	dual_ = []

#	results = []

	u = [0.0 for s in students]

	for k in list(range(100)):

		candidates = []
		z_dual = sum(u)

		for s in schools:
			partial_c, partial_cost = easy_knapsack(utility, s, students, vacancy[s], u)
			candidates.append(partial_c)
			z_dual = z_dual + partial_cost

		allocation = get_allocation(schools, students, candidates)

		lambda_ = solve_subgradient(students, allocation)

		matching, z_primal = solve_primal(lambda_, students, schools, allocation, utility, ranking, u)

		primal_.append(z_primal)
		dual_.append(z_dual)

		if z_dual < best_dual:
			best_dual = z_dual
			dual_solution = candidates

		if z_primal > best_primal:
			best_primal = z_primal
			primal_solution = matching

		if best_primal * 1.001 >= best_dual:
			print('solução otima encontrada na iteracao: {}'.format(k))
			break

		stepsize = solve_stepsize(z_primal, z_dual, lambda_)
		u = multipliers_update(students, u, stepsize, lambda_)

#		match_state, match_student, match_parents, match_school = analyse_solution(students, schools, distance, primal_solution, student_want, parents_want, school_want)
#		results.append(statistics.mean([match_state, match_student, match_parents, match_school]))

#	print('{:.4f}'.format(max(results)))

	return best_dual, best_primal, primal_solution

def utility_merge(schools, students, parents_want, student_want, school_want):

	utility = {}

	for i in schools:
		for j in students:
			utility[(i, j)] = [0.0, 0.0, 0.0, 0.0]

	for s in students:
		for i in list(range(len(parents_want[s][0]))):
			school = parents_want[s][0][i]
			desejo = parents_want[s][1][i]
			utility[(school, s)][2] = desejo

	for s in students:
		for i in list(range(len(student_want[s][0]))):
			school = student_want[s][0][i]
			desejo = student_want[s][1][i]
			utility[(school, s)][3] = desejo

	for s in schools:
		for j in list(range(len(school_want[s][0]))):
			student = school_want[s][0][j]
			desejo = school_want[s][1][j]
			utility[(s, student)][1] = desejo

	for i in schools:
		for j in students:
			utility[(i, j)][0] = random.random()

	return utility

def analyse_solution(students, schools, distance, matching, student_want, parents_want, school_want):

	ideal_possibilities = [[] for s in students]
	ideal_matching = [0.0 for s in students]
	max_ideal_matching = 0.0
	ideal_student = [0.0 for s in students]
	ideal_parents = [0.0 for s in students]
	ideal_school = [0.0 for s in students]
	student_match = 0.0
	parents_match = 0.0
	school_match = 0.0

	for j in students:

		for i in schools:
			if distance[(i, j)] <= 3.0:
				ideal_possibilities[j].append(i)

		if len(student_want[j][1]) > 0.0:
			ideal_student[j] = statistics.mean(student_want[j][1])

		if len(parents_want[j][1]) > 0.0:
			ideal_parents[j] = statistics.mean(parents_want[j][1])

		temp = 0
		for i in schools:
			if j in school_want[i][0]:
				for k in list(range(len(school_want[i][0]))):
					if j == school_want[i][0][k]:
						ideal_school[j] = ideal_school[j] + school_want[i][1][k]
						temp = temp + 1
		if temp > 0:
			ideal_school[j] = ideal_school[j] / temp
	
		if len(ideal_possibilities[j]) > 0.0:
			max_ideal_matching = max_ideal_matching + 1.0
			if matching[j] in ideal_possibilities[j]:
				ideal_matching[j] = 1.0

		if matching[j] in student_want[j][0]:
			for k in list(range(len(student_want[j][0]))):
				if matching[j] == student_want[j][0][k]:
					student_match = student_match + student_want[j][1][k]

		if matching[j] in parents_want[j][0]:
			for k in list(range(len(parents_want[j][0]))):
				if matching[j] == parents_want[j][0][k]:
					parents_match = parents_match + parents_want[j][1][k]

		if j in school_want[matching[j]][0]:
			for k in list(range(len(school_want[matching[j]][0]))):
				if j == school_want[matching[j]][0][k]:
					school_match = school_match + school_want[matching[j]][1][k]

	match_state = float(sum(ideal_matching) / max_ideal_matching)
	match_student = float(student_match / sum(ideal_student))
	match_parents = float(parents_match / sum(ideal_parents))
	match_school = float(school_match / sum(ideal_school))

	return match_state, match_student, match_parents, match_school
