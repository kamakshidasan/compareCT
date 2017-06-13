import csv, sys
import pickle
import os

filename = (sys.argv[1]).split('.')[0]
parent_path = '/home/raghavendra/Desktop/adhitya/'
tree_path = parent_path +'trees/'
dictionary_path = parent_path +'dictionary/'
image_path = parent_path + 'images/'
graph_path = parent_path + 'graph/'
contour_file = tree_path + filename + '.csv'
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
		self.value = None

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
			current.value = node
			traverse(j, node, current)

def preorder(tree, right_dictionary, parent_dictionary, label_dictionary, difference_dictionary):
	if(tree == None):
		return
	else:
		right_dictionary[index_map[tree.value]] = index_map[right_ancestor(tree)]
		label_dictionary[index_map[tree.value]] = scalars[tree.value]
		if tree.value != tree.parent.value:
			parent_dictionary[index_map[tree.value]] = index_map[tree.parent.value]
		else:
			parent_dictionary[index_map[tree.value]] = 0

		if (tree.left != None and tree.right != None):
			difference_dictionary[index_map[tree.value]] = max(abs(scalars[tree.right.value] - scalars[tree.value]), abs(scalars[tree.left.value] - scalars[tree.value]))
		elif (tree.left == None and tree.right != None):
			difference_dictionary[index_map[tree.value]] = abs(scalars[tree.right.value] - scalars[tree.value])
		elif (tree.left != None and tree.right == None):
			difference_dictionary[index_map[tree.value]] = abs(scalars[tree.left.value] - scalars[tree.value])
		else:
			difference_dictionary[index_map[tree.value]] = abs(scalars[tree.value])

		preorder(tree.left, right_dictionary, parent_dictionary, label_dictionary, difference_dictionary)
		preorder(tree.right, right_dictionary, parent_dictionary, label_dictionary, difference_dictionary)

def right_ancestor(tree):
	if(tree == None):
		return
	elif(tree.right == None):
		return tree.value
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
tree.value = root
tree.parent = tree
traverse(0, root, tree)

preorder(tree, r1, p1, l1, d1)

inv_map = {v: k for k, v in index_map.iteritems()}

graph_path = graph_path + filename + '.txt'
image_path = image_path + filename + '.png'
graph_file = open(graph_path, 'w')
graph_file.write('digraph {\n')
for i in index_map.keys():
	j = index_map[i]
	if p1[j] != 0:
		node1 = "\""+str(round(scalars[i],4)) + ' ('+str(j)+')' +"\""
		connector = ' -> '
		node2 = "\""+ str(round(scalars[inv_map[p1[j]]],4)) + ' ('+str(p1[j])+')' +"\""
		end = ';'

		line = node2 + connector + node1 + end +'\n'
		graph_file.write(line)

graph_file.write('}')
graph_file.close()

os.system('dot -Tpng '+ graph_path+' > '+image_path)

with open(dictionary_path + filename+'-right.txt', 'wb') as handle:
  pickle.dump(r1, handle)

with open(dictionary_path + filename+'-parent.txt', 'wb') as handle:
  pickle.dump(p1, handle)

with open(dictionary_path + filename+'-labels.txt', 'wb') as handle:
  pickle.dump(l1, handle)

with open(dictionary_path + filename+'-difference.txt', 'wb') as handle:
  pickle.dump(l1, handle)
