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
    [0.0339, 0.0095],
    [0.05, 0.0256, 0.0256, 0.0011]
]

irm = Binomial(3)
irm.append(sample_irm)

r00 = irm.value(0, 0)
r10 = irm.value(1, 0)
r11 = irm.value(1, 1)
p10 = model_price(100, r10, delta=0.5)
p11 = model_price(100, r11, delta=0.5)
pm2 = sample_market_data["Price"][1]
pm3 = sample_market_data["Price"][2]

not_adjusted_rnp = rnp(p10, p11, r00, pm2, delta=0.5)
print("rnp not adjusted: " + str(not_adjusted_rnp))

bond_price = []
i = irm.size-1  # size = 3
rear = [100 for r in range(2**irm.size)]
while i >= 0:
    node_price = []
    for j in range(2**i):
        c1 = rear[2*j]
        c2 = rear[2*j+1]
        rij = irm.value(i, j)
        price = model_price(c1, rij, delta=0.5)*not_adjusted_rnp + \
                model_price(c2, rij, delta=0.5)*(1-not_adjusted_rnp)
        node_price.append(price)
    bond_price.insert(0, node_price)
    rear = node_price
    i -= 1

print(bond_price)

bp = Binomial(3)
bp.append(bond_price)

bp10 = bp.value(1, 0)
bp11 = bp.value(1, 1)

adjusted_rnp = rnp(bp10, bp11, r00, pm3, delta=0.5)
print("adjusted rnp: "+str(adjusted_rnp))
if __name__ == '__main__':
    print("-------------------")
