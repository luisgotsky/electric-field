import numpy as np
import matplotlib.pyplot as plt

k = 9e-9
e0 = 8.85e-12

#Clase carga que pretende generalizar el concepto de carga puntual
#como una clase de Python.

class Carga(object):
    
    def __init__(self, carga, pos):
        
        self.carga = carga
        self.x = pos[0]
        self.y = pos[1]
        
    def dist(self, p):
        
        return ((self.x - p[0])**2 + (self.y - p[1])**2)**0.5
    
    def campo(self, p):
        
        return [k*self.carga*(p[0] - self.x)/self.dist(p)**3,
                k*self.carga*(p[1] - self.y)/self.dist(p)**3]
    
    def potencial(self, p):
        
        return k*self.carga/self.dist(p)
    
    def plotQ(self):
        
        if self.carga > 0:
            
            plt.scatter(self.y, self.x, c="b", s=200)
            
        else:
            
            plt.scatter(self.y, self.x, c="r", s=200)
    
#Dada una lista de objetos "carga" y un punto devuelve el campo eléctrico
#generado por las mismas en dicho punto
    
def campoE(Q, p):
    
    Ex, Ey = 0, 0
    
    for carga in Q:
        
        E = carga.campo(p)
        Ex += E[0]
        Ey += E[1]
        
    return Ex, Ey

#Dado un array de objetos "carga" y un punto devuelve el potencial
#generado por las mismas en dicho punto

def potV(Q, p):
    
    V = 0
    
    for carga in Q:
        
        V += carga.potencial(p)
        
    return V

#Dadas las arrays X, Y, Ex, Ey y la array de cargas genera una
#representación vectorial del campo eléctrico

def plotE(X, Y, Ex, Ey, Q, save=False, name=None):
    
    color = 2 * np.log(np.sqrt(Ex**2 + Ey**2))            
    plt.figure(figsize=(9, 9))
    
    for carga in Q:
        
        carga.plotQ()
        
    plt.streamplot(X, Y, Ey, Ex, color=color, linewidth=1, cmap=plt.cm.inferno,
                  density=2, arrowstyle='->', arrowsize=1.5)
    plt.xlabel("X (m)")
    plt.ylabel("Y (m)")
    
    if save: plt.savefig(name + ".png", dpi=1200)

#Idem pero con el potencial

def plotV(X, Y, V, save=False, name=None):
    
    x,y = np.meshgrid(X, Y)
    fig = plt.figure(figsize=(9, 6))
    ha = fig.add_subplot(111, projection='3d')
    ha.plot_surface(x, y, V, cmap="viridis")
    
    if save: plt.savefig(name + ".png", dpi=1200)
    
#Función que genera ambos campos a partir de la array de cargas y las
#arrays X e Y
    
def campos(X, Y, Q):
    
    n = len(X)
    Ex, Ey, V = np.zeros((n, n)), np.zeros((n, n)), np.zeros((n, n))
    
    for i in range(n):
        
        for j in range(n):
            
            p = [X[i], Y[j]]
            E = campoE(Q, p)
            Ex[i, j] += E[0]
            Ey[i, j] += E[1]
            V[i, j] += potV(Q, p)
            
    return Ex, Ey, V

#Resolución de la ecuación de Laplace por el método de jacobi para
#el potencial eléctrico

def jacobiV(X, Y, rho, h, tol=10**-6):
    
    n = len(X)
    V = np.ones((n, n))
    V2 = np.zeros((n, n))
    
    for i in range(1, n-1):
        
        for j in range(1, n-1):
            
            while abs(V2[i, j] - V[i, j]) > tol:
                
                V[i, j] = V2[i, j]
                V2[i, j] = 0.25*(V[i+1,j]+V[i-1,j]+V[i,j+1]+V[i,j-1]+
                                e0*rho[i,j]*h**2)
                
    return V2

#Esta función aproxima el valor del campo eléctrico a partir de un
#potencial dado

def aproxE(V):
    
    Ex, Ey = np.gradient(V)
            
    return Ex, Ey

#Esta función representará el perfil de la función potencial

def perfV(X, V, n, save=False, name=None):
    
    l = len(X)
    indexes = [i for i in range(l)]
    i = indexes[l//2:l//2+n:] + indexes[l//2:l//2-n:]
    
    plt.figure(figsize=(9, 6))
    
    for x in i:
        
        plt.plot(X, V[:,x])
        
    plt.xlabel("X (m)")
    plt.ylabel("Potencial (V)")
        
    if save: plt.savefig(name + ".png", dpi=1200)

def main():
        
    n = 36 #Finura del teselado del espacio
    L = 2 #Cuadrado de [-L, L]
    X, Y = np.linspace(-L, L, n), np.linspace(-L, L, n) #Espacio
    h = X[1]-X[0] #Distancia entre puntos
    
    #Hay que definir la array de cargas, en este caso un dipolo. También
    #la matriz de densidad de carga
    
    q1, q2 = Carga(0.5, [-1, 0]), Carga(-0.5, [1, 0])
    Q = [q1, q2]
    rho = np.zeros((n, n))
    rho[n//4, n//2] = 1e60
    rho[3*n//4, n//2] = -1e60
    
    #Calculamos campo y potencial
    
    Ex, Ey, V = campos(X, Y, Q)
    VLap = jacobiV(X, Y, rho, h)
    ELapx, ELapy = aproxE(VLap)
    
    #Graficamos
        
    plotE(X, Y, Ex, Ey, Q)
    plotV(X, Y, V)
    plotV(X, Y, VLap)
    perfV(X, V, 20)
    perfV(X, VLap, 20)

if __name__ == "__main__":
    
    main()