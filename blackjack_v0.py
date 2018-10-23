from dealer_probability import *



def something():
	#create stand matrix
	stand= [[[DUMMY for i in range(0,32)] for j in range(0,2)] for k in range(0,2)]
	#created a matrix of size [1-31][0-1][0-1]	

	stand[11][1][1]= 