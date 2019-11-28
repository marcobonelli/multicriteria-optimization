#coding: utf-8

import sys
import copy
import math
import random
import operator
import statistics

import numpy as np

import Functions as do
import FlowSort as flow_sort
import InstanceGenerator as generator
import ChoquetIntegral as choquet
import LagrangianDual as lagrangian

def set_choquet_weight():

	weight = { 
			     '[0]': 0.25,
			     '[1]': 0.25,
			     '[2]': 0.25,
			     '[3]': 0.25,
			  '[0, 1]': 0.50,
			  '[0, 2]': 0.50,
			  '[0, 3]': 0.50,
			  '[1, 2]': 0.30,
			  '[1, 3]': 0.50,
			  '[2, 3]': 0.50,
		   '[0, 1, 2]': 0.55,
		   '[0, 1, 3]': 0.75,
		   '[0, 2, 3]': 0.75,
		   '[1, 2, 3]': 0.55,
		'[0, 1, 2, 3]': 1.00
	}

	return weight

def flow_sort_parameters():

	weight = {'c1': 0.40, 'c2': 0.20, 'c3': 0.20, 'c4': 0.20}

	# todos os alunos
	alternatives = ['a1', 'a2', 'a3']

	criterias = ['c1', 'c2', 'c3', 'c4']

	profiles = ['r1', 'r2', 'r3', 'r4']

	gates = ['incluir', 'candidato', 'excluir']

	references = {
		'r1': [1.0, 1.0, 1.0, 1.0], # alocacao direta
		'r2': [0.7, 0.7, 0.7, 0.7], # alocacao direta
		'r3': [0.3, 0.3, 0.3, 0.3], # candidato a alocacao
		'r4': [0.0, 0.0, 0.0, 0.0]  # remover possibilidade de alocacao
	}

	# performance dos alunos, em cada escola e para cada criterio
	performances = {
		'a1': [25.0, 25.0, 50.0, 75.0],
		'a2': [54.0, 17.0, 71.0, 45.0],
		'a3': [15.0,  5.0, 19.0,  9.0]
	}

	return weight, alternatives, criterias, profiles, gates, references, performances

if __name__ == '__main__':

	wfile = open('solution_table.txt','w')

	H = 9400
	step = 2200
	number = 4

	seed_ = 1.0000
	density = 177.4000

	for iteration in list(range(number)):

		random.seed(seed_)
		H = H + step

		students, schools, vacancy, preferences, student_want, parents_want, school_want, students_axes, schools_axes = generator.instantiate(seed_, H, density)

		utility = lagrangian.utility_merge(schools, students, parents_want, student_want, school_want)
		distance = do.distance_to_schools(students, students_axes, schools_axes, schools)

		weight = set_choquet_weight()

		ranking_ = []
		choquet_utility = {}
		ranking = [[] for s in students]

		for s in students:

			performance_matrix = choquet.get_performance_matrix(s, schools, distance, student_want, parents_want, school_want)

			ranking_.append(choquet.choquet_integral(performance_matrix, weight, schools))

			for (school, rank) in ranking_[s]:
				ranking[s].append(school)
				choquet_utility[school, s] = rank

		weight, alternatives, criterias, profiles, gates, references, performances = flow_sort_parameters()

		preference_score = []

		for s in students:

			if s in preferences:
				preference_score.append(1.0)
			else:
				preference_score.append(0.0)

		utility_ = {}

		for k in schools:

			temp = {}
			for s in students:
				temp['{}'.format(s)] = utility[k, s]

			performances = temp
			alternatives = ['{}'.format(s) for s in students]

			positions = flow_sort.run(weight, alternatives, criterias, profiles, gates, references, performances)

			for s in students:
				if positions['{}'.format(s)] == 'excluir':
					utility_[k, s] = 0.0 + preference_score[s]
				elif positions['{}'.format(s)] == 'incluir':
					utility_[k, s] = 1.0 + preference_score[s]
				else:
					utility_[k, s] = choquet_utility[k, s] + preference_score[s]

		utility = utility_

		z_dual, z_primal, matching = lagrangian.solve_lagrangian_dual(students, schools, vacancy, utility, ranking)

		match_state, match_student, match_parents, match_school = lagrangian.analyse_solution(students, schools, distance, matching, student_want, parents_want, school_want)

		wfile.write('{:02d}\#\t&\t({:.4f}, {}, {:.4f})\t&\t{}\t&\t{}\t&\t{:.4f}\t&\t{:.4f}\t&\t{:.4f}\t&\t{:.4f}\t&\t{:.4f}\t&\t{:.4f}\t&\t{:.4f}\t&\t{:.4f} \n'.format(iteration + 1, seed_, H, density, len(students), len(schools), z_dual, z_primal, float((z_dual - z_primal) / z_dual), match_state, match_student, match_parents, match_school, statistics.mean([match_state, match_student, match_parents, match_school])))

		print('{:2d}: ({:.2f}, {}, {:.2f}) executado'.format(iteration + 1, seed_, H, density))

	wfile.close()
