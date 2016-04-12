class PriceDict:
    def __init__(self, prices):
        self._prices = {p[0]: p[1] for p in prices}

    def update(self, prices):
        self._prices.update(prices.prices)
        self._prices = {k: v for k, v in self._prices.items() if v > 0}

    @property
    def prices(self):
        return self._prices

    def get_vol_for_price(self, price):
        if price in self._prices:
            return self._prices[price]
        else:
            return 0

    def __repr__(self):
        return str(vars(self))
