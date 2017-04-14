import os
os.environ['THEANO_FLAGS']="device=cuda1,floatX=float32,lib.cnmem=0.7"
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
kernel_size_1 = 5
kernel_size_2 = 3 
drop_prob_2 = 0.5 # dropout in the FC layer with probability 0.5



#============ LOAD DATA ================
X_train, Y_trai_ = load.load_data("../data/output/user_sim_files/user_sim", 0,section_size,image_size=99)

num_train, height, width, depth = X_train.shape # there are 50000 training examples in CIFAR-10 
Y_train = np_utils.to_categorical(Y_trai_-1, 5)


#============= MODEL ===================
inp = Input(shape=(height, width, depth)) # N.B. depth goes first in Keras!

flatten = Flatten()(inp)
hidden = Dense(9801, activation='relu')(flatten)
drop_3 = Dropout(drop_prob_2)(hidden)
hidden_2 = Dense(9801, activation='relu')(drop_3)
drop_4 = Dropout(drop_prob_2)(hidden_2)

out = Dense(5, activation='softmax')(drop_4)

model = Model(inp, out) # To define a model, just specify its input and output layers
os.makedirs("model", exist_ok=True)
checkpointer = ModelCheckpoint(filepath="model/weights.hdf5", verbose=0, save_best_only=False)

train_loss = []
validation_loss =[]
#============= MODEL RUN===============
model.compile(loss='categorical_crossentropy', # using the cross-entropy loss function
              optimizer=optimizers.RMSprop(lr=0.001), # using the Adam optimiser
              metrics=['accuracy']) # reporting the accuracy
for i in range(section_size,256000,section_size):
	for x in range(num_epochs):
		print("Section:"+ str(i/section_size)+" --Epoch: "+ str(x))
		history = model.fit(X_train, Y_train,#(Y_trai_[:,0,0,:]/4) Train the model using the training set...
		          batch_size=batch_size, epochs=1,
		          verbose=0, validation_split=0.1, callbacks=[checkpointer]) # ...holding out 10% of the data for validation
		train_loss.append(history.history['loss'])
		validation_loss.append(history.history['val_loss'])
		log.loss_curve(train_loss,validation_loss,"costs.png")
	if i%10==0:
		for j in range(2):
			print(model.predict(X_train)[j])
			print(str(Y_train[j]))

	X_train, Y_trai_ = load.load_data("user_sim", i,i+section_size, image_size=99)
	Y_train = np_utils.to_categorical(Y_trai_-1, 5)

