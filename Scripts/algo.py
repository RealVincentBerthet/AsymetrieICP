import numpy as np
import scipy.spatial
import scipy.linalg as la
import rendering
import time

def compute_plane(x, n,renderer,renderWindow,colors,pointSize,scaleFactor,epsilon=0.01):
    start_time = time.time()
    x = np.array(x)
    # Step 0 : Initialise plane
    # moyenne des points clouds pour trouver le centroid
    m = np.array([0,0,0])
    for i in range(len(x)):
       m = m + x[i]
    m = m / len(x)

    # normale
    n = np.array(n)
    n = n / np.linalg.norm(n)

    # distance de l'origine
    o = np.array([0, 0, 0])
    d = np.linalg.norm(m-o)

    I3 = np.array([[1, 0, 0],
                 [0, 1, 0],
                 [0, 0, 1]])

    n_prec = n + 1
    d_prec = d + 1
    iter=0
    oldPlane=None
    oldCenter=None
    oldLog=None
    while abs(np.linalg.norm(n-n_prec)) > epsilon or abs(d-d_prec) > epsilon :
        n_prec = n
        d_prec = d

        iter = iter + 1

        # Step 1 :

        # Projection des points de l'autre coté du plans
        sym = []
        for i in range(len(x)):
            tmp = (I3 - 2 * np.dot(np.array([n]).T,np.array([n]))) @ x[i] + 2 * d * n
            sym.append(tmp)

        sym = np.array(sym)

        # Associer chaque point symétrique au point le plus proche (kd-tree)
        association_list = []
        y = []
        xtmp = x
        sym_tmp = sym
        YourTreeName = scipy.spatial.cKDTree(sym_tmp, leafsize=100)
        for i in range(len(xtmp)):
            res = YourTreeName.query(xtmp[i])
            association_list.append(res)

        dist = []
        for i in range(len(association_list)):
            index = association_list[i][1]
            y.append(x[index])
            dist.append(association_list[i][0])
        y = np.array(y)

        # Step 2 :
        # Calcul wi(ri)
        sigma = 10
        w = []
        for i in range(len(x)):
            # tmp = 1 / (sigma*sigma) * np.exp(-(dist[i]*dist[i]) / (sigma*sigma))
            # w.append(tmp)
            w.append(1)

        # Calcul xg et yg
        sumxg = np.array([0,0,0])
        for i in range(len(x)):
            sumxg = sumxg + w[i] * x[i]
        xg = sumxg / np.sum(w)

        sumyg = np.array([0,0,0])
        for i in range(len(y)):
            sumyg = sumyg + w[i] * y[i]
        yg = sumyg / np.sum(w)

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

        # Calcul n
        # n colinear with the eigenvector corresponding to the smallest eigenvalue of the matrix A

        eigvals, eigvecs = la.eig(A)
        minIndex = np.argmin(eigvals.real)
        n = eigvecs[:,minIndex]

        # Calcul d
        d_vect = 1/2 * (xg+yg)
        d = d_vect @ n
        print("iter " + str(iter))
        print("normal : " + str(n.tolist()))
        print("center : " + str(d_vect.tolist()))

        # Draw
        #oldCenter=rendering.DrawPoint([d_vect],renderer,colors,5,oldCenter)
        oldPlane=rendering.DrawPlan(renderer,colors.GetColor3d("Plane"),d_vect,n,scaleFactor,oldPlane)

        temp=round(time.time() - start_time)
        hours = temp//3600
        temp = temp - 3600*hours
        minutes = temp//60
        seconds = temp - 60*minutes
        if seconds < 10 :
            seconds="0"+str(seconds)

        text="Iteration "+str(iter)+"\nNormal "+str(n.tolist())+"\nCenter "+str(d_vect.tolist())+"\nTime : "+str(minutes)+':'+str(seconds)
        oldLog=rendering.AddLog(renderer,text,14,oldLog)
        renderWindow.Render()

    return dist 