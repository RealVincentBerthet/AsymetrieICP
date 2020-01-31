import numpy as np

def compute_plane_test(planeSource, data):

    # Step 0 : Initialise plane

    # moyenne des points clouds pour trouver le centroid
    m = np.array([0,0,0])
    for i in range(len(data)):
       m = m + data[i]
    m = m / len(data)
    # print(m)
    planeSource.SetNormal(1, 0, 0)
    planeSource.SetCenter(m)


    # Step 1 :

    # Projection des points de l'autre coté du plan
    # distance de l'origine
    # o = np.array([0, 0, 0])
    # c = np.array([0, 0, 0])
    # D = np.sqrt((c[0]-o[0])^2 + (c[0]-o[0])^2 + (c[0]-o[0])^2)
    # I = np.array([[1, 0, 0],
    #              [0, 1, 0],
    #              [0, 0, 1]])
    # # normale
    # N = np.array([1, 0, 0])
    # Projection
    # y = (I - 2 * N * N.transpose()) * x + 2 * D * N

    # Associer chaque point projeté au point le plus proche (kd-tree)


    return planeSource