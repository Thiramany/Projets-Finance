import numpy as np
import numpy.random as npr
import matplotlib.pyplot as plt

def wiener_process(dt=0.1, x0=0, n=100000):
    # W mouvement brownien ssi
    #   - W(0) = 0
    #   - accroissements indépendants et suivent N(0,dt)
    #   - continuité des sauts
    W = np.zeros(n+1)
    # t = 0, 1, 2, ..., n
    t = np.linspace(x0, n, n+1)
    #! N(0,dt) = sqrt(dt) * N(0,1)
    # génerer des accroissement (somme cumulée) indépendants suivant N(0,dt) n fois
    #! npr.normal(loc, standard deviation!!, samples)
    W[1:n+1] = np.cumsum(npr.normal(0,np.sqrt(dt), n))
    return t, W


def plot_process(t, W):
    plt.plot(t, W)
    plt.xlabel('time')
    plt.ylabel('Wiener Process W(t)')
    plt.title('Wiener Process')
    print(np.mean(W))
    plt.show()

if __name__=='__main__':
    time, W = wiener_process()
    plot_process(time, W)
