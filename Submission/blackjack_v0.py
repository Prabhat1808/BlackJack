from dealer_probability import *
import sys

P = 0.307
HARD= []
SOFT=[]
PAIR=[]

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
	stand[21][0][0][0] = prob_less(dealers_card,21,p) - prob_greater(dealers_card,21,p)
	stand[21][0][0][1] = prob_less(dealers_card,21,p) - prob_greater(dealers_card,21,p)
	stand[21][0][1][0] = prob_less(dealers_card,21,p) - prob_greater(dealers_card,21,p)
	stand[21][0][1][1] = prob_less(dealers_card,21,p) - prob_greater(dealers_card,21,p)

	#whenn i get busted
	for i in range(22, 32):
		stand[i][0][0][0]=-1
		stand[i][0][0][1]=-1
		stand[i][0][1][0]=-1
		stand[i][0][1][1]=-1

	#when im in bw 21 and  17
	for i in range(17,21):
		stand[i][0][0][0]= prob_less(dealers_card,i,p) - prob_greater(dealers_card,i,p)
		stand[i][0][0][1]= prob_less(dealers_card,i,p) - prob_greater(dealers_card,i,p)
		stand[i][1][0][0]= prob_less(dealers_card,i,p) - prob_greater(dealers_card,i,p)
		stand[i][1][0][1]= prob_less(dealers_card,i,p) - prob_greater(dealers_card,i,p)

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
				dd[n][c][a][0]= 2*p*stand[n+10][0][a][0]
				dd[n][c][a][1]= 2*p*stand[n+10][0][a][1]
				#handling face card
				for i in range(2,10):
					dd[n][c][a][0]+= 2*q*stand[n+i][0][a][0]
					dd[n][c][a][1]+= 2*q*stand[n+i][0][a][1]
				#handling the ace ab-
				dd[n][c][a][0]+= 2*q*stand[n+1][0][(a+2)/2][0]
				dd[n][c][a][1]+= 2*q*stand[n+1][0][(a+2)/2][1]
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
						hit[i][c][a][s] += q * best[i+j][0][a][s]
					hit[i][c][a][s] += p* best[i+10][0][a][s]
					hit[i][c][a][s] += q* best[i+1][0][(a+2)/2][s]
					if(c==0):
						best[i][c][a][s]= max(hit[i][c][a][s],stand[i][c][a][s])
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
			temp = temp + p*best[i+10][1][0][0]

		temp= 2*temp
		if(i==10):
			split[2*i][1][0][1]= temp/(1-2*p)
		else:
			split[2*i][1][0][1]= temp/(1-2*q)

	#checking for contradiction
		if(split[2*i][1][0][1] >=  best[2*i][1][0][1]):
			#badhiya
			# if i==9 :
			# 	print "yes for a pair of 9 split is optimal"
			best[2*i][1][0][1]= split[2*i][1][0][1]
		else:
			#panga ho giya
			#dhyaan se likhiyo please

			#case2
			# if i==9 :
			# 	print "no for a pair of 9 split is not optimal"
			# 	print split[18][1][0][1]
			# 	print "this was the proposed split "
			# 	print "but its not better than "
			# 	print best[18][1][0][1]

			temp = 0
			for j in range(2,10):
				temp = temp + q*(best[j+i][1][0][0])
			temp = temp + p*(best[i+10][1][0][0])
			temp = temp + q*(best[i+1][1][1][0])

			#best jo set hai voh sahi hai but we still get the new correct value of splittable
			split[2*i][1][0][1] = 2*temp

			# if i==9:
			# 	print "newly found actual split for 9,9 is"
			# 	print split[2*i][1][0][1]

	#handle the pair of aces case
	#can split only once
	#no bj after this and no doubling either
	temp=0
	for j in range(2,10):
		temp = temp + q* stand[1+j][0][1][0]
	temp= temp + p*stand[11][0][1][0]
	temp= temp + q*stand[2][0][1][0] #haan consider the non splittable version

	temp= 2*temp

	split[2][1][1][1] = temp
	if(temp>best[2][1][1][1]):
		best[2][1][1][1]=temp

	def chosen(n, c, a, s ):
		if(best[n][c][a][s]== hit[n][c][a][s]):
			return "H"
		elif(best[n][c][a][s]== dd[n][c][a][s]):
			return "D"
		elif(best[n][c][a][s]== stand[n][c][a][s]):
			return "S"
		elif(best[n][c][a][s]== split[n][c][a][s]):
			return "P"
		else:
			return "ERROR"

	def return_policy():
		#for all possible initial hands i have return the best move

		#pehle hard
		# print "hard"
		h = []
		for j in range(5,20):
			# print j, chosen(j,1,0,0)
			h.append(chosen(j,1,0,0))
		HARD.append(h)

		# print
		# print "now soft"
		s=[]
		for j in range(3,12):
			# print j-1,  chosen(j,1,1,0)
			s.append(chosen(j,1,1,0))
		SOFT.append(s)

		# print
		# print "now pairs"
		p = []
		for j in range(2,11):
			# print j, chosen(2*j, 1,0,1)
			p.append(chosen(2*j, 1,0,1))
		# print 'A',  chosen(2,1,1,1)
		p.append(chosen(2,1,1,1))
		PAIR.append(p)

	def return_everything():
		#for all possible initial hands i have return the best move

		#pehle hard
		print "hard"
		for j in range(5,20):
			print j, chosen(j,1,0,0), hit[j][1][0][0] , stand[j][1][0][0], dd[j][1][0][0], split[j][1][0][0]

		print
		print "now soft"
		for j in range(3,12):
			print j-1,  chosen(j,1,1,0) , hit[j][1][1][0] , stand[j][1][1][0], dd[j][1][1][0], split[j][1][1][0]

		print
		print "now pairs"
		for j in range(2,11):
			print j, chosen(2*j, 1,0,1) ,  hit[2*j][1][0][1] , stand[2*j][1][0][1], dd[2*j][1][0][1], split[2*j][1][0][1], best[2*j][1][0][1]
		print 'A',  chosen(2,1,1,1) ,  hit[2][1][1][1] , stand[2][1][1][1], dd[2][1][1][1], split[2][1][1][1]

	return_policy()

