import numpy as np
p = 0.1
q = (1-p)/9

HARD = [[0.0 for i in range(22)] for j in range(32)]
SOFT = [[0.0 for i in range(22)] for j in range(32)]

for i in range(17,22):
    HARD[i][i] = 1.0
    SOFT[i][i] = 1.0

for i in range(17,22):
    HARD[16][i] = q
    # SOFT[16][i] = q

for i in range(15,10,-1):
    for j in range(17,22):
        # if(i == 15):
        #     print ('HARD[',i+10,'][',j,'] = ',HARD[i+10][j])
        HARD[i][j] = p*HARD[i+10][j]
        for k in range(1,10):
            HARD[i][j] += q*HARD[i+k][j]
            # if(i == 15):
            #     print ('HARD[',i+k,'][',j,'] = ',HARD[i+k][j])

# for i in range()
for i in range(15,10,-1):
    for j in range(17,22):
        for k in range(1,21-i+1):
            SOFT[i][j] += q*SOFT[i+k][j]
        for k in range(21-i+1,10):
            SOFT[i][j] += q*HARD[i+k-10][j]
        SOFT[i][j] += p*HARD[i][j]
        if(i == 11 and j == 21):
            SOFT[i][j] = 0
            for k in range(1,10):
                SOFT[i][j] += SOFT[i+k][j]

for i in range(10,0,-1):
    for j in range(17,22):
        for k in range(2,10):
            HARD[i][j] += q*HARD[i+k][j]
        HARD[i][j] += p*HARD[i+10][j] + q*SOFT[i+11][j]
