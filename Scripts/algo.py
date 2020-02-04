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
    c = np.array([2, 3, 0])
    # normale
    n = np.array([2, 1, 0])
    n = n / np.linalg.norm(n)
    print('n')
    print(n)

    # Step 1 :

    # Projection des points de l'autre coté du plan
    # distance de l'origine
    o = np.array([0, 0, 0])

    d = np.linalg.norm(c-o)
    print('d')
    print(d)

    I3 = np.array([[1, 0, 0],
                 [0, 1, 0],
                 [0, 0, 1]])


    for iter in range(1):

        print("iter " + str(iter))

        # Projection
        sym = []
        for i in range(len(x)):
            tmp = (I3 - 2 * np.dot(np.array([n]).T,np.array([n]))) @ x[i] + 2 * d * n
            sym.append(tmp)

        sym = np.array(sym)
        print('sym')
        print(sym)

        # Associer chaque point symétrique au point le plus proche (kd-tree)
        association_list = []
        y = []
        xtmp = x
        sym_tmp = sym
        YourTreeName = scipy.spatial.cKDTree(sym_tmp, leafsize=100)
        for i in range(len(xtmp)):
            res = YourTreeName.query(xtmp[i])
            association_list.append(res)
        print('association')
        print(association_list)

        for i in range(len(association_list)):
            index = association_list[i][1]
            y.append(x[index])
        y = np.array(y)
        print('y')
        print(y)


        # Step 2 :

        # Calcul wi(ri)
        sigma = 1
        w = []
        for i in range(len(x)):
            # tmp = 1 / (sigma*sigma) * np.exp(-(association_list[i][0]*association_list[i][0]) / (sigma*sigma))
            # w.append(tmp)
            w.append(1)
        print('w')
        print(w)

        # Calcul xg et yg
        sumxg = np.array([0,0,0])
        for i in range(len(x)):
            sumxg = sumxg + w[i] * x[i]
        xg = sumxg / np.sum(w)

        sumyg = np.array([0,0,0])
        for i in range(len(y)):
            sumyg = sumyg + w[i] * y[i]
        yg = sumyg / np.sum(w)
        print('xg')
        print(xg)
        print('yg')
        print(yg)

        # Calcul A
        A = np.array([0,0,0])
        for i in range(len(x)):
            a1 = x[i]-xg + y[i]-yg
            a1 = np.array([a1])
            a2 = np.array(a1).T
            a3 = x[i]-y[i]
            a3 = np.array([a3])
            a4 = np.array(a3).T

            A = A + (w[i] * (a2 @ a1 - a4 @ a3))
        print("A")
        print((A))


        # Calcul n
        # n colinear with the eigenvector corresponding to the smallest eigenvalue of the matrix A

        eigvals, eigvecs = la.eig(A)
        minIndex = np.argmin(eigvals.real)
        n = eigvecs[:,minIndex]
        print('n new')
        print(n)

        # Calcul d
        d = 1/2 * (xg+yg) @ n
        d_vect = 1/2 * (xg+yg)
        print('d')
        print(d)
        print(d_vect)
        print("normal : " + str(n.tolist()))
        print("center : " + str(m.tolist()))




    return m.tolist(), n.tolist()