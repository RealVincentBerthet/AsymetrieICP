import numpy as np
import scipy.spatial
import scipy.linalg as la

def compute_plane(x):
    # Step 0 : Initialise plane

    # moyenne des points clouds pour trouver le centroid
    m = np.array([0,0,0])
    for i in range(len(x)):
       m = m + x[i]
    m = m / len(x)
    # print(m)

    c = m
    c = np.array([1, 0, 0])
    # normale
    n = np.array([1, 0, 0])
    n = n / np.linalg.norm(n)
    print(n)

    # Step 1 :

    # Projection des points de l'autre coté du plan
    # distance de l'origine
    o = np.array([0, 0, 0])

    d = np.linalg.norm(c-o)
    print(d)

    I3 = np.array([[1, 0, 0],
                 [0, 1, 0],
                 [0, 0, 1]])


    for iter in range(1):

        print("iter " + str(iter))

        # Projection
        y = []
        for i in range(len(x)):
            tmp = (I3 - 2 * np.dot(np.array([n]).T,np.array([n]))) @ x[i] + 2 * d * n
            # print(x[i])
            print(tmp)
            y.append(tmp)

        y = np.array(y)

        # Associer chaque point symétrique au point le plus proche (kd-tree)
        association_list = []
        xtmp = x
        ytmp = y
        YourTreeName = scipy.spatial.cKDTree(ytmp, leafsize=100)
        for i in range(len(xtmp)):
            res = YourTreeName.query(xtmp[i])
            # print((res[1]))
            association_list.append(res)
        print(association_list)

        # Step 2 :

        # Calcul wi(ri)
        # sigma = 5
        # w = []
        # for i in range(len(x)):
        #     tmp = 1 / sigma * np.exp(-(association_list[i][0]*association_list[i][0]) / (sigma*sigma))
        #     w.append(tmp)
        # print(w)
        w = 1

        # Calcul xg et yg
        sumxg = np.array([0,0,0])
        for i in range(len(x)):
            sumxg = sumxg + w * x[i]
        xg = sumxg / len(x)

        sumyg = np.array([0,0,0])
        for i in range(len(y)):
            sumyg = sumyg + w * y[i]
        yg = sumyg / len(y)
        print(xg)
        print(yg)

        # Calcul A
        # A = np.array(x.shape)
        A = np.array([0,0,0])
        for i in range(len(x)):
            a1 = x[i]-xg + y[i]-yg
            a2 = x[i]-y[i]

            A = A + (w * (a1 @ a1 - a2 @ a2))
        print((A))
        A3 = np.diag(A)
        print((A3))

        # Calcul n
        # n colinear with the eigenvector corresponding to the smallest eigenvalue of the matrix A

        eigvals, eigvecs = la.eig(A3)
        print(eigvecs)
        n = np.array([eigvecs[0][0], eigvecs[1][1], eigvecs[2][2]])



        # Calcul d
        d = 1/2 * (xg + yg) * n
        print(d)
        print("normal : "+str(n.tolist()))
        print("center : "+str(m.tolist()))


    return m.tolist(),n.tolist()