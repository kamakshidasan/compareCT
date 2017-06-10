import csv, sys

filename = sys.argv[1]
parent_path = '/home/nagarjun/Desktop/Raghavendra/' 
nodes_file = parent_path + 'nodes-'+ filename + '.csv'
arcs_file = parent_path + 'arcs-'+ filename + '.csv'
scalars = {}
nodes = []

with open(nodes_file, 'rb') as csvfile:
	csvfile.readline() 
	spamreader = csv.reader(csvfile, delimiter=' ')
	for r in spamreader:
		row = r[0].split(',')
		scalars[int(row[2])] = float(row[0])

with open(arcs_file, 'rb') as csvfile:
	csvfile.readline()
	spamreader = csv.reader(csvfile, delimiter=' ')
	for r in spamreader:
		row = r[0].split(',')
		x = int(row[3]) + 50
		y = int(row[4]) + 50
		z = int(row[5]) + 50
		index = z * 101 * 101 + y * 101 + x
		nodes.append(index)

with open(parent_path + filename +'.csv', 'w') as csvfile:
	fieldnames = ['Node:0', 'Node:1', 'Scalar:0', 'Scalar:1']
	writer = csv.writer(csvfile, delimiter=',')
	writer.writerow(fieldnames)	
	for index in range(0,len(nodes),2):
		writer.writerow([nodes[index], nodes[index+1], scalars[nodes[index]], scalars[nodes[index+1]]])

contour_path = parent_path + 'tree-'+ filename + '.txt'
contour_file = open(contour_path, 'w')
contour_file.write('graph {\n')
for index in range(0,len(nodes),2):
	line = str(nodes[index]) + ' -- ' + str(nodes[index+1])
	contour_file.write(line)
	contour_file.write('\n')

contour_file.write('}')
contour_file.close()
