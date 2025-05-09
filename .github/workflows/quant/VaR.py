import numpy as np
from scipy.stats import norm
import yfinance as yf
import pandas as pd
import datetime

def download_data(stock, start, end):
    datas = {}
    ticker = yf.download(stock, start, end, auto_adjust=False)
    datas[stock] = ticker['Adj Close']

    return pd.DataFrame(datas)

#valeur à risque pour les n prochains jours
def var(position, c, mu, sigma, n):

    return position * (mu * n - sigma* np.sqrt(n) * norm.ppf(1-c))

if __name__ == '__main__':
    start = datetime.datetime(2010,1,1)
    end= datetime.datetime(2020,1,1)

    stock_data = download_data('AAPL', start, end)
    #stock log-daily return
    stock_data['returns'] = np.log(stock_data['AAPL'] / stock_data['AAPL'].shift(1))
    stock_data = stock_data[1:]
    #amount of money we invest in 'AAPL'
    position=1e6
    #niveau de confiance
    c=0.95
    #.iloc[0] -> extraire la valeur numérique de Series
    mu = np.mean(stock_data['returns'])
    sigma = np.std(stock_data['returns'])

    print("la valeur à risque est de €%.2f" % var(position,c,mu,sigma,1))
