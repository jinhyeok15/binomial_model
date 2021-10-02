import numpy as np
import binomial as bi
import sympy as sym
from scipy.optimize import fsolve


def model_price(value, ir, delta=1.0):
    return value * np.exp(-ir * delta)


def rnp(par, irm, market_price, delta=1.0):  # only use one-step model
    up = model_price(par, irm.value(1, 0), delta)
    dn = model_price(par, irm.value(1, 1), delta)
    x = (market_price * np.exp(irm.value(0, 0) * delta) - dn) / (up - dn)
    return x


def simultaneous_equation(coefficient, target):  # parameters' type is np.matrix
    inv_coefficient = np.linalg.inv(coefficient)
    return inv_coefficient * target


def bond_model(par, irm, rnp_list, delta):
    rnp_list.append(1.0)
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
            price = model_price(c1, rij, delta) * p + \
                    model_price(c2, rij, delta) * (1 - p)
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
    i = irm.size - 2
    rear = bpm.data[i + 1]
    while i >= 0:
        value_list = []
        for j in range(2 ** i):
            p = rnp_list[i]
            c1 = rear[2 * j]
            c2 = rear[2 * j + 1]
            rij = irm.value(i, j)
            value_list.append(sym.expand(model_price(c1 * p + c2 * (1 - p), rij, delta=delta)))
        rear = value_list
        i -= 1
    return sym.solve(rear[0] - pm, x)


def ho_lee_irm(par, r0, market_data, volatility, delta, th0=0.01):
    _rnp = []
    _irm = bi.model([[r0]])
    for i in market_data:
        _rnp.append(0.5)
        get_bpm = lambda th: bond_model(par,
                                        _get_next_irm(_irm, th, volatility, delta),
                                        _rnp, delta)
        price_error = lambda th: (get_bpm(th).value(0, 0) - i) ** 2
        _result = fsolve(price_error, th0)
        theta = _result[0]
        _irm = _get_next_irm(_irm, theta, volatility, delta)
    return _irm


def _ir_by_ho_lee(ir, theta, vol, delta):
    return [ir + theta * delta + vol * delta ** 0.5,
            ir + theta * delta - vol * delta ** 0.5]


def _get_next_irm(__irm, __th, __vol, __delta):
    next_irm_data = []
    next_data = []
    for i in __irm.data[-1]:
        for j in _ir_by_ho_lee(i, __th, __vol, __delta):
            next_data.append(j)
    for i in __irm.data:
        next_irm_data.append(i)
    next_irm_data.append(next_data)
    return bi.model(next_irm_data)


if __name__ == '__main__':
    print("main")
