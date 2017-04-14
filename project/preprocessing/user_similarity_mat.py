import sys
sys.path.insert(0, '../tools/')
import numpy as np
import progbar
from multiprocessing import Process
from sklearn.metrics.pairwise import pairwise_kernels as pwd
from scipy import sparse as sp

CPUS = 16
STEP = CPUS*64
VALS = 100

def sort_x(X,i,j,ind):
    info_data = []
    for x in X:
        if x.any():
            sort_x = [(a[0][0],a[1]) for a in sorted(np.ndenumerate(x), key=lambda x:x[1], reverse=True)][:VALS]
            info_data.append(sort_x)
    w = open("../data/output/user_sim_files_x/"+str(i+ind)+"-"+str(j+ind),"w")
    for x in info_data:
        w.write(str(x).strip('[]')+"\n")

#load row_mean_utility_matrix
X = sp.load_npz("../data/output/col_mean_utility_matrix_x.npz")

#step 
for i in range(0,X.shape[0],STEP):
    i_end = i+STEP
    if i_end >= X.shape[0]:
        i_end = X.shape[0]
    progbar.printb(i, X.shape[0])
    #calculate cosine similarity for all other than batch
    calc_data = pwd(X=X[i:i_end], Y=X, metric="cosine", n_jobs=CPUS)
    #multiprocessing params
    procs = []

    #for all cpus
    for j in range(CPUS):
        start = int(j*(STEP/CPUS))
        if start >= calc_data.shape[0]:
            break
        end = int((j+1)*(STEP/CPUS))
        if end >= calc_data.shape[0]:
            end = calc_data.shape[0]

        #run the sorting section
        p = Process(target=sort_x, args=(calc_data[start:end],start,end,i))
        p.start()
        procs.append(p)

    for j in procs:
        j.join()
