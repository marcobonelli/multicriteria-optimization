#coding: utf-8

import sys
import copy
import math
import random
import operator

def getMatch(H):

	proportion = random.random()

	students = list(range(int(abs(H * proportion))))

	vacancy = (0.8 + 0.4 * random.random()) * len(students)

	schools = list(range(abs(int(float(vacancy) / 600.0)))) 

	return students, schools, vacancy

def getSchoolVacancy(schools, vacancy):

	school_vacancy = [random.random() for s in schools]

	total = sum(school_vacancy)

	school_vacancy = [int(round((school_vacancy[s] / total) * vacancy, 0)) for s in schools]

	return school_vacancy

def getPreference(students):

	proportion = random.random()

	size = int(abs(len(students) * proportion))

	preferences = random.sample(students, size)

	return preferences

def getStudentWant(schools, student):

	student_want = []

	for s in student:

		max_size = min(5, len(schools))
		size = random.sample(list(range(max_size + 1)), 1)
		size = size[0]

		temp_s = random.sample(schools, size)
		temp_w = [random.random() for i in list(range(size))]

		student_want.append((temp_s, temp_w))

	return student_want

def getParentsWant(schools, student):

	parents_want = []

	for s in student:

		max_size = min(3, len(schools))
		size = random.sample(list(range(max_size + 1)), 1)
		size = size[0]

		temp_s = random.sample(schools, size)
		temp_w = [random.random() for i in list(range(size))]

		parents_want.append((temp_s, temp_w))

	return parents_want

def getSchoolWant(schools, students):

	school_want = []

	for s in schools:

		proportion = 0.25 * random.random()
		size = int(abs(proportion * len(students)))

		temp_s = random.sample(students, size)
		temp_w = [random.random() for i in list(range(size))]

		school_want.append((temp_s, temp_w))

	return school_want

def getPositions(students, schools, density):

	factor = float(len(students)) / density

	students_axes = [(factor * round(random.random(), 4), factor * round(random.random(), 4)) for s in students]
	schools_axes = [(factor * round(random.random(), 4), factor * round(random.random(), 4)) for s in schools]

	return students_axes, schools_axes

def instantiate(seed_ = 1.0, H = 10000, density = 177.4):

	random.seed(seed_)

	students, schools, vacancy = getMatch(H)
	vacancy_per_school = getSchoolVacancy(schools, vacancy)
	preferences = getPreference(students)
	student_want = getStudentWant(schools, students)
	parents_want = getParentsWant(schools, students)
	school_want = getSchoolWant(schools, students)
	students_axes, schools_axes = getPositions(students, schools, density)

	return students, schools, vacancy_per_school, preferences, student_want, parents_want, school_want, students_axes, schools_axes
