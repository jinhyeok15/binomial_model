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

    not_adjusted_rnp = rnp(p10, p11, r00, pm2, delta=0.5)
    print("rnp not adjusted: " + str(not_adjusted_rnp))

    bp = bond_model(100, irm, not_adjusted_rnp)

    bp10 = bp.value(1, 0)
    bp11 = bp.value(1, 1)

    print("Risk Neutral Price Model: " + str(bp.data))

    adjusted_rnp = rnp(bp10, bp11, r00, pm3, delta=0.5)
    print("adjusted rnp: " + str(adjusted_rnp))

    expected_price = np.exp(-r00 * 0.5) * (bp10 * adjusted_rnp + bp11 * (1 - adjusted_rnp))
    print("expected price: " + str(expected_price))

    print("-----------------------------------")
