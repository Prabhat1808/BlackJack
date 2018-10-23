#blakjack a4
#jayant and kanaujia
DUMMY = -100

def prob_bj(card , p):
	if card==1 :
		#implies ace
		return p
	elif card==10:
		return (1-p)/9
	else:
		return 0

#def prob_bust():


def prob_end(dealers_card,end_game,p):
	#returns the probability for one of the endgame for the dealer - 17, 18, 19, 20, 21
	# #dp
	soft_dp = [DUMMY for i in range(0,32)]
	hard_dp = [DUMMY for j in range(0,32)]

	#initialise
	#base case
	soft_dp[end_game]=1
	hard_dp[end_game]=1
	for i in range(end_game+1,32):
		hard_dp[i]=0

	for i in range(end_game+1, 22):
		soft_dp[i]=0
	for i in range(17,end_game):
		hard_dp[i]=0
		soft_dp[i]=0

	def soft(summ , end ):
		if soft_dp[summ] != DUMMY :
			return soft_dp[summ]
		else:
			if(summ>21):
				soft_dp[summ] = hard(summ-10, end)
				return hard(summ-10, end)
			#calculate it as
			soft_dp[summ]=0
			for i in range(2,10):
				#X(i,j,true) is soft
				soft_dp[summ] += ((1.-p)/9)*soft(summ+i,end)
			soft_dp[summ] += ((1.-p)/9)*soft(summ+1,end)
			soft_dp[summ] += p*soft(summ+10,end)

			return soft_dp[summ]

	def hard(summ, end ):
		if hard_dp[summ] != DUMMY:
			return hard_dp[summ]
		else:
			hard_dp[summ]=0
			counter=0
			for i in range(2,10):
				# if(hard(summ+i,end)>0 ):
				# 	counter=counter+1
				# print counter
				hard_dp[summ] += ((1.-p)/9)*hard(summ+i,end)
			hard_dp[summ] += ((1.-p)/9)*soft(summ+11,end)#handling the ace
			hard_dp[summ] += p*hard(summ+10,end)

			return hard_dp[summ]
	shift=0
	if end_game==21:
		shift = prob_bj(dealers_card, p)

	if dealers_card==1:
		return soft(11,end_game)- shift
	else:
		return hard(dealers_card,end_game) - shift

def prob_bust(dealers_card,p):
	answer=1
	for i in range(17,22):
		answer= answer- prob_end(dealers_card,i,p)
	answer= answer- prob_bj(dealers_card,p)
	return answer


def prob_greater(dealers_card, threshold, p):
	answer=0
	for i in range(threshold+1, 22):
		answer=answer+ prob_end(dealers_card, i, p)
	answer=answer+ prob_bj(dealers_card,p)
	#answer=answer+ prob_bust(dealers_card,p)
	return answer

def prob_less(dealers_card, threshold,p):
	answer=0
	for i in range(17, threshold):
		answer= answer + prob_end(dealers_card, i ,p)
	answer=answer+ prob_bust(dealers_card,p)
	return answer

def print_all():
	for i in range(1,11):
		for j in range(17,22):
			print prob_end(i,j,0.307),
		print prob_bj(i,0.307), prob_bust(i,0.307)


print_all()















