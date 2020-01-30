def compute_plane(planeSource, data):

    # Step 0 : Initialise plane

    planeSource.SetCenter(0, 0, 0)
    planeSource.SetNormal(1, 0, 0)

    # Step 1 :

    # Projection des points de l'autre coté du plan
    # distance de l'origine
    D =
    I = np.array([[1, 0, 0],
         [0, 1, 0],
         [0, 0, 1]])
    # normale
    N = np.array([1, 0, 0])
    # Projection
    y = (I - 2 * N * N.transpose()) * x + 2 * D * N