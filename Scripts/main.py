import vtk
import csv
import argparse
import numpy as np
import algo
import os
import time
import rendering

def Get_csv_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--filename", help="CSV file use to draw cloud points")
    args = parser.parse_args()
    scaleFactor=(1,1,1)
    pointSize=1.0
    normal=(1,0,0)

    if args.filename != None:
        print("CSV Loaded : "+str(args.filename))
    else:
        print("No CSV loaded used -f argurment")
        quit()

    if os.path.basename(args.filename) == "ventricules.csv" :
        scaleFactor=(100,100,100)
        normal=(0,0,1)
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

    return data,normal,scaleFactor, pointSize

def main():
    start_time = time.time()
    data,normal,scaleFactor,pointSize=Get_csv_args()
    # Rendering
    colors = vtk.vtkNamedColors()
    colors.SetColor("BackgroundColor", [26, 51, 77, 255])
    colors.SetColor("Plane", [1.0, 0.0, 1.0,1.0])
    # Create a rendering window and renderer
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(colors.GetColor3d("BackgroundColor"))
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetSize(640, 480)
    renderWindow.SetFullScreen(1)
    renderWindow.SetBorders(1)
    renderWindow.AddRenderer(renderer)
    
    # Create a renderwindowinteractor
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)
    # dist[i] est la distance entre x[i] et son symétrique y[i], donc plus dist est élévé plus on met du rouge
    rendering.DrawAxes(renderer,(10,10,10))
    # Draw cloud point from CSV    
    rendering.DrawPoint(data,renderer,colors,pointSize)
    algo.compute_plane(data, normal,renderer,renderWindow,colors,pointSize,scaleFactor)
    print('time : '+str(round(time.time() - start_time))+' seconds')
    renderWindowInteractor.Start()





if __name__ == '__main__':
    main()
