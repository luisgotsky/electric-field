import numpy as np
import CampoE.CodigoEM as em

n = 100
L = 2
X, Y = np.linspace(-L, L, n), np.linspace(-L, L, n)
Q = []
rho = np.zeros((n, n))

for j in range(n):
        
    Q.append(em.Carga(0.5, [-2, Y[j]]))
    Q.append(em.Carga(-0.5, [2, Y[j]]))
    
Ex, Ey, V = em.campos(X, Y, Q)
em.plotE(X, Y, Ex, Ey, Q, save=False, name="Campo - Placas paralelas")
em.plotV(X, Y, V, save=False, name="Potencial - Placas paralelas")

rho = np.zeros((n, n))

for i in range(n):
    
    rho[1, i] = -1e50
    rho[n-2, i] = 1e50
    
VLap = em.jacobiV(X, Y, rho, X[1]-X[0])
em.plotV(X, Y, VLap, save=True, name="Poisson - Placas Paralelas")
em.perfV(X, V, 5, save=False, name="Potencial Perfil - Placas paralelas")
em.perfV(X, VLap, 5, save=True, name="Poisson perfil - Placas paralelas")
Exl, Eyl = em.aproxE(VLap)
em.plotE(X, Y, Exl, Eyl, Q)