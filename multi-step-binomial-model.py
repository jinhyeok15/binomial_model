from price import *
from binomial import Binomial

sample_market_data = {
        "Maturity": [0.5, 1.0, 1.5],
        "Price": [99.1338, 97.8925, 96.1531],
        "Yield": [0.0174, 0.0213, 0.0262],
        "ForwardRate": [0.0174, 0.0252, 0.0359]
    }

sample_irm = [
    [0.0174],
    [0.0339, 0.095],
    [0.05, 0.0256, 0.0256, 0.0011]
]
