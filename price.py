import numpy as np
import binomial as bi


def model_price(value, ir, delta=1.0):
    return value*np.exp(-ir*delta)


def rnp(up, dn, ir, market_price, delta=1.0):
    x = (market_price*np.exp(ir*delta)-dn)/(up-dn)
    return x


def simultaneous_equation(coefficient, objective):
    inv_coefficient = np.linalg.inv(coefficient)
    return inv_coefficient*objective


def bond_model(principal, irm, rn_prop):
    i = irm.size - 1
    rear = [principal for r in range(2 ** irm.size)]
    bond_price = [rear]
    while i >= 0:
        node_price = []
        for j in range(2 ** i):
            c1 = rear[2 * j]
            c2 = rear[2 * j + 1]
            rij = irm.value(i, j)
            price = model_price(c1, rij, delta=0.5) * rn_prop + \
                model_price(c2, rij, delta=0.5) * (1 - rn_prop)
            node_price.append(price)
        bond_price.insert(0, node_price)
        rear = node_price
        i -= 1
    return bi.model(bond_price)
