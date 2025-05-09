from math import exp as e

#Time value of money
def future_discrete_value(x, r, n):
    return x*(1+r)**n

def present_discrete_value(x, r ,n):
    return x/(1+r)**n

def future_continuous_value(x, r, n):
    return x*e(r*n)

def present_continuous_value(x, r ,n):
    return x*e(-r*n)

if __name__ == '__main__':
    # value of investment
    x = 100
    # define the interest rate
    r = 0.05
    # duration (years)
    n = 5

    print("future value of x: %s" % future_discrete_value(x,r,n))
    print("present value of x: %s" % present_discrete_value(x, r, n))
    print("future value of x: %s" % future_continuous_value(x, r, n))
    print("present value of x: %s" % present_continuous_value(x,r,n))

# bonds price

class ZeroCouponBonds:
    #constructeur
    def __init__(self, principal, maturity, interest_rate):
        #principal amount
        self.principal = principal
        #time of maturity
        self.maturity = maturity
        self.interest_rate = interest_rate/100

    def present_value(self, x, n):
        return x / (1+self.interest_rate)**n

    def calculate_price(self):
        return self.present_value(self.principal, self.maturity)
##
if __name__ == '__main__':

    bond = ZeroCouponBonds(1000,2,4)
    print(bond.calculate_price())


class CouponBond:
    #constuctor
    def __init__(self, principal, rate, maturity, interest_rate):
        self.principal = principal
        self.rate = rate / 100
        self.maturity = maturity
        self.interest_rate = interest_rate / 100

    def present_value(self, x, n):
        return x / (1+self.interest_rate)**n

    def present_value_continuous(self, x, n):
        return x * e(-self.interest_rate*n)

    def calculate_price(self):

        price = 0

        for i in (1, self.maturity+1) :
           price += self.present_value_continuous(self.principal * self.rate, i)

        price += self.present_value_continuous(self.principal, self.maturity)

        return price

if __name__ == '__main__':

    bonds = CouponBond(1000, 10, 3, 4)
    print(bonds.calculate_price())





