import itertools
import sys
import pickle

# Only me and god knows how this code works
# In a few days only god will now

#filename1 =  sys.argv[1]
#filename2 = sys.argv[2]

from binarytree import tree, pprint

i1 = {}
p1 = {}
r1 = {}
l1 = {}

i2 = {}
p2 = {}
r2 = {}
l2 = {}
index = 1

def preorder(tree, parent, i, p, r, l):
	global index
	if(tree == None):
		return
	else:
		#print tree.value, parent.value, right_ancestor(tree)
		i[tree.value] = index
		if(tree.value == parent.value):
			p[index] = 0
		else:
			p[index] = i[parent.value]
		l[index] = tree.value
		r[index] = right_ancestor(tree)
		index += 1
		preorder(tree.left, tree, i, p, r, l)
		preorder(tree.right, tree, i, p, r, l)

def right_ancestor(tree):
	if(tree == None):
		return
	elif(tree.right == None):
		return tree.value
	else:
		return right_ancestor(tree.right)

tree1 = tree()
preorder(tree1, tree1, i1, p1, r1, l1)
index = 1
for i in r1.keys():
	r1[i] = i1[r1[i]]

tree2 = tree()
preorder(tree2, tree2, i2, p2, r2, l2)
index = 1
for i in r2.keys():
	r2[i] = i2[r2[i]]

size1 = len(p1.keys())
size2 = len(p2.keys())

Q = {}
Q1 = {}
Q2 = {}
a = 1
b = 0.5


def p(i, j):
    return abs(l1[i]-l2[j])


def checkBadExtents1(i1, i):
    if (i <= 0 or i > size1 or i1 <= 0 or i1 > size1):
        return True
    return False

def checkBadExtents2(j1, j):
    if (j <= 0 or j > size2 or j1 <= 0 or j1 > size2):
        return True
    return False


def Qf(i1, i, j1, j):
   #print i1, i, j1, j

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
    #print i1, i, j1, j

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
    #print i1, i, j1, j

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

#print size1, size2

pprint(tree1), pprint(tree2)

print Q[1] [r1[1]] [1] [r2[1]]
