import csv, sys
import pickle

filename = sys.argv[1]
parent_path = '/home/nagarjun/Desktop/Raghavendra/' 
contour_file = parent_path + filename + '.csv'

scalars = {}
visited= {}
adjacency = {}
index_map = {}
index = 1
r1 = {}
p1 = {}
l1 = {}
d1 = {}

root = None

class Tree(object):
    def __init__(self):
		self.parent = None
		self.left = None
		self.right = None
		self.data = None

def compare_nodes(a, b):
    if scalars[a] > scalars[b]:
        return 1
    elif scalars[a] == scalars[b]:
		if a > b:
			return 1
		else:
			return -1
    else:
		return -1

def traverse(i, root, vertex):
	#print root, scalars[root], i
	global index
	index_map[root] = index
	index += 1
	visited[root] = True
	adjacency[root].sort(compare_nodes)
	for j, node in enumerate(adjacency[root]):
		if(visited[node] == False):
			current = Tree()
			if(j == 0):
				vertex.left = current
			if(j == 1):
				vertex.right = current
			current.parent = vertex
			current.data = node
			traverse(j, node, current)

def preorder(tree, right_dictionary, parent_dictionary, label_dictionary, difference_dictionary):
	if(tree == None):
		return
	else:
		right_dictionary[index_map[tree.data]] = index_map[right_ancestor(tree)]
		label_dictionary[index_map[tree.data]] = scalars[tree.data]
		if tree.data != tree.parent.data:
			parent_dictionary[index_map[tree.data]] = index_map[tree.parent.data]
		else:
			parent_dictionary[index_map[tree.data]] = 0

		if (tree.left != None and tree.right != None):
			difference_dictionary[index_map[tree.data]] = max(abs(scalars[tree.right.data] - scalars[tree.data]), abs(scalars[tree.left.data] - scalars[tree.data]))
		elif (tree.left == None and tree.right != None):
			difference_dictionary[index_map[tree.data]] = abs(scalars[tree.right.data] - scalars[tree.data])
		elif (tree.left != None and tree.right == None):
			difference_dictionary[index_map[tree.data]] = abs(scalars[tree.left.data] - scalars[tree.data])
		else:
			difference_dictionary[index_map[tree.data]] = abs(scalars[tree.data])

		preorder(tree.left, right_dictionary, parent_dictionary, label_dictionary, difference_dictionary)
		preorder(tree.right, right_dictionary, parent_dictionary, label_dictionary, difference_dictionary)

def right_ancestor(tree):
	if(tree == None):
		return
	elif(tree.right == None):
		return tree.data
	else:
		return right_ancestor(tree.right)

with open(contour_file, 'rb') as csvfile:
	csvfile.readline() 
	spamreader = csv.reader(csvfile, delimiter=' ')
	for r in spamreader:
		row = r[0].split(',')
		node1 = int(row[0])
		node2 = int(row[1])
		
		scalars[node1] = float(row[2])
		scalars[node2] = float(row[3])
		
		visited[node1] = False
		visited[node2] = False

		if node1 not in adjacency.keys():
			adjacency[node1] = []

		if node2 not in adjacency.keys():
			adjacency[node2] = []

		adjacency[node1].append(node2)
		adjacency[node2].append(node1)

for i in adjacency.keys():
	if len(adjacency[i]) == 1:
		if ( (scalars[i] > scalars[adjacency[i][0]]) or ((scalars[i] == scalars[adjacency[i][0]]) and i > adjacency[i][0]) ):
			root = i

tree = Tree()
tree.data = root
tree.parent = tree
traverse(0, root, tree)

preorder(tree, r1, p1, l1, d1)

for i in index_map.keys():
	j = index_map[i]
	print j, r1[j], p1[j], l1[j], d1[j]

with open(parent_path+'intermediate/'+filename+'-right.txt', 'wb') as handle:
  pickle.dump(r1, handle)

with open(parent_path+'intermediate/'+filename+'-parent.txt', 'wb') as handle:
  pickle.dump(p1, handle)

with open(parent_path+'intermediate/'+filename+'-labels.txt', 'wb') as handle:
  pickle.dump(l1, handle)

with open(parent_path+'intermediate/'+filename+'-difference.txt', 'wb') as handle:
  pickle.dump(l1, handle)
