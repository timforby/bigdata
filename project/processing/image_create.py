import numpy as np

def make_img(sim_movies, line, util_matrix, SIZE_IMAGE):
    #matrix is of size 99x99 - 49vals then center then 49vals
    indiv_mat = np.zeros((SIZE_IMAGE,SIZE_IMAGE))
    weights = 0
    weighted_ratings = 0
    mid = int((SIZE_IMAGE-1)/2)
    #for all image pixels
    for i in range(0,SIZE_IMAGE):
        #gets offset ==> |3|1|0|2|4 transpose
        col_offset = -1 if i%2==1 else 1
        #coeff is the similarity measure between user in center
        user_coeff=float(line[2*i+1])
        col_i = int((col_offset*int((i+1)/2))+mid)

        for j in range(0,SIZE_IMAGE):
            if i==0 and j==0:
                continue
            #get row offset 
            row_offset = -1 if j%2==1 else 1
            movie_coeff=sim_movies[2*j+1]
            row_i = int((row_offset*int((j+1)/2))+mid)
            rating = util_matrix[int(sim_movies[2*j]),int(line[2*i])]
            weight = movie_coeff*user_coeff
            #applying coeef to rating (rating could not exists and be 0)
            weighted_rating = weight*rating
            weighted_ratings += weighted_rating
            #if rating is 0 we dont want to add weights
            if weighted_rating > 0:
                weights += weight
            #set weighted rating
            indiv_mat[row_i, col_i] = weighted_rating
    if weighted_ratings !=0:
        indiv_mat[mid,mid] = weighted_ratings/weights
    else:
        indiv_mat[mid,mid] = 3
    #indiv_mat/=5#np.max(indiv_mat)
    rating = util_matrix[int(sim_movies[0]),int(line[0])]
    #returns teh image and the true rating
    return indiv_mat, rating

#similar to make img but just for the movies
def make_vect(sim_movies, line, util_matrix, SIZE_IMAGE):
    #matrix is of size 99x99 - 49vals then center then 49vals
    indiv_mat = np.zeros((SIZE_IMAGE,1))
    weights = 0
    weighted_ratings = 0
    mid = int((SIZE_IMAGE-1)/2)


    for j in range(0,SIZE_IMAGE):
        if j==0:
            continue
        row_offset = -1 if j%2==1 else 1
        movie_coeff=sim_movies[2*j+1]
        row_i = int((row_offset*int((j+1)/2))+mid)
        rating = util_matrix[int(sim_movies[2*j]),int(line[0])]
        weight = movie_coeff
        weighted_rating = weight*rating
        weighted_ratings += weighted_rating
        if weighted_rating > 0:
            weights += weight
        indiv_mat[row_i, 0] = weighted_rating
    if weighted_ratings !=0:
        indiv_mat[mid,0] = weighted_ratings/weights
    else:
        indiv_mat[mid,0] = 3
    rating = util_matrix[int(sim_movies[0]),int(line[0])]
    return indiv_mat, rating
