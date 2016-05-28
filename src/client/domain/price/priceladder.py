from client.domain.price.pricevol import PriceVol


class PriceLadder:
    def __init__(self, prices: list):
        self._ladder = {p[0]: PriceVol(p[1:]) for p in prices}

    def update(self, price_ladder):
        self._ladder.update(price_ladder.ladder)
        self._ladder = {k: v for k, v in self._ladder.items() if v.vol > 0}

    @property
    def ladder(self):
        return self._ladder

    @property
    def price_list(self):
        return [self.ladder[position] for position in self.ladder]

    def get_price_at_position(self, position):
        return self._ladder[position]

    def size(self):
        return len(self._ladder)

    def __eq__(self, other):
        return self.ladder == other.ladder

    def __repr__(self):
        return str(vars(self))
