from scipy import stats
from numpy import log, exp, sqrt

#solution de l équation de black Scholes'
#prix initial
def call_option_price(S, E, T, risk_free_rate, sigma):
    d1 = log(S / E) + (risk_free_rate + 1/2 * sigma**2)*T/sigma*sqrt(T)
    d2 = d1 - sigma*sqrt(T)
    print("d1 = %s" % d1.round(4))
    print("d2 = %s" % d2.round(4))

    #distribution normale
    #cdf : cumulative distribution function
    return S*stats.norm.cdf(d1) - E*exp(-risk_free_rate*T) * stats.norm.cdf(d2)

#prix initial
def put_option_price(S, E, T, risk_free_rate, sigma):
    d1 = log(S / E) + (risk_free_rate + 1/2 * sigma**2)*T/sigma*sqrt(T)
    d2 = d1 - sigma*sqrt(T)

    #distribution normale standardisée
    #cdf : cumulative distribution function
    return -S*stats.norm.cdf(-d1) + E*exp(-risk_free_rate*T) * stats.norm.cdf(-d2)

if __name__ == '__main__':
    S=100
    E=100
    T=1
    risk_free_rate = 0.05
    sigma = 0.2

    call_price = call_option_price(S,E,T,risk_free_rate, sigma)
    put_price = put_option_price(S, E, T, risk_free_rate, sigma)
    print("Call option price = %s €" % call_price)
    print("Put option price = %s €" % put_price)