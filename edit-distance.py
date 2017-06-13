import itertools
import sys
import pickle
import random
import time

# Only me and god knows how this code works
# In a few days only god will now

#[filename1,filename2] = random.sample(range(0,1002),2)
#filename1 = 'tv_'+filename1
#filename2 = 'tv_'+filename2

filename1 =  sys.argv[1]
filename2 = sys.argv[2]

start_time = time.time()

parent_path = '/home/raghavendra/Desktop/adhitya/'
dictionary_path = parent_path + 'dictionary/'

dictionary1 = dictionary_path + filename1
dictionary2 = dictionary_path + filename2

with open(dictionary1+'-right.txt', 'rb') as handle:
  r1 = pickle.loads(handle.read())

with open(dictionary2+'-right.txt', 'rb') as handle:
  r2 = pickle.loads(handle.read())

with open(dictionary1+'-parent.txt', 'rb') as handle:
  p1 = pickle.loads(handle.read())

with open(dictionary2+'-parent.txt', 'rb') as handle:
  p2 = pickle.loads(handle.read())

with open(dictionary1+'-labels.txt', 'rb') as handle:
  l1 = pickle.loads(handle.read())

with open(dictionary2+'-labels.txt', 'rb') as handle:
  l2 = pickle.loads(handle.read())

with open(dictionary1+'-difference.txt', 'rb') as handle:
  d1 = pickle.loads(handle.read())

with open(dictionary2+'-difference.txt', 'rb') as handle:
  d2 = pickle.loads(handle.read())

size1 = len(p1.keys())
size2 = len(p2.keys())

Q = {}
Q1 = {}
Q2 = {}
a = 1
b = 0.5


def p(i, j):
    return abs(l1[i] - l2[j])


def checkBadExtents1(i1, i):
    if (i <= 0 or i > size1 or i1 <= 0 or i1 > size1):
        return True
    return False

def checkBadExtents2(j1, j):
    if (j <= 0 or j > size2 or j1 <= 0 or j1 > size2):
        return True
    return False


def Qf(i1, i, j1, j):
    print i1, i, j1, j

    try:
        Q[i1][i][j1][j] += 0
    except:
        if i1 not in Q.keys():
            Q[i1] = {}
        if i not in Q[i1].keys():
            Q[i1][i] = {}
        if j1 not in Q[i1][i].keys():
            Q[i1][i][j1] = {}
        if j not in Q[i1][i][j1].keys():
            Q[i1][i][j1][j] = {}

    if ((i1 == 0) or (i == 0) or (j1 == 0) or (j == 0)):
        Q[i1][i][j1][j] = 0
        return Q[i1][i][j1][j]

    t1, t2 = True, True
    if (j < j1 or checkBadExtents2(j1, j)):
        t2 = False
    if (i < i1 or checkBadExtents1(i1, i)):
        t1 = False
    if (t1 == False and t2 == False):
        Q[i1][i][j1][j] = 0
        return Q[i1][i][j1][j]
    elif (t1 == False or t2 == False):
        Q[i1][i][j1][j] = float('inf')
        return Q[i1][i][j1][j]

    if (bool(Q[i1][i][j1][j])):
        return Q[i1][i][j1][j]
    else:
        Q[i1][i][j1][j] = min(Qf(i1, i - 1, j1, j) + p(i, j), Q1f(i1, i, j1, j), Q2f(i1, i, j1, j))
        return Q[i1][i][j1][j]


