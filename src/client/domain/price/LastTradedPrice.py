class LastTradedPrice:
    def __init__(self, price, traded):
        self._price = price
        self._traded = traded

    def update(self, last_traded_price):
        self._traded = last_traded_price.traded

        # Has a valid "ltp" value => update values
        if last_traded_price.price is not None:
            self._price = last_traded_price.price

    @property
    def price(self):
        if self._traded:
            return self._price
        else:
            return None

    @property
    def traded(self):
        return self._traded

    def __repr__(self):
        return str(vars(self))
