#### import the simple module from the paraview
from paraview.simple import *
import os
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'Legacy VTK Reader'
tv_34vtk = LegacyVTKReader(FileNames=['/home/raghavendra/Desktop/blobdata/Data/tv_108.vtk'])

# get active view
spreadSheetView1 = GetActiveViewOrCreate('SpreadSheetView')
# uncomment following to set a specific view size
# spreadSheetView1.ViewSize = [400, 400]

# show data in view
tv_34vtkDisplay = Show(tv_34vtk, spreadSheetView1)

# create a new 'TTK ContourForests'
tTKContourForests1 = TTKContourForests(Input=tv_34vtk)

# Properties modified on tTKContourForests1
tTKContourForests1.TreeType = 'Join Tree'
tTKContourForests1.ArcSampling = 0
tTKContourForests1.ArcSmoothing = 100.0

# show data in view
tTKContourForests1Display = Show(tTKContourForests1, spreadSheetView1)

# hide data in view
Hide(tv_34vtk, spreadSheetView1)

# show data in view
tTKContourForests1Display_1 = Show(OutputPort(tTKContourForests1, 1), spreadSheetView1)

# hide data in view
Hide(tv_34vtk, spreadSheetView1)

# show data in view
tTKContourForests1Display_2 = Show(OutputPort(tTKContourForests1, 2), spreadSheetView1)

# hide data in view
Hide(tv_34vtk, spreadSheetView1)

# find view
renderView1 = FindViewOrCreate('RenderView1', viewtype='RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1414, 415]

# set active view
SetActiveView(renderView1)

# set active source
SetActiveSource(tTKContourForests1)

# show data in view
tTKContourForests1Display_3 = Show(OutputPort(tTKContourForests1, 1), renderView1)

# reset view to fit data
renderView1.ResetCamera()

# set active view
SetActiveView(spreadSheetView1)

# show data in view
tTKContourForests1Display = Show(tTKContourForests1, spreadSheetView1)

# export view
ExportView('/home/raghavendra/Desktop/blobdata/Join-Trees/nodes-108.csv', view=spreadSheetView1, FilterColumnsByVisibility=1)

# show data in view
tTKContourForests1Display_1 = Show(OutputPort(tTKContourForests1, 1), spreadSheetView1)

# export view
ExportView('/home/raghavendra/Desktop/blobdata/Join-Trees/arcs-108.csv', view=spreadSheetView1, FilterColumnsByVisibility=1)

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [-79.49077914356731, 250.35076883508685, 207.2853897453842]
renderView1.CameraViewUp = [-0.9654076344631878, -0.1112974461581046, -0.2357985958373713]
renderView1.CameraParallelScale = 86.60254037844386

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
print 'Done :)'
os._exit(0)
