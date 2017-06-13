from ..price.pricedict import PriceDict
from ..price.priceladder import PriceLadder


class RunnerChange:
    def __init__(self, response):
        if 'id' in response:
            self.id = response['id']
        if 'atb' in response:
            self.atb = PriceDict(response['atb'])
        if 'atl' in response:
            self.atl = PriceDict(response['atl'])
        if 'batb' in response:
            self.batb = PriceLadder(response['batb'])
        if 'batl' in response:
            self.batl = PriceLadder(response['batl'])
        if 'bdatb' in response:
            self.bdatb = PriceLadder(response['bdatb'])
        if 'bdatl' in response:
            self.bdatl = PriceLadder(response['bdatl'])
        if 'spn' in response:
            self.spn = response['spn']
        if 'spf' in response:
            self.spf = response['spf']
        if 'spb' in response:
            self.spb = PriceDict(response['spb'])
        if 'spl' in response:
            self.spl = PriceDict(response['spl'])
        if 'trd' in response:
            self.trd = PriceDict(response['trd'])
        if 'ltp' in response:
            self.ltp = response['ltp']
        if 'tv' in response:
            self.tv = response['tv']

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

    def __repr__(self):
        return str(vars(self))
