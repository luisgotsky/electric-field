import numpy as np
import CampoE.CodigoEM as em

n = 100
L = 2
X, Y = np.linspace(-L, L, n), np.linspace(-L, L, n)
Q = []
rho = np.zeros((n, n))

for j in range(n):
    
    if X[j] < 1.5 and Y[j] < 1.5 and X[j] > -1.5 and Y[j] > -1.5:
        
        Q.append(em.Carga(6*0.5/4, [-1.5, Y[j]]))
        Q.append(em.Carga(6*0.5/4, [1.5, Y[j]]))
        Q.append(em.Carga(6*0.5/4, [X[j], -1.5]))
        Q.append(em.Carga(6*0.5/4, [X[j], 1.5]))
    
    if X[j] < 1 and Y[j] < 1 and X[j] > -1 and Y[j] > -1:
    
        Q.append(em.Carga(-0.5, [-1, Y[j]]))
        Q.append(em.Carga(-0.5, [1, Y[j]]))
        Q.append(em.Carga(-0.5, [X[j], -1]))
        Q.append(em.Carga(-0.5, [X[j], 1]))
    
Ex, Ey, V = em.campos(X, Y, Q)
em.plotE(X, Y, Ex, Ey, Q, save=True, name="Campo eléctrico - Condensador cuadrado")
em.plotV(X, Y, V, save=True, name="Potencial - Condensador cuadrado")
em.perfV(X, V, 20, save=True, name="Perfiles - Condensador cuadrado")