import numpy as np

market_data = {
    "Maturity": [0.5, 1.0, 1.5],
    "Price": [99.1338, 97.8925, 96.1531],
    "Yield": [0.0174, 0.0213, 0.0262],
    "ForwardRate": [0.0174, 0.0252, 0.0359]
}

irm = [
    0.0174,
    [0.0339, 0.0095]
]


def model_price(value, ir, delta=1):
    return value*np.exp(-ir*delta)


def rnp(p1, p2, ir, pm, delta=1):
    x = (pm*np.exp(ir*delta)-p2)/(p1-p2)
    return x


if __name__ == '__main__':
    print(model_price(100, irm[1][0], delta=0.5))
    p1 = model_price(100, irm[1][0], delta=0.5)
    p2 = model_price(100, irm[1][1], delta=0.5)
    pm = market_data["Price"][1]
    rnp = rnp(p1, p2, irm[0], pm, delta=0.5)
    print("rnp: "+str(rnp))

    # put option payoff (RNP approach)
    r0 = irm[0]
    r1 = irm[1][0]
    r2 = irm[1][1]
    rk = 0.02
    put_p1 = 100*max(rk-r1, 0)
    put_p2 = 100*max(rk-r2, 0)
    exp_value = put_p1*rnp+put_p2*(1-rnp)
    print("expected value at 6-month: "+str(exp_value))
    exp_value = model_price(exp_value, r0, delta=0.5)
    print("discounted value: "+str(exp_value))
