import numpy as np
import matplotlib.pyplot as plt
import numpy.random as npr

def simulate_geometric_random_walk(S0, T=2, N=1000, mu=0.1, sigma=0.05):
    dt = T/N
    t = np.linspace(0, T, N)
    # N(0, 1)
    W = npr.standard_normal(size=N)
    # avec N(0, dt) = sqrt(dt) * N(0,1)
    W = np.cumsum(np.sqrt(dt) * W)
    # dF(S)
    X = (mu - 0.5 * sigma**2)*t + sigma * W
    # S(t)
    S = S0*np.exp(X)
    return t, S

def plot_simulation(t, S):
    plt.plot(t, S, lw=0.5)
    plt.xlabel('time')
    plt.ylabel("S(t), Stock Price")
    plt.title('Geometric Brownian Motion')
    # plt.show()

# comprendre mu
def plot_simulations_monte_carlo(S0, M, N=1000):
    plt.figure(figsize=(10,6))
    S1 = np.zeros((M, N))

    for i in range(M):

        t, S1[i,:] = simulate_geometric_random_walk(10)
        plot_simulation(t, S1[i,:])

    plt.plot(t, np.mean(S1, axis=0), 'k', label='Moyenne des trajectoires')
    plt.title('Simulation de M trajectoires de $S(t)$')
    plt.xlabel('Temps (t)')
    plt.ylabel('Prix $S(t)$')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    t, S = simulate_geometric_random_walk(10)
    plot_simulation(t, S)
    plot_simulations_mu(10, 10)