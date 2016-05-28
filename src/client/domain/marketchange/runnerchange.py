from client.domain.price.lasttradedprice import LastTradedPrice
from client.domain.price.pricedict import PriceDict
from client.domain.price.priceladder import PriceLadder


class RunnerChange:
    def __init__(self, response):
        if 'id' in response:
            self._id = response['id']
        if 'atb' in response:
            self._atb = PriceDict(response['atb'])
        if 'atl' in response:
            self._atl = PriceDict(response['atl'])
        if 'batb' in response:
            self._batb = PriceLadder(response['batb'])
        if 'batl' in response:
            self._batl = PriceLadder(response['batl'])
        if 'bdatb' in response:
            self._bdatb = PriceLadder(response['bdatb'])
        if 'bdatl' in response:
            self._bdatl = PriceLadder(response['bdatl'])
        if 'spn' in response:
            self._spn = response['spn']
        if 'spf' in response:
            self._spf = response['spf']
        if 'spb' in response:
            self._spb = PriceDict(response['spb'])
        if 'spl' in response:
            self._spl = PriceDict(response['spl'])
        if 'trd' in response:
            self._trd = PriceDict(response['trd'])
        if 'ltp' in response:
            self._ltp = LastTradedPrice(response['ltp'], hasattr(self, "_trd"))
        else:
            # Return an empty LastTradedPrice to trigger update()
            self._ltp = LastTradedPrice(None, hasattr(self, "_trd"))
        if 'tv' in response:
            self._tv = response['tv']

    def update(self, runner_change):
        for attr, value in vars(runner_change).items():
            if hasattr(self, attr):
                self_attr = getattr(self, attr)
                if hasattr(self_attr, "update"):
                    self_attr.update(value)
                else:
                    setattr(self, attr, value)
            else:
                setattr(self, attr, value)

    @property
    def id(self):
        return self._id

    @property
    def atb(self):
        return self._atb

    @property
    def atl(self):
        return self._atl

    @property
    def batb(self):
        return self._batb

    @property
    def batl(self):
        return self._batl

    @property
    def bdatb(self):
        return self._bdatb

    @property
    def bdatl(self):
        return self._bdatl

    @property
    def spn(self):
        return self._spn

    @property
    def spf(self):
        return self._spf

    @property
    def spb(self):
        return self._spb

    @property
    def spl(self):
        return self._spl

    @property
    def trd(self):
        return self._trd

    @property
    def ltp(self):
        return self._ltp.price

    @property
    def tv(self):
        return self._tv

    def __repr__(self):
        return str(vars(self))
