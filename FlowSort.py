#coding: utf-8

import sys
import math
import copy
import random
import operator
import xlsxwriter

import numpy as np

def preference_procedure_Usual(profiles, references, alternatives, performances, criterias):

	P = {}

	for c in list(range(len(criterias))):

		for alternative in alternatives:

			R = [alternative] + profiles
			P[alternative, criterias[c]] = [[0.0 for j in R] for i in R]
			criteria_performance = [performances[alternative][c]]
			
			for i in profiles:
				criteria_performance.append(references[i][c])
			
			for i in list(range(len(R))):
				for j in list(range(len(R))):
					if criteria_performance[i] > criteria_performance[j] and i != j:
						P[alternative, criterias[c]][i][j] = 1.0

	return P

def preference_degree(P, weight, criterias, alternatives, profiles):

	pi = {}
	pi_profile = {}

	for alternative in alternatives:
		for p in list(range(len(profiles))):
			pi[alternative, profiles[p]] = np.sum(weight[criteria] * P[alternative, criteria][0][p + 1] for criteria in criterias)
			pi[profiles[p], alternative] = np.sum(weight[criteria] * P[alternative, criteria][p + 1][0] for criteria in criterias)

			for k in list(range(len(profiles))):
				if k != p:
					pi_profile[alternative, profiles[p], profiles[k]] = np.sum(weight[criteria] * P[alternative, criteria][p + 1][k + 1] for criteria in criterias)
				else:
					pi_profile[alternative, profiles[p], profiles[k]] = 0.0

	return pi, pi_profile

def net_value(pi, pi_profile, profiles, alternatives):

	fi_plus = {}
	fi_minus = {}
	fi = {}

	fi_profile_plus = {}
	fi_profile_minus = {}
	fi_profile = {}

	for alternative in alternatives:

		R = [alternative] + profiles
		
		fi_plus[alternative] = np.sum(pi[alternative, r] for r in R if r != alternative) / (len(R) - 1)
		fi_minus[alternative] = np.sum(pi[r, alternative] for r in R if r != alternative) / (len(R) - 1)
		fi[alternative] = round(fi_plus[alternative] - fi_minus[alternative], 4)

		for p in list(range(len(profiles))):
			fi_profile_plus[alternative, profiles[p]] = (pi[profiles[p], alternative] + np.sum(pi_profile[alternative, profiles[p], r] for r in R if r != profiles[p] and r != alternative)) / (len(R) - 1)
			fi_profile_minus[alternative, profiles[p]] = (pi[alternative, profiles[p]] + np.sum(pi_profile[alternative, r, profiles[p]] for r in R if r != profiles[p] and r != alternative)) / (len(R) - 1)
			fi_profile[alternative, profiles[p]] = round(fi_profile_plus[alternative, profiles[p]] - fi_profile_minus[alternative, profiles[p]], 4)

	return fi, fi_profile

def classification_procedure(fi, fi_profile, profiles, alternatives, gates):

	vector = {}
	positions = {}

	for alternative in alternatives:
		vector[alternative] = []

		for profile in profiles:
			vector[alternative].append([profile, fi_profile[alternative, profile]])

		vector[alternative].append([alternative, fi[alternative]])

		vector[alternative].sort(key = operator.itemgetter(1), reverse = True)

		for v in list(range(len(vector[alternative]))):
			[a, f] = vector[alternative][v]
			if a == alternative:
				positions[alternative] = gates[v - 1]

	return positions

def run(weight, alternatives, criterias, profiles, gates, references, performances):

	P = preference_procedure_Usual(profiles, references, alternatives, performances, criterias)

	pi, pi_profile = preference_degree(P, weight, criterias, alternatives, profiles)

	fi, fi_profile = net_value(pi, pi_profile, profiles, alternatives)

	classification_procedure(fi, fi_profile, profiles, alternatives, gates)

	positions = classification_procedure(fi, fi_profile, profiles, alternatives, gates)

	return positions
