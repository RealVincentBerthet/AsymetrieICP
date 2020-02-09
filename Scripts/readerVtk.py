import vtk
import argparse
import rendering

parser = argparse.ArgumentParser()
parser.add_argument("-f","--filename", help="VTK file")
args = parser.parse_args()

if args.filename != None:
    print("VTK Loaded : "+str(args.filename))
else:
    print("No VTK loaded used -f argurment")
    quit()


# Initialize renderer
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.1, 0.2, 0.4)
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

rendering.AddVtkModel(renderer,args.filename)

interactor.Initialize()
render_window.Render()
interactor.Start()