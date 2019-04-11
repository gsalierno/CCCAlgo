#!/usr/bin/env python3

import numpy as np
#This is a dummy matching algorithm used to compare the performance of the matching without constraint

#simply take the minimum of row for each task
def computeScoreNORM(adjM):
	print(adjM)
	print("Score NORM: ", sum(np.apply_along_axis(sumScore, axis=1, arr=adjM)))


def sumScore(row):
	print(row)
	return np.min(row)
