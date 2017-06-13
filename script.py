#### import the simple module from the paraview
from paraview.simple import *
import os, csv

paraview.simple._DisableFirstRenderCameraReset()

full_file_name = 'adhitya.vtk'
parent_path = '/home/raghavendra/Desktop/adhitya/'
data_path = parent_path + 'data/'
file_path = data_path + full_file_name
intermediate_path = parent_path + 'intermediate/'
file_name = os.path.splitext(os.path.basename(file_path))[0]
nodes_path = intermediate_path +'nodes-'+file_name+'.csv'
arcs_path = intermediate_path +'arcs-'+file_name+'.csv'

vtkFile = LegacyVTKReader(FileNames=[file_path])

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1414, 860]

# show data in view
vtkFileDisplay = Show(vtkFile, renderView1)

# reset view to fit data
renderView1.ResetCamera()

# show color bar/color legend
vtkFileDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'magnitude'
magnitudeLUT = GetColorTransferFunction('magnitude')

# get opacity transfer function/opacity map for 'magnitude'
magnitudePWF = GetOpacityTransferFunction('magnitude')

# create a new 'TTK ContourForests'
tTKContourForests1 = TTKContourForests(Input=vtkFile)

# Properties modified on tTKContourForests1
tTKContourForests1.TreeType = 'Join Tree'
tTKContourForests1.ArcSampling = 0
tTKContourForests1.ArcSmoothing = 100.0

# show data in view
tTKContourForests1Display = Show(tTKContourForests1, renderView1)

# hide data in view
Hide(vtkFile, renderView1)

# show color bar/color legend
tTKContourForests1Display.SetScalarBarVisibility(renderView1, True)

# show data in view
tTKContourForests1Display_1 = Show(OutputPort(tTKContourForests1, 1), renderView1)

# hide data in view
Hide(vtkFile, renderView1)

# show color bar/color legend
tTKContourForests1Display_1.SetScalarBarVisibility(renderView1, True)

# show data in view
tTKContourForests1Display_2 = Show(OutputPort(tTKContourForests1, 2), renderView1)

# hide data in view
Hide(vtkFile, renderView1)

# show color bar/color legend
tTKContourForests1Display_2.SetScalarBarVisibility(renderView1, True)

# get layout
layout1 = GetLayout()

# split cell
layout1.SplitVertical(0, 0.5)

# set active view
SetActiveView(None)

# Create a new 'SpreadSheet View'
spreadSheetView1 = CreateView('SpreadSheetView')
spreadSheetView1.ColumnToSort = ''
spreadSheetView1.BlockSize = 1024L
# uncomment following to set a specific view size
# spreadSheetView1.ViewSize = [400, 400]

# place view in the layout
layout1.AssignView(2, spreadSheetView1)

# show data in view
tTKContourForests1Display_3 = Show(tTKContourForests1, spreadSheetView1)

# export view
ExportView(nodes_path, view=spreadSheetView1, FilterColumnsByVisibility=1)

# show data in view
tTKContourForests1Display_4 = Show(OutputPort(tTKContourForests1, 1), spreadSheetView1)

# export view
ExportView(arcs_path, view=spreadSheetView1, FilterColumnsByVisibility=1)

scalars = {}
nodes = []

bounds = vtkFile.GetDataInformation().GetBounds()
[x_min,x_max,y_min,y_max,z_min,z_max]=bounds

x_dim = int(x_max - x_min + 1)
y_dim = int(y_max - y_min + 1)
z_dim = int(z_max - z_min + 1)

with open(nodes_path, 'rb') as csvfile:
	csvfile.readline() 
	spamreader = csv.reader(csvfile, delimiter=' ')
	for r in spamreader:
		row = r[0].split(',')
		scalars[int(row[2])] = float(row[0])

with open(arcs_path, 'rb') as csvfile:
	csvfile.readline()
	spamreader = csv.reader(csvfile, delimiter=' ')
	for r in spamreader:
		row = r[0].split(',')
		x = int(row[3]) + int(abs(x_min))
		y = int(row[4]) + int(abs(y_min))
		z = int(row[5]) + int(abs(z_min))
		index = z * x_dim * y_dim + y * x_dim + x
		nodes.append(index)

with open(parent_path+'trees/'+file_name +'.csv', 'w') as csvfile:
	fieldnames = ['Node:0', 'Node:1', 'Scalar:0', 'Scalar:1']
	writer = csv.writer(csvfile, delimiter=',')
	writer.writerow(fieldnames)	
	for index in range(0,len(nodes),2):
		writer.writerow([nodes[index], nodes[index+1], scalars[nodes[index]], scalars[nodes[index+1]]])

print 'Done! :)'
os._exit(0)
