import sys
sys.path.insert(0, '../processing/')
import load
import scipy.misc
import time

#creates prints images to files
imsize = 5
center = int(imsize/2)
images, ratings = load.load_data("../data/output/user_sim_files_x", 0,1,image_size=imsize)
x = 0
for i in images:
	print(i[center,center])
	print(ratings[x])
	j = scipy.misc.imresize(i[:,:,0], (1000,1000), mode='L', interp='nearest')
	scipy.misc.imsave('images/'+str(x)+'.jpg', j)
	x +=1

