import numpy as np
from scipy import sparse as sp

#change to FALSE for users (columns)
ROW = True
ROW = False

#load util_matrix
mat_data = sp.load_npz("../data/output/utility_matrix_x.npz")

if not ROW:
	mat_data = mat_data.transpose()

#retrieve tuple row ind, col ind, values
(x,y,z)=sp.find(mat_data)

#count number of times each row index appears
sums = np.bincount(x)
#sum of values where there exists a value for each row index
totals = np.bincount(x,weights=z)

#get all nonzero elements in sum (where row index appears more than 0)
nonzeros = [i for i,x in enumerate(sums) if x != 0]
#create a placeholder row
mean_row = np.zeros(mat_data.shape[0])
#get 1D vector with mean of each row in each row
mean_row[nonzeros]=totals[nonzeros]/sums[nonzeros]
#create a 2D matrix with the means in the diagonals
mean_diag = sp.diags(mean_row, 0)
#create another 2D matrix with 1s wherever there is an element in utility matrix
coeff = mat_data.copy();
coeff.data = np.ones_like(coeff.data)
#subtract from original matrix -> the product of the diagonal and element(1) matrix
mat_data -= (mean_diag * coeff)

#print(mat_data.todense())

if ROW:
	sp.save_npz("../data/output/row_mean_utility_matrix_x",mat_data)
else:
	sp.save_npz("../data/output/col_mean_utility_matrix_x",mat_data)
