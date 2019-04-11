#!/usr/bin/env python3

import numpy as np
#This is a dummy matching algorithm used to compare the performance of the matching without constraint

#simply take the minimum of row for each task
def computeScoreNORM(adjM):
	scoreNorm = 0

	for i in range(adjM.shape[0]):
		scoreNorm+=adjM[i,np.argmin(adjM[i])]

	print("Score without constraint",scoreNorm)

