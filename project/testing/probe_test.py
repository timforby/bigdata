import sys
sys.path.insert(0, '../processing/')
sys.path.insert(0, '../tools/')
import os
import numpy as np
import image_create
import progbar
from multiprocessing import Process, Queue
from scipy import sparse as sp


np.set_printoptions(suppress=True)
def make_img(sim_movies, line, util_matrix, SIZE_IMAGE, out_q):
    CENTER = int(SIZE_IMAGE/2)
    #matrix is of size 99x99 - 49vals then center then 49vals
    indiv_mat,rat = image_create.make_vect(sim_movies,line,util_matrix,SIZE_IMAGE)
    out_q.put((indiv_mat[CENTER,0],rat))

def load_probe(amount):
    f = open("../netflix/probe.txt", "r")
    line = f.readline()
    movie = 0
    data = []
    movie_user = []
    x = 0
    while line!="":
        if ":" in line:
            if movie_user:
                data.append(movie_user)
            movie_user = []
            movie_user.append(int(line[:-2])-1)
        else:
            movie_user.append(int(line)-1)
        line = f.readline()
    if amount == -1:
        amount = len(data)
    return data[:amount]
def get_user_file(user):
    #for test
    n = int(user/64)*64
    n2 = int(n+64)
    if n == 2649408:
        n2 = 2649429
    return str(n)+"-"+str(n2)
def load_data(file_loc, amount, SIZE_IMAGE):
    probe_set = load_probe(amount)
    total = len(probe_set)
    #all data for training
    matrices = []
    #all data for ground truth
    truths = []

    user_sim_files = sorted(os.listdir(file_loc))

    #load matrix of movies
    movie_sim = np.load("../data/output/movie_similarity_matrix.npy")

    #load utility matrix
    util_matrix = sp.load_npz("../data/output/utility_matrix.npz")
    x = 0
    out_q = Queue()
    procs = []
    predictions = []
    ratings = []

    for movie_user in probe_set:
        x +=1
        progbar.printb(x, total)
        center_movie = movie_user[0]
        for user in movie_user[1:]:
            f = open(os.path.join(file_loc,get_user_file(user)),"r")
            center_user = -1
            mat = True
            while center_user != int(user):
                line = f.readline()
                line = line.replace(")","").replace("(","").split(',')
                if line[0] == "":
                    mat = False
                    break
                center_user = int(line[0])
            f.close()
            if mat:
                sim_movies = movie_sim[center_movie]
                p = Process(target=make_img, args=(sim_movies,line,util_matrix,SIZE_IMAGE, out_q))
                procs.append(p)
                p.start()
            else:
                #placing if ERROR no movie found 
                predictions.append(10)
                ratings.append(6)

            if len(procs) >= 16:
                for p in procs:
                    pred, rat = out_q.get()
                    predictions.append(pred)
                    ratings.append(rat)

                for p in procs:
                    p.join()

                for prediction,rating in zip(predictions,ratings):
                    fl = open("..data/results/results_non_net_image","a+") 
                    fl.write(str(rating)+","+str(prediction)+"\n")
                    fl.close()
                predictions = []
                ratings = []
                procs = []


load_data("../data/output/user_sim_files", -1, 3)