import sys
sys.path.insert(0, '../tools/')
import numpy as np
import progbar
from multiprocessing import Process, Queue
from sklearn.metrics.pairwise import pairwise_kernels as pwd
from scipy import sparse as sp

CPUS = 16
STEP = CPUS*64
VALS = 100
np.set_printoptions(suppress=True)

def sort_x(X,out_q):
    info_data = []
    for x in X:
        #make sure x has values
        if x.any():
            sort_x = [(a[0][0],a[1]) for a in sorted(np.ndenumerate(x), key=lambda x:x[1], reverse=True)][:VALS]
            #print(sort_x)
            info_data.append(np.asarray(sort_x).flatten(order='C'))
    out_q.put(np.asarray(info_data))


#load row_mean_utility_matrix
X = sp.load_npz("../data/output/row_mean_utility_matrix_x.npz")
movies = np.zeros((1,1))
mov = False

#step 
for i in range(0,X.shape[0],STEP):
    i_end = i+STEP
    if i_end >= X.shape[0]:
        i_end = X.shape[0]
    progbar.printb(i, X.shape[0])
    #calculate cosine similarity for all other than batch
    calc_data = pwd(X=X[i:i_end], Y=X, metric="cosine", n_jobs=CPUS)
    #multiprocessing params
    out_q = Queue()
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
        p = Process(target=sort_x, args=(calc_data[start:end],out_q))
        p.start()
        procs.append(p)

    for j in procs:
        data = out_q.get()
        if not mov:
            mov = True
            movies = data
        else:
            movies.hstack(data)

    for j in procs:
        j.join()

#print(movies)
np.save("../data/output/movie_similarity_matrix_x", movies)




