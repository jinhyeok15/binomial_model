import numpy as np


def model_price(value, ir, delta=1.0):
    return value*np.exp(-ir*delta)


def rnp(up, dn, ir, market_price, delta=1.0):
    x = (market_price*np.exp(ir*delta)-dn)/(up-dn)
    return x


def simultaneous_equation(coefficient, objective):
    inv_coefficient = np.linalg.inv(coefficient)
    return inv_coefficient*objective
