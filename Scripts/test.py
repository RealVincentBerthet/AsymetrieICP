#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# by Panos Mavrogiorgos, email : pmav99 >a< gmail

import vtk
import numpy as np
import csv

# Create a custom lut. The lut is used both at the mapper and at the
# scalar_bar
lut = vtk.vtkLookupTable()
lut.Build()
 



# Read the source file.
#reader = vtk.vtkPolyDataReader()
#reader.SetFileName(file_name)
#reader.Update() # Needed because of GetScalarRange

data=[[10.0, 10.0, 0.0], [10.0, 12.0, 0.0], [14.0, 12.0, 0.0], [-10.0, 11.0, 0.0], [-10.0, 12.0, 0.0], [-14.0, 12.0, 0.0]]
# Create the geometry of a point (the coordinate)
points = vtk.vtkPoints()

# Create the topology of the point (a vertex)
vertices = vtk.vtkCellArray()

# We need an an array of point id's for InsertNextCell.
for p in data :
    id = points.InsertNextPoint(p)
    vertices.InsertNextCell(1)
    vertices.InsertCellPoint(id)

# Create a polydata object
point = vtk.vtkPolyData()

# Set the points and vertices we created as the geometry and topology of the polydata
point.SetPoints(points)
point.SetVerts(vertices)


#output = reader.GetOutput()
output=point
scalar_range = output.GetScalarRange() 


print('scalar range : '+str(scalar_range))
mapper = vtk.vtkDataSetMapper()

mapper.SetInputData(output)
mapper.SetScalarRange(scalar_range)
mapper.SetLookupTable(lut)
 
actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetPointSize(20)
 
renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)
 
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
 
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
 
# create the scalar_bar
scalar_bar = vtk.vtkScalarBarActor()
scalar_bar.SetOrientationToHorizontal()
scalar_bar.SetLookupTable(lut)

# create the scalar_bar_widget
scalar_bar_widget = vtk.vtkScalarBarWidget()
scalar_bar_widget.SetInteractor(interactor)
scalar_bar_widget.SetScalarBarActor(scalar_bar)
scalar_bar_widget.On()
 
interactor.Initialize()
render_window.Render()
interactor.Start()