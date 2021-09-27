import numpy as np
import binomial as bi
import sympy as sym


def model_price(value, ir, delta=1.0):
    return value*np.exp(-ir*delta)


def rnp(up, dn, ir, market_price, delta=1.0):
    x = (market_price*np.exp(ir*delta)-dn)/(up-dn)
    return x


def simultaneous_equation(coefficient, objective):  # parameters' type is np.matrix
    inv_coefficient = np.linalg.inv(coefficient)
    return inv_coefficient*objective


def bond_model(par, irm, rnp_list):
    rnp_list.append(1)
    i = irm.size - 1
    rear = [par for r in range(2 ** irm.size)]
    bond_price = [rear]
    while i >= 0:
        node_price = []
        for j in range(2 ** i):
            p = rnp_list[i]
            c1 = rear[2 * j]
            c2 = rear[2 * j + 1]
            rij = irm.value(i, j)
            price = model_price(c1, rij, delta=0.5) * p + \
                model_price(c2, rij, delta=0.5) * (1 - p)
            node_price.append(price)
        bond_price.insert(0, node_price)
        rear = node_price
        i -= 1
    return bi.model(bond_price)


# binomial model rounding
def round_model(model, num):
    nd = 0
    for i in model.data:
        idx = 0
        for j in i:
            model.exchange(nd, idx, round(j, num))
            idx += 1
        nd += 1
    return model


def adjust_rnp(bpm, irm, rnp_list, pm, delta):
    x = sym.Symbol("x")
    rnp_list.append(x)
    i = irm.size-2
    rear = bpm.data[i+1]
    while i >= 0:
        value_list = []
        for j in range(2**i):
            p = rnp_list[i]
            c1 = rear[2 * j]
            c2 = rear[2 * j + 1]
            rij = irm.value(i, j)
            value_list.append(sym.expand(model_price(c1*p+c2*(1-p), rij, delta=delta)))
        rear = value_list
        i -= 1
    return sym.solve(rear[0]-pm, x)[0]
