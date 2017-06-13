class PriceVol:
    def __init__(self, response):
        self.price = response[0]
        self.vol = response[1]

    def __eq__(self, other):
        return self.price == other.price and self.vol == other.vol

    def __repr__(self):
        return str(vars(self))
