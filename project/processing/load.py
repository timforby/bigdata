import os
import numpy as np
import image_create
from multiprocessing import Process, Queue
from scipy import sparse as sp
np.set_printoptions(suppress=True)
CPUS = 16

def make_img(sim_movies, line, util_matrix, SIZE_IMAGE):
    #matrix is of size 99x99 - 49vals then center then 49vals
    indiv_mat,rat = image_create.make_img(sim_movies,line,util_matrix,SIZE_IMAGE)
    #out_q.put((indiv_mat,rat))
    return indiv_mat,rat
def load_data(file_loc, start, end, image_size=99):
    #all data for training
    matrices = []
    #all data for ground truth
    truths = []

    user_sim_files = sorted(os.listdir(file_loc))
    
    #load matrix of movies
    movie_sim = np.load("../data/output/movie_similarity_matrix_x.npy")

    #load utility matrix
    util_matrix = sp.load_npz("../data/output/utility_matrix_x.npz")

    amount = end - start
    #batching
    step = int(amount/CPUS)
    if step == 0:
        step = 1
    #multiple process 
    out_q = Queue()
    procs = []
    for i in range(0,amount,CPUS):
        tasks = CPUS if amount-i > CPUS else amount-i
        for j in range(tasks):
            start_ = start+i+j
            end_ = start_+1
            user_sim_files_ = user_sim_files[start_:end_]
            p = Process(target=load_single, args=(file_loc, user_sim_files_,movie_sim,util_matrix,image_size,out_q))
            procs.append(p)
            p.start()
        for j in range(tasks):
            mat, rat = out_q.get()
            matrices = matrices+mat
            truths = truths+rat

        for j in range(tasks):
            p.join()

    matrices = np.asarray(matrices)
    matrices = matrices.reshape((matrices.shape[0], image_size, image_size, 1))
    truths = np.asarray(truths).flatten()
    truths = truths.reshape((truths.shape[0], 1, 1, 1))
    return matrices, truths 

def load_single(file_loc,user_sim_files,movie_sim,util_matrix, image_size, out_q):
    #all data for training
    matrices = []
    #all data for ground truth
    truths = []

    for file in user_sim_files:
        print("dsfd")

        #define matrix
        #retrieve similar users for all users --- list of 200 vals | even = user, odd = sim to user  0
        f = open(os.path.join(file_loc,file),"r")
        lines = []
        line = f.readline()
        while line !="":
            lines.append(line)
            line = f.readline()
        f.close() 
        indexes = np.random.permutation(np.asarray(range(len(lines))))
        #print("there")
        line_index = 0
        rating_index = 1
        allow_any = False
        #for line_index in indexes[:NUM_USERS]:
        while rating_index <= 5:

            line = lines[indexes[line_index]]
            line_index += 1
            line = line.replace(")","").replace("(","").split(',')
            center_user = int(line[0])
            #get movie sim
            numb_movies = np.random.permutation(range(len(util_matrix[:,center_user].nonzero()[0])))
            if line_index == len(indexes)-1:
                line_index = 0

                allow_any = True
            for i in numb_movies:
                center_movie = util_matrix[:,center_user].nonzero()[0][i]
                sim_movies = movie_sim[center_movie]
                rating = util_matrix[int(center_movie),int(center_user)]
                #sim_movies = np.asarray(list(zip(sim_movies[::2], sim_movies[1::2])))
                #fill np array with vals
                if rating_index == int(rating) or allow_any:

                    rating_index += 1
                    if out_q:
                        mat, rat = make_img(sim_movies,line,util_matrix,image_size)
                        matrices.append(mat)
                        truths.append(rat)
                    else:
                        pass
                        #todo
                    break

    out_q.put((matrices,truths))
    return
