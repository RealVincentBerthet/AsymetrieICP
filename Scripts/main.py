import vtk
import csv
import argparse
import numpy as np
import algo
import os

def Get_csv_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--filename", help="CSV file use to draw cloud points")
    args = parser.parse_args()
    scaleFactor=(1,1,1)
    pointSize=1.0

    if args.filename != None:
        print("CSV Loaded : "+str(args.filename))
    else:
        print("No CSV loaded used -f argurment")
        quit()

    if os.path.basename(args.filename) == "ventricules.csv" :
        scaleFactor=(100,100,100)
    elif os.path.basename(args.filename) == "Visage_symetrique.csv" :
        scaleFactor=(250,250,250)
    elif os.path.basename(args.filename) == "Visage_symetrique_decimated.csv" :
        scaleFactor=(250,250,250)
    elif os.path.basename(args.filename) == "Visage_symetrique_deforme.csv" :
        scaleFactor=(250,250,250)
    elif os.path.basename(args.filename) == "Visage_symetrique_deforme_decimated.csv" :
        scaleFactor=(250,250,250)
    elif os.path.basename(args.filename) == "Demo.csv" :
        scaleFactor=(30,30,30)
        pointSize=20

    #Load CSV Data    
    data = []
    with open(args.filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if (row[0]!="Points:0"):
                tmp=[]
                for s in row :
                    tmp.append(float(s))
                data.append(tmp)

    return data,scaleFactor, pointSize

def DrawAxes(renderer,length):
    axes = vtk.vtkAxesActor()
    axes.AxisLabelsOff()
    transform = vtk.vtkTransform()
    transform.Translate(0.0, 0.0, 0.0)
    axes.SetUserTransform(transform)
    axes.SetTotalLength(length)

    renderer.AddActor(axes)

def DrawPoint(data,renderer,color,pointSize):
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

    # Visualize
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(point)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(color)
    actor.GetProperty().SetPointSize(pointSize)

    renderer.AddActor(actor)

def DrawPlan(renderer,color,center,normal,scaleFactor):   
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
    actor.GetProperty().SetRepresentationToWireframe() #plan unfilled
    actor.GetProperty().SetColor(color)

    renderer.AddActor(actor)

def main():
    data,scaleFactor,pointSize=Get_csv_args()
    ## Rendering
    colors = vtk.vtkNamedColors()
    colors.SetColor("BackgroundColor", [26, 51, 77, 255])
    # Create a rendering window and renderer

    renderer = vtk.vtkRenderer()
    renderer.SetBackground(colors.GetColor3d("BackgroundColor"))
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    # Create a renderwindowinteractor
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)
    #endregion

    center,normal=algo.compute_plane(data)
    DrawPoint([center],renderer,colors.GetColor3d("DarkGreen"),10.0)
    DrawAxes(renderer,(5,5,5))
    # Draw cloud point from CSV    
    DrawPoint(data,renderer,colors.GetColor3d("Tomato"),pointSize)
    # Draw plane
    DrawPlan(renderer,colors.GetColor3d("Cyan"),center,normal,scaleFactor)
    # Render and interact
    renderWindow.Render()
    renderWindowInteractor.Start()





if __name__ == '__main__':
    main()
