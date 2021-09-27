from price import *
import binomial as bi

sample_market_data = {
        "Maturity": [0.5, 1.0, 1.5],
        "Price": [99.1338, 97.8925, 96.1531],
        "Yield": [0.0174, 0.0213, 0.0262],
        "ForwardRate": [0.0174, 0.0252, 0.0359]
    }

sample_irm = [
    [0.0174],
    [0.0339, 0.0095],
    [0.05, 0.0256, 0.0256, 0.0011]
]


if __name__ == '__main__':
    irm = bi.model(sample_irm)
    r00 = irm.value(0, 0)
    r10 = irm.value(1, 0)
    r11 = irm.value(1, 1)
    p10 = model_price(100, r10, delta=0.5)
    p11 = model_price(100, r11, delta=0.5)
    pm2 = sample_market_data["Price"][1]
    pm3 = sample_market_data["Price"][2]

    rnp0 = rnp(p10, p11, r00, pm2, delta=0.5)
    print("rnp not adjusted: " + str(round(rnp0, 4)))

    bpm1 = round_model(bond_model(100, irm, [rnp0, rnp0]), 4)
    bp00 = bpm1.value(0, 0)
    print("Risk Neutral Price Model: " + str(bpm1.data))

    print("price error: " + str(round((bp00-pm3)**2*100, 2)) + "%")
    rnp1 = adjust_rnp(bpm1, irm, [rnp0], pm3, 0.5)

    print("adjusted rnp: " + str(round(rnp1, 4)))
    bpm2 = round_model(bond_model(100, irm, [rnp0, rnp1]), 4)
    expected_price = bpm2.value(0, 0)
    print("expected price: " + str(expected_price))
    print("adjusted bond model: " + str(bpm2.data))

    print("-----------------------------------")