# something(10,0.307)
def trans(m):
	pose = [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]
	return pose

# for i in range(2,11):
# 	something(i,P)
# something(1,P)

# print "HARD"
# HARD = trans(HARD)
# for row in HARD:
# 	print row
#
# print "SOFT"
# SOFT = trans(SOFT)
# for row in SOFT:
# 	print row
#
# print "PAIR"
# PAIR = trans(PAIR)
# for row in PAIR:
# 	print row

# for j in range(5,20):
# 	print j, "\t",
# 	for i in HARD[j-5]:
# 		print i, " ",
# 	print "\n"
#
# for j in range(3,11):
# 	print "A"+str(j-1),"\t",
# 	for i in SOFT[j-3]:
# 		print i, " ",
# 	print "\n"
#
# for j in range(2,11):
# 	print str(j)+str(j),"\t",
# 	for i in PAIR[j-2]:
# 		print i," ",
# 	print "\n"
# print "AA","\t",
# for i in PAIR[9]:
# 	print i, " ",

def output_policy():
	global HARD
	global SOFT
	global PAIR
	out_str = ""

	for i in range(2,11):
		something(i,P)
	something(1,P)

	HARD = trans(HARD)
	SOFT = trans(SOFT)
	PAIR = trans(PAIR)

	for j in range(5,20):
		print j, "\t",
		out_str = out_str + str(j) + "\t"
		for i in HARD[j-5]:
			print i, " ",
			out_str = out_str + str(i) + " "
		out_str = out_str+"\n"
		print

	for j in range(3,11):
		print "A"+str(j-1),"\t",
		out_str = out_str + "A" + str(j-1) + "\t"
		for i in SOFT[j-3]:
			print i, " ",
			out_str = out_str + str(i) + " "
		out_str = out_str+"\n"
		print

	for j in range(2,11):
		print str(j)+str(j),"\t",
		out_str = out_str + str(j)*2 + "\t"
		for i in PAIR[j-2]:
			print i," ",
			out_str = out_str + str(i) + " "
		out_str = out_str+"\n"
		print
	print "AA","\t",
	out_str = out_str + "AA\t"
	for i in PAIR[9]:
		print i, " ",
		out_str = out_str + str(i) + " "

	return out_str

P = float(sys.argv[1])
policy = output_policy()
file = open("Policy.txt","w+")
file.write(policy)
