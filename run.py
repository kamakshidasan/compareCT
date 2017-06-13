import fileinput
import re
import os

def file_replace(fname, pat, s_after):
    # first, see if the pattern is even in the file.
    with open(fname) as f:
        if not any(re.search(pat, line) for line in f):
            return # pattern does not occur in file so we are done.

    # pattern is in the file, so perform replace operation.
    with open(fname) as f:
        out_fname = fname + ".tmp"
        out = open(out_fname, "w")
        for line in f:
            out.write(re.sub(pat, s_after, line))
        out.close()
        os.rename(out_fname, fname)

file_list = os.listdir('/home/raghavendra/Desktop/adhitya/data/')
file_list.insert(0, 'adhitya.vtk')

for i in range(1, len(file_list)):
	file_replace('/home/raghavendra/Desktop/adhitya/script.py', file_list[i-1], file_list[i])
	#os.system('paraview --script=script.py')
	os.system('python make-graph.py '+file_list[i])
	print i, file_list[i]
	
