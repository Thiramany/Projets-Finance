import numpy as np
import numpy.random as npr
import matplotlib.pyplot as plt
import pandas as pd

NB_SIMULATIONS = 1000

def stock_price_monte_carlo(S0, mu, sigma, N=252):
    resultats = []

    for _ in range(NB_SIMULATIONS):
        prices= [S0]
        for _ in range(N):
            #N(0, 1)
            stock_price = prices[-1] * np.exp((mu - 0.5*sigma**2) + sigma*npr.normal())
            prices.append(stock_price)

        resultats.append(prices)

    simulation = pd.DataFrame(resultats)

    simulation = simulation.T

    plt.plot(simulation, lw=0.5)
    #moyenne sur les colonnes (donc veteur ligne)
    plt.plot(simulation.mean(axis=1),'k', lw=3)
    plt.show()
    simulation['mean'] = simulation.mean(axis=1)
    # 2 chiffres après la virgule
    print("prédiction de la future valeur de l'action dans un an: €%.2f" % simulation['mean'].iloc[-1])

if __name__ == '__main__':
    stock_price_monte_carlo(50, 0.0002, 0.01)