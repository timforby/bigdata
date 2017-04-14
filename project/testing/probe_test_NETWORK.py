import os

os.environ['THEANO_FLAGS']="device=cuda1,floatX=float32,lib.cnmem=0.2"
from keras.models import Model, load_model # basic class for specifying and training a neural network
from keras.callbacks import ModelCheckpoint # to save vals
from keras.utils import np_utils
import numpy as np
import time
import image_create
import progbar
from multiprocessing import Process, Queue
from scipy import sparse as sp



def t_int(val):
	if val.shape == (1,5):
		sol = np.argmax(val)+1
	else:
		sol = val[:,:][0][0]
	return sol

#============ LOAD DATA ================

np.set_printoptions(suppress=True)
def make_img(sim_movies, line, util_matrix, SIZE_IMAGE, out_q):
    CENTER = int(SIZE_IMAGE/2)
    #matrix is of size 99x99 - 49vals then center then 49vals
    indiv_mat,rat = image_create.make_img(sim_movies,line,util_matrix,SIZE_IMAGE)
    out_q.put((indiv_mat.reshape((1, SIZE_IMAGE, SIZE_IMAGE, 1)),rat))

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
    n = int(user/64)*64
    n2 = int(n+64)
    if n == 2649408:
        n2 = 2649429
    return str(n)+"-"+str(n2)
def load_data(file_loc, amount, SIZE_IMAGE, model, model2):
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
                    prediction2 = prediction
                    if type(prediction).__module__ == np.__name__:
                    	prediction2 = t_int(model2.predict(prediction))
                    	prediction1 = t_int(model.predict(prediction))
                    fl = open("..data/results/results_cnn","a+")
                    fl.write(str(rating)+","+str(prediction2)+"\n")
                    fl.close()
                    fl = open("..data/results/results_dn","a+") 
                    fl.write(str(rating)+","+str(prediction1)+"\n")
                    fl.close()
                predictions = []
                ratings = []
                procs = []


#============= MODEL ===================
model2 = load_model(os.path.join('../processing/model/','weights2.hdf5')) # To define a model, just specify its input and output layers
#model3 = load_model(os.path.join('model2','weights2.hdf5')) # To define a model, just specify its input and output layers
model = load_model(os.path.join('../processing/model/','weights.hdf5')) # To define a model, just specify its input and output layers
load_data("../data/output/user_sim_files", -1, 99, model, model2)

