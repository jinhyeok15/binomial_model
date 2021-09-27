from price import *
import binomial as bi
from zero import *

data = [
    [100, 0.50, 0, 99.5],
    [100, 1.00, 0, 98.3],
    [100, 1.50, 0, 97.1]
]

sample_market_data = {
        "Maturity": [0.5, 1.0, 1.5],
        "Price": [99.5, 98.3, 97.1],
        "Yield": zeros(data),
        "ForwardRate": forward_rate(data, 0.5)
    }

one_step_irm = [
    [0.0100],
    [0.0300, 0.005]
]

two_step_irm = [
    [0.0100],
    [0.0300, 0.005],
    [0.0350, 0.0240, 0.0240, 0.004]
]


if __name__ == '__main__':
    irm1 = bi.model(one_step_irm)
    mp10 = sample_market_data["Price"][1]
    rnp0 = rnp(100, irm1, mp10, 0.5)
    print("rnp at one step: " + str(rnp0))
    bpm0 = bond_model(100, irm1, [rnp0], 0.5)
    print(round_model(bpm0, 4))

    # put option payoff (RNP approach)
    rk = 0.02
    put_p1 = 100 * max(rk - bpm0.value(1, 0), 0)
    put_p2 = 100 * max(rk - bpm0.value(1, 1), 0)
    exp_value = put_p1 * rnp0 + put_p2 * (1 - rnp0)
    print("expected value at 6-month: " + str(exp_value))
    exp_value = model_price(exp_value, bpm0.value(0, 0), delta=0.5)
    print("discounted value: " + str(exp_value))

    irm2 = bi.model(two_step_irm)
    mp15 = sample_market_data["Price"][2]
    bpm1 = bond_model(100, irm2, [rnp0, rnp0], 0.5)
    sol_rnp1 = adjust_rnp(bpm1, irm2, [rnp0], mp15, 0.5)
    print("solution: " + str(sol_rnp1))
    rnp1 = sol_rnp1[0]
    print("rnp with adjust: " + str(rnp1))
    bpm2 = bond_model(100, irm2, [rnp0, rnp1], 0.5)

    print("-----------------------------------")
