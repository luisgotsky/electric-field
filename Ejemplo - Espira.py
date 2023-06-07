import numpy as np
import CampoE.CodigoEM as em

n = 40
nt = 80
L = 2
X, Y = np.linspace(-L, L, n), np.linspace(-L, L, n)
thetas = np.linspace(0, 2*np.pi, nt)
Q = []

for i in thetas:
    
    Q.append(em.Carga(1e-9, [0.5*np.cos(i), 0.5*np.sin(i)]))
    
Ex, Ey, V = em.campos(X, Y, Q)

em.plotV(X, Y, V, save=False, name="Potencial Espira")
em.plotE(X, Y, Ex, Ey, Q, save=False, name="Campo Espira")

rho = np.zeros((n, n))
Qt = 1e40

for i in range(n):
    
    for j in range(n):
        
        d = np.sqrt(X[i]**2 + Y[j]**2)
        
        if 0.45 <= d <= 0.55:
            
            rho[i, j] = Qt
            
VLap = em.jacobiV(X, Y, rho, X[1]-X[0])
em.plotV(X, Y, VLap, save=False, name="Laplace espira")
em.perfV(X, V, 5, save=False, name="Potencial perfil Espira")
em.perfV(X, VLap, 5, save=False, name="Laplace perfil espira")

#Resultados teóricos

def espira(x, y):
    
    sig = 1
    rho = np.sqrt(x**2 + y**2)
    a = 0.5
    
    Ex = (sig*a/rho**2)*x
    Ey = (sig*a/rho**2)*y
    
    if rho <= 0.5:
        
        Ex, Ey = 0, 0
    
    return Ex, Ey

Ex, Ey = np.zeros((n, n)), np.zeros((n, n))

for i in range(n):
    
    for j in range(n):
        
        E = espira(X[i], Y[j])
        Ex[i, j] = E[0]
        Ey[i, j] = E[1]
        
em.plotE(X, Y, Ex, Ey, Q, save=False, name="Campo teórico Espira")