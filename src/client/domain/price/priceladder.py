from .pricevol import PriceVol


class PriceLadder:
    def __init__(self, prices: list):
        self.ladder = {p[0]: PriceVol(p[1:]) for p in prices}

    def update(self, price_ladder):
        self.ladder.update(price_ladder.ladder)
        self.ladder = {k: v for k, v in self.ladder.items() if v.vol > 0}

    @property
    def price_list(self):
        return [self.ladder[position] for position in sorted(self.ladder)]

    def get_price_at_position(self, position):
        return self.ladder[position]

    def __len__(self):
        return len(self.ladder)

    def __eq__(self, other):
        return self.ladder == other.ladder

    def __repr__(self):
        return str(vars(self))
