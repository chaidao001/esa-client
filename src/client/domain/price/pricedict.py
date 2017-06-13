class PriceDict:
    def __init__(self, prices):
        self.prices = {p[0]: p[1] for p in prices}

    def update(self, prices):
        self.prices.update(prices.prices)
        self.prices = {k: v for k, v in self.prices.items() if v > 0}

    def get_vol_for_price(self, price):
        if price in self.prices:
            return self.prices[price]
        else:
            return 0

    def __repr__(self):
        return str(vars(self))
