import os
os.environ['THEANO_FLAGS']="device=cuda0,floatX=float32,lib.cnmem=0.7"
from keras.layers import Input, Conv2D, Dense, Dropout, MaxPooling2D,Flatten
from keras.models import Model # basic class for specifying and training a neural network
from keras.callbacks import ModelCheckpoint # to save vals
from keras import optimizers
from keras.utils import np_utils


import numpy as np
import load
import log

# ===========HYPER PARAM ================
section_size = 15 #goes through a section of the user files
batch_size = section_size*5 # in each iteration
kernel_size_1 = 33 
kernel_size_2 = 17 
kernel_size_3 = 15 
kernel_size_4 = 5 
filters_1 = 4
filters_2 = 16
filters_3 = 32
filters_4 = 64
pool_size = (2, 2)
drop_prob_1 = 0.25 # dropout after pooling with probability 0.25
drop_prob_2 = 0.5 # dropout in the FC layer with probability 0.5



#============ LOAD DATA ================

X_train, Y_trai_ = load.load_data("../data/output/user_sim_files/user_sim", 0,section_size,image_size=99)

num_train, height, width, depth = X_train.shape # there are 50000 training examples in CIFAR-10 
Y_train = np_utils.to_categorical(Y_trai_-1, 5)


#============= MODEL ===================
inp = Input(shape=(height, width, depth)) # N.B. depth goes first in Keras!
# Conv [32] -> Conv [32] (with dropout on the conv2 layer)
conv_1 = Conv2D(filters_1, kernel_size_1, padding='valid', activation='relu')(inp)
conv_2 = Conv2D(filters_2, kernel_size_2, padding='valid', activation='relu')(conv_1)
pool_1 = MaxPooling2D(pool_size=pool_size)(conv_2)
#drop_1 = Dropout(drop_prob_1)(pool_1)

conv_3 = Conv2D(filters_3, kernel_size_3, padding='valid', activation='relu')(pool_1)
conv_4 = Conv2D(filters_4, kernel_size_4, padding='valid', activation='relu')(conv_3)
pool_2 = MaxPooling2D(pool_size=pool_size)(conv_4)
#drop_2 = Dropout(drop_prob_1)(pool_2)

flatten = Flatten()(pool_2)
hidden = Dense(64, activation='relu')(flatten)
#drop_3 = Dropout(drop_prob_2)(hidden)

out = Dense(1, activation='relu')(hidden)
#out = Dense(1, activation='relu')(hidden)

model = Model(inp, out) # To define a model, just specify its input and output layers
os.makedirs("model", exist_ok=True)
checkpointer = ModelCheckpoint(filepath="model/weights2.hdf5", verbose=0, save_best_only=False)

train_loss = []
validation_loss =[]
#============= MODEL RUN===============
model.compile(loss='mean_squared_error', # using the cross-entropy loss function
              optimizer=optimizers.RMSprop(lr=0.001), # using the Adam optimiser
              metrics=['accuracy']) # reporting the accuracy
for i in range(section_size,256000,section_size):
	print("Epoch:"+ str(i/section_size))
	history = model.train_on_batch(X_train, Y_train)#(Y_trai_[:,0,0,:]))# Train the model using the training set...
	delta_ =0
	for j in range(X_train.shape[0]):
		prediction = np.argmax(model.predict(X_train)[j])+1
		rating = np.argmax(Y_train)+1#Y_trai_[j][0,0,0]
		delta_ += abs(rating - prediction)
	delta_ /= batch_size
	if(delta_ > 5):
		delta_ = 5
	train_loss.append(delta_)
	#validation_loss.append(Y_trai_[j][0,0,0])
	log.loss_curve(train_loss,validation_loss,"costs_2.png")

	X_train, Y_trai_ = load.load_data("user_sim", i,i+section_size, image_size=99)
	Y_train = np_utils.to_categorical(Y_trai_-1, 5)

