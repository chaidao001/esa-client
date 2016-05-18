class PriceVol:
    def __init__(self, response):
        self._price = response[0]
        self._vol = response[1]

    @property
    def price(self):
        return self._price

    @property
    def vol(self):
        return self._vol

    def __eq__(self, other):
        return self.price == other.price and self.vol == other.vol

    def __repr__(self):
        return str(vars(self))
