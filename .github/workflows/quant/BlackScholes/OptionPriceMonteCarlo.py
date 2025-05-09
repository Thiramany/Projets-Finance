import numpy as np
import numpy.random as npr

class OptionPrice:
    def __init__(self, S0, E, T, rf, sigma, iterations):
        self.S0 = S0
        self.E = E
        self.T = T
        self.rf = rf
        self.sigma = sigma
        self.iterations = iterations

    def call_option_simulations(self):

        option_data = np.zeros([self.iterations,2])

        rand = npr.normal(0, 1, [1, self.iterations])

        stock_price = self.S0 * np.exp((self.rf - 0.5 * self.sigma ** 2)
                                   + self.sigma * np.sqrt(self.T) * rand)

        #on a besoin de S-E parce que on doit calculer max(S-E,0)
        option_data[:, 1] = stock_price - self.E

        #Monte Carlo (iteration puis moyenne)
        moyenne = np.sum(np.amax(option_data, axis=1)) / float(self.iterations)


        return moyenne*np.exp(-self.rf * self.T)

    def put_option_simulations(self):

        option_data = np.zeros([self.iterations,2])

        rand = npr.normal(0, 1, [1, self.iterations])

        stock_price = self.S0 * np.exp((self.rf - 0.5 * self.sigma ** 2)
                                   + self.sigma * np.sqrt(self.T) * rand)

        #on a besoin de S-E parce que on doit calculer max(E-S,0)
        option_data[:, 1] = self.E - stock_price

        #Monte Carlo (iteration puis moyenne)
        moyenne = np.sum(np.amax(option_data, axis=1)) / float(self.iterations)

        return moyenne*np.exp(-self.rf * self.T)

if __name__ == '__main__':
    OptionPrice = OptionPrice(100, 100, 1, 0.05, 0.2, 1000)
    print("Valeur de l'option d'achat est €%.2f" % OptionPrice.call_option_simulations())
    print("Valeur de l'option de vente est €%.2f" % OptionPrice.put_option_simulations())