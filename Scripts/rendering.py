import vtk
import numpy as np
import algo
import time

def DrawAxes(renderer,length):
    axes = vtk.vtkAxesActor()
    axes.AxisLabelsOff()
    transform = vtk.vtkTransform()
    transform.Translate(0.0, 0.0, 0.0)
    axes.SetUserTransform(transform)
    axes.SetTotalLength(length)

    renderer.AddActor(axes)

def DrawPoint(data,renderer,colors,pointSize,oldActor=None):
    # Create the geometry of a point (the coordinate)
    points = vtk.vtkPoints()
    # Create the topology of the point (a vertex)
    vertices = vtk.vtkCellArray()

    color=colors.GetColor3d("Tomato")

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

    # Visualize
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(point)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(color)
    actor.GetProperty().SetPointSize(pointSize)
    if oldActor != None :
        renderer.RemoveActor(oldActor)
    renderer.AddActor(actor)

    return actor

def DrawPlan(renderer,color,center,normal,scaleFactor,oldActor=None):   
    # Create a plane
    planeSource = vtk.vtkPlaneSource()
    planeSource.SetCenter(0,0,0)
    planeSource.SetNormal(normal)
    planeSource.Update()
   
    # Scale plane
    scaleTransform=vtk.vtkTransform()
    scaleTransform.Scale((scaleFactor))
    scaleFilter = vtk.vtkTransformPolyDataFilter()
    scaleFilter.SetInputConnection(planeSource.GetOutputPort())
    scaleFilter.SetTransform(scaleTransform)
    scaleFilter.Update()

    # Translate plane
    translation = vtk.vtkTransform()
    translation.Translate(center)
    transformFilter = vtk.vtkTransformPolyDataFilter()
    transformFilter.SetInputConnection(scaleFilter.GetOutputPort())
    transformFilter.SetTransform(translation)
    transformFilter.Update()

    plane = transformFilter.GetOutput()

    # Create a mapper and actor
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(plane)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    #actor.GetProperty().SetRepresentationToWireframe() #plan unfilled
    actor.GetProperty().SetColor(color)
    actor.GetProperty().SetOpacity(0.5)

    if oldActor != None :
        renderer.RemoveActor(oldActor)
    renderer.AddActor(actor)

    return actor