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
	stand= [[[[DUMMY for i in range(0,2)] for j in range(0,2)] for k in range(0,2)] for l in range(0,32)]
	#created a matrix of size [1-31][0-1][0-1]	

	stand[11][1][1][0]= 1.5 * (1- prob_bj(dealers_card,p))
	stand[11][1][1][1]= 1.5 * (1- prob_bj(dealers_card,p))

	#potential mistake
	stand[21][1][0][0] = stand[11][1][1][0]
	stand[21][1][0][1] = stand[11][1][1][1]
	stand[21][0][0][0] = prob_less(21) - prob_greater(21)
	stand[21][0][0][1] = prob_less(21) - prob_greater(21)
	stand[21][0][1][0] = prob_less(21) - prob_greater(21)
	stand[21][0][1][1] = prob_less(21) - prob_greater(21)

	#whenn i get busted
	for i in range(22, 32):
		stand[i][0][0][0]=-1
		stand[i][0][0][1]=-1
		stand[i][0][1][0]=-1
		stand[i][0][1][1]=-1

	#when im in bw 21 and  17
	for i in range(17,21):
		stand[i][0][0][0]= prob_less(i) - prob_greater(i)
		stand[i][0][0][1]= prob_less(i) - prob_greater(i)
		stand[i][1][0][0]= prob_less(i) - prob_greater(i)
		stand[i][1][0][1]= prob_less(i) - prob_greater(i)

	#when im less than this toh i hope ki uska bust ho jaaye
	for i in range(2,17):
		stand[i][0][0][0]= 2*prob_bust(dealers_card,p) - 1
		stand[i][0][0][1]= 2*prob_bust(dealers_card,p) - 1
		stand[i][1][0][0]= 2*prob_bust(dealers_card,p) - 1
		stand[i][1][0][1]= 2*prob_bust(dealers_card,p) - 1

	#handling aces
	for i in range(2,21):
		stand[i][0][1][0]=maxi(stand[i+10][0][0][0],stand[i][0][0][0])
		stand[i][0][1][1]=maxi(stand[i+10][0][0][0],stand[i][0][0][0])
		stand[i][1][1][0]=maxi(stand[i+10][0][0][0],stand[i][0][0][0])
		stand[i][1][1][1]=maxi(stand[i+10][0][0][0],stand[i][0][0][0])
		# because if sum is less than 21 toh sirf sum matter karega
	
	#time to sit down

	#double down
	#ONLY VALID IN FIRST MOVE

	#fill poora and while filling best take care ki valid moves mei se hi best chuna jaaye
	#initi
	dd = [[[[DUMMY for i in range(0,2)] for j in range(0,2)] for k in range(0,2)] for l in range(0,32)]

	#potential error - BLACKJACK MAY NOT HAVE BEEN HANDLED
	#summation mei stand mei hamesha 0 liya hai c => num cards>2 ...may be wrong?

	for n in range(2,22):
		for c in range(2):
			for a in range(2):
				dd[n][c][a][0]= p*stand[n+10][0][a][0]
				dd[n][c][a][1]= p*stand[n+10][0][a][1]
				#handling face card
				for i in range(2,10):
					dd[n][c][a][0]+= q*stand[n+i][0][a][0]
					dd[n][c][a][1]+= q*stand[n+i][0][a][1]
				#handling the ace ab-
				dd[n][c][a][0]+= q*stand[n+1][0][(a+2)/2][0]
				dd[n][c][a][1]+= q*stand[n+1][0][(a+2)/2][1]
				#here i have made sure that if a is 1 and i get another then its still one

	#hit and best simultaneously
	best = [[[[DUMMY for i in range(0,2)] for j in range(0,2)] for k in range(0,2)] for l in range(0,32)]
	hit = [[[[DUMMY for i in range(0,2)] for j in range(0,2)] for k in range(0,2)] for l in range(0,32)]

	for i in range(22,32):
		for c in range(2):
			for a in range(2):
				for s in range(2):
					best[i][c][a][s]= -1

	for c in range(2):
		for s in range(2):
			for a in range(2):
				hit[21][c][a][s] = -1
				best[21][c][a][s]= maxi(hit[21][c][a][s],stand[21][c][a][s])

	for i in range(20,1,-1):
		for c in range(2):
			for s in range(2):
				for a in range(2):
					hit[i][c][a][s] = 0
					for j in range(2,10):
						hit[i][c][a][s] += q * best[n+j][0][a][s]
					hit[i][c][a][s] += p* best[n+10][0][a][s] 
					hit[i][c][a][s] += q* best[n+1][0][(a+2)/2][s]
					if(c==0):
						best[i][c][a][s]= maxi(hit[i][c][a][s],stand[i][c][a][s])
					else:
						best[i][c][a][s]= max(hit[i][c][a][s],stand[i][c][a][s],dd[i][c][a][s])
						# best[i][c][a][s]= max()
						
	# we have assigned best values to splittable states which may not be correct
	#take care
	#potential source of error


	#handling splitting
	split = [[[[DUMMY for i in range(0,2)] for j in range(0,2)] for k in range(0,2)] for l in range(0,32)]

	#handling aces later
	for i in range(2,11):
		#case1 - assume split is besr
		split[2*i][1][0][1]= 0
		temp=0
		for j in range(2,i):
			temp = temp + q*best[i+j][1][0][0]
		for j in range(i+1,10):
			temp = temp + q*best[i+j][1][0][0]

		temp += q* best[i+1][1][1][0]
		if(i!=10):
			temp += temp + p*best[i+10][1][0][0]

		temp= 2*temp
		if(i==10):
			split[2*i][1][0][1]= temp/(1-2*p)
		else:
			split[2*i][1][0][1]= temp/(1-2*q)

	#checking for contradiction
		if(split[2*i][1][0][1] >=  best[2*i][1][0][1]):
			#badhiya
			best[2*i][1][0][1]= split[2*i][1][0][1]
		else:
			#panga ho giya
			#dhyaan se likhiyo please