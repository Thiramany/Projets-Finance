#Modern Portfolio Theory
import numpy as np
import yfinance as yf #download dts on Yahoo
import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize as optimization #optimized alg

#ACTIONS CHOSIS
stocks = ['AAPL', 'TSLA', 'GE', 'AMZN', 'DB']

#données passées - définir les dates de DEBUT et FIN
start_date= '2010-01-01'
end_date= '2017-01-01'

NUM_TRADING_DAYS = 252 #On enlève les jours feriés, week_ends...
NUM_PORTFOLIOS = 10000 #nombre de portefeuilles aléatoires générés
def download_data():
    # name of the stock (clé) - valeur action (2023-2025) comme valeur
    stock_data = {}

    for stock in stocks :
        #prix de clotûre
        ticker = yf.Ticker(stock)
        stock_data[stock] = ticker.history(start=start_date, end=end_date)['Close']

    return pd.DataFrame(stock_data)

def show_data(data):
    data.plot(figsize=(10, 4))
    plt.title('cours des stocks')
    plt.show()

def calculate_return(data):
    #log return :  log S(t+1)/S(t)
    log_return = np.log(data/data.shift(1))
    return log_return[1:]

def show_statistics(returns):
    # rendement annuel moyen = rendement quotidien moyen * 252
    print(returns.mean() * NUM_TRADING_DAYS)
    print(returns.cov() * NUM_TRADING_DAYS)

def show_mean_variance(returns, weights):
    portfolio_return = np.sum(returns.mean()*weights) * NUM_TRADING_DAYS
    portfolio_volatility = np.dot(weights.T, np.dot(returns.cov()*NUM_TRADING_DAYS, weights))
    print("Expected portfolio mean (return) : ", portfolio_return)
    print("Expected portfolio volatility (standard deviation): ", portfolio_volatility)

def generate_portfolio(returns):
    portfolio_means = []
    portfolio_risks = []
    portfolio_weights = []

    for _ in range(NUM_PORTFOLIOS):
        w = np.random.random(len(stocks))
        w /= np.sum(w)
        portfolio_weights.append(w)
        portfolio_means.append(np.sum(returns.mean()*w) * NUM_TRADING_DAYS)
        portfolio_risks.append(np.sqrt(np.dot(w.T, np.dot(returns.cov()*NUM_TRADING_DAYS, w))))
    return np.array(portfolio_weights), np.array(portfolio_means), np.array(portfolio_risks)

def statistics(weights, returns):
    portfolio_return = np.sum(returns.mean()*weights) * NUM_TRADING_DAYS
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(returns.cov()*NUM_TRADING_DAYS, weights)))

    return np.array([portfolio_return, portfolio_volatility, portfolio_return/portfolio_volatility])

#scipy optimize peut trouve rle minimum d'une fonction donnée
#le maximum de f(x) est le mminimum de -f(x)
def min_function_sharpe(weights, returns):
    return -statistics(weights, returns)[2]

#contraintes : la somme des poids = 1
#f(x) = 0 la fonction à minimiser
def optimize_portfolio(weights, returns):
    #la somme des poids doit être égale à 1
    #scipy attends constraints de cette forme
    constraints = {'type' : 'eq', 'fun' : lambda x: np.sum(x) - 1}
    #les poids peuvent être à 1 au pire : 1 quand 100% de l'argent est investi dans une seule action
    bounds = tuple((0,1) for _ in range(len(stocks)))
    return optimization.minimize(fun= min_function_sharpe, x0 = weights[0],
                          args=returns, method='SLSQP', bounds=bounds,
                          constraints=constraints)

#optimum = optimize_portfolio
def print_optimal_portfolio(optimum, returns):
    #optimum['x'] retourne le vectuer poids optimal
    print("Optimum portfolio: ", optimum['x'].round(3))
    print("Expected return, volatility and Sharpe ratio: ", statistics(optimum['x'].round(3), returns))


def show_optimal_portfolio(optimum, returns, portfolio_returns, portfolio_vols):
    plt.figure(figsize=(10,6))
    plt.scatter(portfolio_vols, portfolio_returns, c=portfolio_returns/portfolio_vols, marker='.')
    plt.xlabel("Expected Volatility (Risk)")
    plt.ylabel("Expected Return")
    plt.colorbar(label="Sharpe Ratio")
    plt.plot(statistics(optimum['x'], returns)[1], statistics(optimum['x'],returns)[0], 'g*', markersize=20)
    plt.show()
# après avoir crée les fonctions pour calculer les rendements et les risques associés.
# Il faut générer différents portefeuilles pour trouver le plus optimal
if __name__ == '__main__':
    dataset=download_data()
    log_returns = calculate_return(dataset)
    #show_statistics(log_returns)
    print("Rendement moyen annuel par action :")
    print(log_returns.mean() * NUM_TRADING_DAYS)

    portfolio_weights, means, risks = generate_portfolio(log_returns)

    optimum=optimize_portfolio(portfolio_weights, log_returns)
    print_optimal_portfolio(optimum, log_returns)
    show_optimal_portfolio(optimum, log_returns, means, risks)

