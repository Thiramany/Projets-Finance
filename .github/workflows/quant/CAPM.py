import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

#market free rate
RISK_FREE_RATE = 0.05

MONTH_IN_YEAR = 12
class CAPM:

    def __init__(self, stocks, start_date, end_date):
        self.data = None
        self.stocks = stocks
        self.start_date = start_date
        self.end_date = end_date

    def download_data(self):

        data = yf.download(self.stocks, start=self.start_date, end=self.end_date, auto_adjust=False)
        data = data['Adj Close']
        return pd.DataFrame(data)

    def initialize(self):

        stock_data = self.download_data()
        #on utilise les rendements mensuels au lieu des rendements quotidiens ('M')
        stock_data = stock_data.resample('ME').last()

        self.data = pd.DataFrame({'s_adjclose' : stock_data[self.stocks[0]],
                                  'm_adjclose' : stock_data[self.stocks[1]]})

        self.data[['s_returns', 'm_returns']] = np.log(self.data[['s_adjclose', 'm_adjclose']] /
                                                       self.data[['s_adjclose', 'm_adjclose']].shift(1))
        self.data = self.data[1:]

    def calculate_beta(self):
        # matrice de covariance symétrique
        # variance de l'action puis du marché dans la diagonale
        cov_matrix = np.cov(self.data['s_returns'], self.data['m_returns'])
        beta = cov_matrix[1,0] / cov_matrix[1,1]
        print("Beta par la formule: ",beta)

    def regression(self):
        #utiliser la régression linéaire pour trouver une ligne de donnée
        # [stock_returns, market_returns] - pente = beta
        #deg = 1 -> linéaire, 2 -> quadratique, 3 -> cubique
        beta, alpha = np.polyfit(self.data['m_returns'], self.data['s_returns'], deg=1)
        print("Beta par la regression: ", beta)
        #rendement annuel moyen = rendement mensuel moyen * 12
        expected_return = RISK_FREE_RATE + beta * (self.data['m_returns'].mean()*MONTH_IN_YEAR - RISK_FREE_RATE)

        print('expected return: ', expected_return)
        self.plot_regression(alpha, beta)

    def plot_regression(self, alpha, beta):
        fig, axis = plt.subplots(figsize = (10,6))
        axis.scatter(self.data['s_returns'], self.data['m_returns'], label = "Points de données")
        axis.plot(self.data['m_returns'], beta * self.data['m_returns'] + alpha, color = 'red', label = 'CAPM')
        plt.title('Capital Asset Pricing Model, déterminer alpha et beta')
        plt.xlabel('Market return')
        plt.ylabel('Stock return')
        plt.legend()
        plt.grid(True)
        plt.hist(self.data['s_returns'])
        plt.show()

if __name__ == '__main__':
    capm = CAPM(['IBM','^GSPC'], '2012-01-01', '2017-01-01')
    capm.initialize()
    capm.calculate_beta()
    capm.regression()