def Q1f(i1, i, j1, j):
    print i1, i, j1, j

    try:
        Q1[i1][i][j1][j] += 0
    except:
        if i1 not in Q1.keys():
            Q1[i1] = {}
        if i not in Q1[i1].keys():
            Q1[i1][i] = {}
        if j1 not in Q1[i1][i].keys():
            Q1[i1][i][j1] = {}
        if j not in Q1[i1][i][j1].keys():
            Q1[i1][i][j1][j] = {}

    if ((i1 == 0) or (i == 0) or (j1 == 0) or (j == 0)):
        Q1[i1][i][j1][j] = 0
        return Q1[i1][i][j1][j]

    t1, t2 = True, True
    if (j < j1 or checkBadExtents2(j1, j)):
        t2 = False
    if (i < i1 or checkBadExtents1(i1, i)):
        t1 = False
    if (t1 == False and t2 == False):
        Q1[i1][i][j1][j] = 0
        return Q1[i1][i][j1][j]
    elif (t2 == False):
        Q1[i1][i][j1][j] = a + b * i
        return Q1[i1][i][j1][j]
    elif (t1 == False):
        Q1[i1][i][j1][j] = float('inf')
        return Q1[i1][i][j1][j]

    if (bool(Q1[i1][i][j1][j])):
        return Q1[i1][i][j1][j]
    else:
        minimum = float('inf')
        for k in range(j1, j + 1):
            minimum = min(minimum, Q1f(i1, p1[i], j1, k) + Qf(p1[i] + 1, i - 1, k + 1, j) + b)
        Q1[i1][i][j1][j] = min(Qf(i1, i - 1, j1, j) + a + b, Q1f(i1, i - 1, j1, j) + b, minimum)
        return Q1[i1][i][j1][j]


def Q2f(i1, i, j1, j):
    print i1, i, j1, j

    try:
        Q2[i1][i][j1][j] += 0
    except:
        if i1 not in Q2.keys():
            Q2[i1] = {}
        if i not in Q2[i1].keys():
            Q2[i1][i] = {}
        if j1 not in Q2[i1][i].keys():
            Q2[i1][i][j1] = {}
        if j not in Q2[i1][i][j1].keys():
            Q2[i1][i][j1][j] = {}

    if ((i1 == 0) or (i == 0) or (j1 == 0) or (j == 0)):
        Q2[i1][i][j1][j] = 0
        return Q2[i1][i][j1][j]

    t1, t2 = True, True
    if (j < j1 or checkBadExtents2(j1, j)):
        t2 = False
    if (i < i1 or checkBadExtents1(i1, i)):
        t1 = False
    if (t1 == False and t2 == False):
        Q2[i1][i][j1][j] = 0
        return Q2[i1][i][j1][j]
    elif (t1 == False):
        Q2[i1][i][j1][j] = a + b * i
        return Q2[i1][i][j1][j]
    elif (t2 == False):
        Q2[i1][i][j1][j] = float('inf')
        return Q2[i1][i][j1][j]
    
    if (bool(Q2[i1][i][j1][j])):
        return Q2[i1][i][j1][j]
    else:
        minimum = float('inf')
        for k in range(i1, i + 1):
            minimum = min(minimum, Q2f(i1, k, j1, p2[j]) + Qf(k + 1, i, p2[j] + 1, j - 1) + b)
        Q2[i1][i][j1][j] = min(Qf(i1, i, j1, j - 1) + a + b, Q2f(i1, i, j1, j - 1) + b, minimum)
        return Q2[i1][i][j1][j]

for i1, j1 in itertools.product(range(1, size1+1), range(1, size2+1)):
    for i in range(i1, r1[i1] + 1):
        for j in range(j1, r2[j1] + 1):
            Q1[i1][i][j1][j] = Q1f(i1, i, j1, j)
            Q2[i1][i][j1][j] = Q2f(i1, i, j1, j)
            Q[i1][i][j1][j] = Qf(i1, i, j1, j)
            # print i1, i, j, j1


print "echo \'<html><img src=\"images/"+ filename1 +".png\"\"/><img src=\"images/"+ filename2 +".png\"\"/></html>\';"

print 'Difference: ', Q[1] [r1[1]] [1] [r2[1]]

seconds = time.time() - start_time
m, s = divmod(seconds, 60)
h, m = divmod(m, 60)
print "%d:%02d:%02d" % (h, m, s)
