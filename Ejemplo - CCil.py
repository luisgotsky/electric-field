import CampoE.CodigoEM as em
import numpy as np

n = 100
nt = 200
L = 2
thetas = np.linspace(0, 2*np.pi, nt)
Q = []
X, Y = np.linspace(-L, L, n), np.linspace(-L, L, n)

for i in thetas:
    
    Q.append(em.Carga(1e-9, [0.5*np.cos(i), 0.5*np.sin(i)]))
    Q.append(em.Carga(-1e-9, [1.5*np.cos(i), 1.5*np.sin(i)]))
    
Ex, Ey, V = em.campos(X, Y, Q)

em.plotV(X, Y, V, save=True, name="Potencial - Doble espira")
em.plotE(X, Y, Ex, Ey, Q, save=False, name="Campo - Doble espira")

rho = np.zeros((n, n))
Qt = 1e60

for i in range(n):
    
    for j in range(n):
        
        d = np.sqrt(X[i]**2 + Y[j]**2)
        
        if 0.45 <= d <= 0.55:
            
            rho[i, j] = Qt
            
        elif 1.45 <= d <= 1.55:
            
            rho[i, j] = -Qt

VLap = em.jacobiV(X, Y, rho, X[1]-X[0])
em.plotV(X, Y, VLap, save=True, name="Potencial Laplace - Doble espira")
em.perfV(X, V, 5, save=True, name="Potencial Perfil - Doble espira")
em.perfV(X, VLap, 5, save=True, name="Laplace Perfil - Doble espira")

#Resultados teóricos

def espira(x, y):
    
    sig = 1
    rho = np.sqrt(x**2 + y**2)
    a = 0.5
    
    Ex = (sig*a/rho**2)*x
    Ey = (sig*a/rho**2)*y
    
    if rho <= 0.5 or rho >= 1.5:
        
        Ex, Ey = 0, 0
    
    return Ex, Ey

Ex, Ey = np.zeros((n, n)), np.zeros((n, n))

for i in range(n):
    
    for j in range(n):
        
        E = espira(X[i], Y[j])
        Ex[i, j] = E[0]
        Ey[i, j] = E[1]
        
em.plotE(X, Y, Ex, Ey, Q, save=False, name="Campo teórico - Doble Espira")