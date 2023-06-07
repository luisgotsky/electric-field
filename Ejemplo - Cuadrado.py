import numpy as np
import CampoE.CodigoEM as em

n = 30L = 2
X, Y = np.linspace(-L, L, n), np.linspace(-L, L, n)
Q = []
rho = np.zeros((n, n))

for j in range(n):
        
    Q.append(em.Carga(0.5, [-2, Y[j]]))
    Q.append(em.Carga(-0.5, [2, Y[j]]))
    Q.append(em.Carga(0.5, [X[j], -2]))
    Q.append(em.Carga(-0.5, [X[j], 2]))
    
Ex, Ey, V = em.campos(X, Y, Q)
em.plotE(X, Y, Ex, Ey, Q, save=True, name="Cuadrado - Campo")
em.plotV(X, Y, V, save=True, name="Cuadrado - Potencial")
em.perfV(X, V, 20, save=True, name="Cuadrado - Perfiles")