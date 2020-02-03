import csv
import compute_plane
import vtk
import numpy as np
# Read CSV
# List of data
data = []
with open('./Data/ventricules.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        if (row[0]!="Points:0"):
            tmp = []
            for s in row:
                tmp.append(float(s))
            data.append(tmp)




def main():


    colors = vtk.vtkNamedColors()

    # Set the background color.
    colors.SetColor("BkgColor", [26, 51, 77, 255])

    # Create a plane
    planeSource = vtk.vtkPlaneSource()
    # planeSource.SetCenter(10, 10, 10)
    # planeSource.SetNormal(10, 2, 3)

    planeSource = compute_plane.compute_plane_test(planeSource, data)
    # planeSource.Update()
    #
    # plane = planeSource.GetOutput()
    #
    # # Create a mapper and actor
    # mapper = vtk.vtkPolyDataMapper()
    # mapper.SetInputData(plane)
    #
    # actor = vtk.vtkActor()
    # actor.SetMapper(mapper)
    # actor.GetProperty().SetColor(colors.GetColor3d("Cyan"))
    #
    # # Create a renderer, render window and interactor
    # renderer = vtk.vtkRenderer()
    # renderWindow = vtk.vtkRenderWindow()
    # renderWindow.SetWindowName("Plane")
    # renderWindow.AddRenderer(renderer)
    # renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    # renderWindowInteractor.SetRenderWindow(renderWindow)
    #
    # # Add the actors to the scene
    # renderer.AddActor(actor)
    # renderer.SetBackground(colors.GetColor3d("BkgColor"))
    #
    # # Render and interact
    # renderWindow.Render()
    # renderWindowInteractor.Start()


if __name__ == '__main__':
    main()