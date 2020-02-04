import numpy as np
import scipy.spatial
import scipy.linalg as la

def compute_plane(x, n):

    x = np.array(x)
    # f = open("test.txt", "w")

    # Step 0 : Initialise plane

    # moyenne des points clouds pour trouver le centroid
    m = np.array([0,0,0])
    for i in range(len(x)):
       m = m + x[i]
    m = m / len(x)
    # print(m)

    c = m
    # c = np.array([1000, 0, 0])

    # normale
    n = np.array(n)
    n = n / np.linalg.norm(n)
    print('n')
    print(n)

    # distance de l'origine
    o = np.array([0, 0, 0])

    d = np.linalg.norm(c-o)
    print('d')
    print(d)

    I3 = np.array([[1, 0, 0],
                 [0, 1, 0],
                 [0, 0, 1]])

    n_prec = n + 1
    d_prec = d + 1
    iter=0
    # for iter in range(40):
    while abs(np.linalg.norm(n-n_prec)) > 0.01 or abs(d-d_prec) > 0.01 :

        n_prec = n
        d_prec = d

        iter = iter + 1
        print("iter " + str(iter))

        # Step 1 :

        # Projection des points de l'autre coté du plans
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

        dist = []
        for i in range(len(association_list)):
            index = association_list[i][1]
            y.append(x[index])
            dist.append(association_list[i][0])
        y = np.array(y)
        print('y')
        print(y)




        # Step 2 :

        # Calcul wi(ri)
        sigma = 10
        w = []
        for i in range(len(x)):
            # tmp = 1 / (sigma*sigma) * np.exp(-(dist[i]*dist[i]) / (sigma*sigma))
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
        d_vect = 1/2 * (xg+yg)
        d = d_vect @ n
        print('d')
        print(d)
        print(d_vect)
        print("normal : " + str(n.tolist()))
        print("center : " + str(d_vect.tolist()))

        # f.write(str(iter)+"\n")
        # f.write("normal : " + str(np.linalg.norm(n))+"\n")
        # f.write("center : " + str(d)+"\n")


    return d_vect.tolist(), n.tolist(), dist