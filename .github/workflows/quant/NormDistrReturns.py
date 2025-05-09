import numpy as np
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
def download_data(stock, start_date, end_date):
    data = yf.download(stock, start=start_date, end=end_date, auto_adjust=False)
    data = data['Adj Close']
    return pd.DataFrame(data)
def calculate_returns(stock_data):
    stock_data=np.log(stock_data['Adj Close'] / stock_data['Adj Close'].shift(1))
    return stock_data[1:]


def show(stock_data):
    #bins, nombre d'intervalles régulières
    plt.hist(calculate_returns(stock_data), bins =700)
    stock_var = stock_data.var()
    stock_mean = stock_data.mean()
    sigma = np.sqrt(stock_data)
    x= np.linspace(stock_mean- 5*sigma, stock_mean + 5* sigma, 100)
    plt.plot(x, norm.pdf(x, stock_mean, sigma))
    plt.show()

if __name__ == '__main__':
    stock_data = download_data('IBM', '2010-01-01', '2017-01-01')
    show(stock_data)
