from dealer_probability import *

def maxi(a,b):
	if a>b:
		return a
	else:
		return b
# def ace_addition
def something(dealers_card,p):
	#create stand matrix
	q=(1.-p)/9
	stand= [[[DUMMY for i in range(0,2)] for j in range(0,2)] for k in range(0,32)]
	#created a matrix of size [1-31][0-1][0-1]	

	stand[11][1][1]= 1.5 * (1- prob_bj(dealers_card,p))

	#potential mistake
	stand[21][1][0] = stand[11][1][1]
	stand[21][0][0] = prob_less(21) - prob_greater(21)
	stand[21][0][1] = prob_less(21) - prob_greater(21)

	#whenn i get busted
	for i in range(22, 32):
		stand[i][0][0]=-1
		stand[i][0][1]=-1

	#when im in bw 21 and  17
	for i in range(17,21):
		stand[i][0][0]= prob_less(i) - prob_greater(i)
		stand[i][1][0]= prob_less(i) - prob_greater(i)

	#when im less than this toh i hope ki uska bust ho jaaye
	for i in range(2,17):
		stand[i][0][0]= 2*prob_bust(dealers_card,p) - 1
		stand[i][1][0]= 2*prob_bust(dealers_card,p) - 1

	#handling aces
	for i in range(2,21):
		stand[i][0][1]=maxi(stand[i+10][0][0],stand[i][0][0])
		stand[i][1][1]=maxi(stand[i+10][0][0],stand[i][0][0])
		# because if sum is less than 21 toh sirf sum matter karega
	
	#time to sit down

	#double down
	#ONLY VALID IN FIRST MOVE

	#fill poora and while filling best take care ki valid moves mei se hi best chuna jaaye
	#initi
	dd = [[[DUMMY for i in range(0,2)] for j in range(0,2)] for k in range(0,32)]

	#potential error - BLACKJACK MAY NOT HAVE BEEN HANDLED
	#summation mei stand mei hamesha 0 liya hai c => num cards>2 ...may be wrong?

	for n in range(2,22):
		for c in range(2):
			for a in range(2):
				dd[n][c][a]= p*stand[n+10][0][a]
				#handling face card
				for i in range(2,10):
					dd[n][c][a]+= q*stand[n+i][0][a]
				#handling the ace ab-
				dd[n][c][a]+= q*stand[n+1][0][(a+2)/2]
				#here i have made sure that if a is 1 and i get another then its still one