import sys
sys.path.insert(0, '../tools/')
import os
import numpy as np
import math
import progbar
import signal
from sklearn.metrics.pairwise import cosine_similarity as csim
from scipy import sparse as sp

file_loc = "../data/input/training_set_x"
files =  sorted(os.listdir(file_loc))

#columns need to be known, mentioned in Netflix README
#cols = 2649429
cols = 12

mat_data = sp.csr_matrix((1,cols))

#for all movie files
for file in files:
	f = open(os.path.join(file_loc,file),"r")

	#get movie
	movie = f.readline().split(':')[0]
	next = f.readline()
	row_data = np.zeros((1,cols))

	#pring progress bar
	progbar.printb(int(movie), len(files))

	#get user and ratings
	while next !="":
		user,rating = next.split(',')
		row_data[0][int(user)-1] = float(rating)

		next = f.readline()

	#append/vstack to sparse matrix
	if int(movie) == 1:
		mat_data = sp.csr_matrix(row_data)
	else:
		mat_data = sp.vstack([mat_data, sp.csr_matrix(row_data)])


#print(mat_data.todense())
sp.save_npz("../data/output/utility_matrix_x",mat_data)
