import csv
import vtk

# Read CSV
# List of data
data = []
with open('./Data/ventricules.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        if (row[0]!="Points:0"):
            data.append(row)




def main():
    colors = vtk.vtkNamedColors()

    # Set the background color.
    colors.SetColor("BkgColor", [26, 51, 77, 255])

    # Create a plane
    planeSource = vtk.vtkPlaneSource()
    planeSource.SetCenter(1.0, 0.0, 0.0)
    planeSource.SetNormal(1.0, 0.0, 1.0)
    planeSource.Update()

    plane = planeSource.GetOutput()

    # Create a mapper and actor
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(plane)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(colors.GetColor3d("Cyan"))

    # Create a renderer, render window and interactor
    renderer = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetWindowName("Plane")
    renderWindow.AddRenderer(renderer)
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    # Add the actors to the scene
    renderer.AddActor(actor)
    renderer.SetBackground(colors.GetColor3d("BkgColor"))

    # Render and interact
    renderWindow.Render()
    renderWindowInteractor.Start()


if __name__ == '__main__':
    main()