import vtk
import numpy as np

def AddLog(renderer,text,fontSize,oldActor=None):
    colors = vtk.vtkNamedColors()

    # Create a text actor.
    actor = vtk.vtkTextActor()
    actor.SetInput(text)
    actor.GetTextProperty().SetFontFamilyToArial()
    actor.GetTextProperty().SetFontSize(fontSize)
    actor.GetTextProperty().ShadowOn()
    actor.GetTextProperty().SetShadowOffset(1, 1)
    actor.GetTextProperty().SetColor(colors.GetColor3d("Cornsilk"))
    actor.SetDisplayPosition(10, 10)

    if oldActor != None :
        renderer.RemoveActor(oldActor)
    renderer.AddActor(actor)

    return actor


def AddVtkModel(renderer,vtkFilePath,opacity=1.0):
    if vtkFilePath != None :
        reader = vtk.vtkPolyDataReader()

        reader.SetFileName(vtkFilePath)
        reader.Update()
        
        mapper = vtk.vtkDataSetMapper()
        mapper.SetInputData(reader.GetOutput())
        actor = vtk.vtkActor()
        actor.GetProperty().SetOpacity(opacity)
        actor.SetMapper(mapper)
 
        renderer.AddActor(actor)
    else :
        print("No vtk model added")

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
    pointData = vtk.vtkPolyData()

    # Set the points and vertices we created as the geometry and topology of the polydata
    pointData.SetPoints(points)
    pointData.SetVerts(vertices)

    # Visualize
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(pointData)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(color)
    actor.GetProperty().SetPointSize(pointSize)

    if oldActor != None :
        renderer.RemoveActor(oldActor)
    renderer.AddActor(actor)

    return actor,pointData

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

def DrawPointDistance(renderer,renderWindowInteractor,distance,data):
    # Create the color map
    minD=min(distance)
    print("Distance min : "+str(minD))
    maxD=max(distance)
    print("Distance max : "+str(maxD))
    colorLookupTable = vtk.vtkLookupTable()
    colorLookupTable.SetTableRange(minD, maxD)
    colorLookupTable.SetHueRange(0.667, 0.0)
    colorLookupTable.Build()
    
    # Polydata
    points = vtk.vtkPoints()
    vertices = vtk.vtkCellArray()
    for p in data :
        id = points.InsertNextPoint(p)
        vertices.InsertNextCell(1)
        vertices.InsertCellPoint(id)

    pointPolyData = vtk.vtkPolyData()
    pointPolyData.SetPoints(points)
    pointPolyData.SetVerts(vertices)
    
    # Generate colors for each points
    colors = vtk.vtkUnsignedCharArray()
    colors.SetNumberOfComponents(3)
    colors.SetName("Colors")

    for i in range (pointPolyData.GetNumberOfPoints()): 
        p= 3*[0.0]
        pointPolyData.GetPoint(i,p)
        dcolor = 3*[0.0]
        colorLookupTable.GetColor(distance[i], dcolor)
        color=3*[0.0]
        for j in range(0,3):
          color[j] = int(255.0 * dcolor[j])
          
        colors.InsertNextTypedTuple(color)

    pointPolyData.GetPointData().SetScalars(colors)

    # Create a mapper and actor
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(pointPolyData)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # create the scalar_bar
    scalar_bar = vtk.vtkScalarBarActor()
    scalar_bar.SetMaximumWidthInPixels(50)
    scalar_bar.SetOrientationToHorizontal()
    scalar_bar.SetLookupTable(colorLookupTable)
    scalar_bar.SetTitle("Distance")
    # create the scalar_bar_widget
    scalar_bar_widget = vtk.vtkScalarBarWidget()
    scalar_bar_widget.SetInteractor(renderWindowInteractor)
    scalar_bar_widget.SetScalarBarActor(scalar_bar)
    scalar_bar_widget.On()

    # Add the actor to the scene
    renderer.AddActor(actor)
    renderWindowInteractor.Start()
    






