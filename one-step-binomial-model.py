from price import *
import binomial as bi
from zero import *

data0 = [
        [100, 0.50, 0, 99.5],
        [100, 1.00, 0, 98.3],
        [100, 1.50, 0, 97.1]
    ]

sample_market_data = {
        "Maturity": [0.5, 1.0, 1.5],
        "Price": [99.5, 98.3, 97.1],
        "Yield": zeros(data0),
        "ForwardRate": forward_rate(data0, 0.5)
    }

sample_irm = [
    [0.0100],
    [0.0300, 0.005]
]

if __name__ == '__main__':
    bi_irm = bi.model(sample_irm)

    r0 = bi_irm.value(0, 0)
    r1 = bi_irm.value(1, 0)
    r2 = bi_irm.value(1, 1)
    print(model_price(100, r1, delta=0.5))
    p1 = model_price(100, r1, delta=0.5)
    print("p1: " + str(p1))
    p2 = model_price(100, r2, delta=0.5)
    print("p2: " + str(p2))
    pm = sample_market_data["Price"][1]
    rnp = rnp(100, bi_irm, pm, 0.5)
    print("rnp: "+str(rnp))

    # put option payoff (RNP approach)
    rk = 0.02
    put_p1 = 100*max(rk-r1, 0)
    put_p2 = 100*max(rk-r2, 0)
    exp_value = put_p1*rnp+put_p2*(1-rnp)
    print("expected value at 6-month: "+str(exp_value))
    exp_value = model_price(exp_value, r0, delta=0.5)
    print("discounted value: "+str(exp_value))

    # Replicating portfolio approach
    scenario_6m = {
        "up": {
            "ir": r1,
            "6m_bond": 100,
            "1yr_bond": model_price(100, r1, delta=0.5),
            "derivative_price": put_p1
        },
        "dn": {
            "ir": r2,
            "6m_bond": 100,
            "1yr_bond": model_price(100, r2, delta=0.5),
            "derivative_price": put_p2
        }
    }

    return_matrix = np.matrix(
        [[scenario_6m["up"]["6m_bond"]/sample_market_data["Price"][0],
          scenario_6m["up"]["1yr_bond"]/sample_market_data["Price"][1]],
         [scenario_6m["dn"]["6m_bond"]/sample_market_data["Price"][0],
          scenario_6m["dn"]["1yr_bond"]/sample_market_data["Price"][1]]]
    )

    derivative_price_matrix = np.matrix(
        [[put_p1], [put_p2]]
    )

    ratio = simultaneous_equation(return_matrix, derivative_price_matrix)
    print(np.linalg.inv(return_matrix))
    portfolio_value = float(ratio[0][0]+ratio[1][0])
    print("portfolio value: "+str(portfolio_value))
