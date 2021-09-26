import numpy as np
import binomial as bi
import sympy as sym


def model_price(value, ir, delta=1.0):
    return value*np.exp(-ir*delta)


def rnp(up, dn, ir, market_price, delta=1.0):
    x = (market_price*np.exp(ir*delta)-dn)/(up-dn)
    return x


def simultaneous_equation(coefficient, objective):  # np.matrix
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


def adjust_rnp(bpm, irm, pm, delta):
    p = sym.Symbol('p')
    bp20 = bpm.value(2, 0)
    bp21 = bpm.value(2, 1)
    bp22 = bpm.value(2, 2)
    bp23 = bpm.value(2, 3)
    r10 = irm.value(1, 0)
    r11 = irm.value(1, 1)
    r00 = irm.value(0, 0)
    bp10 = sym.expand(model_price(bp20*p+bp21*(1-p), r10, delta=delta))
    bp11 = sym.expand(model_price(bp22*p+bp23*(1-p), r11, delta=delta))
    bp00 = sym.expand(model_price(bp10*p+bp11*(1-p), r00, delta=delta))
    return sym.solve(bp00-pm, p)
