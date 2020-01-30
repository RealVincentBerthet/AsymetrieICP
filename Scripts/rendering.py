import vtk
import csv
import argparse

def get_csv_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--filename", help="CSV file use to draw cloud points")
    args = parser.parse_args()
    return args.filename

def DrawPoint(p,renderer,color):
    # Create the geometry of a point (the coordinate)
    points = vtk.vtkPoints()
    
    # Create the topology of the point (a vertex)
    vertices = vtk.vtkCellArray()
    # We need an an array of point id's for InsertNextCell.
    pid = [0]
    pid[0] = points.InsertNextPoint(p)
    vertices.InsertNextCell(1, pid)

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
    actor.GetProperty().SetPointSize(20)

    renderer.AddActor(actor)

def main():
    #region Initialization
    #Get filename from args
    filename=get_csv_args()
    if filename != None:
        print("CSV Loaded : "+str(filename))
    else:
        print("No CSV loaded used -f argurment")
        return
    #Load CSV Data    
    data = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if (row[0]!="Points:0"):
                data.append(row)
    
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

    # Draw cloud point from CSV
    DrawPoint([1.0, 2.0, 3.0],renderer,colors.GetColor3d("Tomato"))
    DrawPoint([2.0, 2.0, 3.0],renderer,colors.GetColor3d("DarkGreen"))

    # Render and interact
    renderWindow.Render()
    renderWindowInteractor.Start()





if __name__ == '__main__':
    main()
