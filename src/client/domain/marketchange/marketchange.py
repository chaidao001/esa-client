from client.domain.marketchange.marketdefinition import MarketDefinition
from client.domain.marketchange.runner import Runner
from client.domain.marketchange.runnerchange import RunnerChange
from client.utils.utils import format_value


class MarketChange:
    def __init__(self, response):
        self._id = response["id"]
        if "rc" in response:
            self._rc = {rc["id"]: RunnerChange(rc) for rc in response["rc"]}
        else:
            self._rc = dict()
        if "img" in response:
            self._img = response["img"]
        else:
            self._img = False
        if "marketDefinition" in response:
            self._market_definition = MarketDefinition(response["marketDefinition"])
        if "tv" in response:
            self._tv = response["tv"]

    def update(self, market_change):
        if hasattr(market_change, "market_def"):
            self._market_definition = market_change.market_def

        for runner_id, runner_change in market_change.rc.items():
            if runner_id in self.rc:
                self.rc[runner_id].update(runner_change)
            else:
                self.rc[runner_id] = runner_change

        if hasattr(market_change, "tv"):
            self._tv = market_change.tv

    @property
    def id(self):
        return self._id

    @property
    def rc(self):
        return self._rc

    @property
    def img(self):
        return self._img

    @property
    def market_def(self):
        return self._market_definition

    @property
    def tv(self):
        return self._tv

    def formatted_string(self):

        ladder_format = '{:<15} {:<50} {:>50}\n'

        market_def = self.market_def
        market_status = market_def.status

        market_result = "Market {} (£{}) - {}\n".format(self.id, format_value(self.tv), market_status.name)

        for runner in market_def.runners:
            runner_id = runner.id

            if runner_id not in self.rc:
                continue

            runner_change = self.rc[runner_id]

            if runner.status != Runner.RunnerStatus.ACTIVE \
                    or not hasattr(runner_change, "bdatb") or runner_change.bdatb.size() < 3 \
                    or not hasattr(runner_change, "bdatl") or runner_change.bdatl.size() < 3:
                continue

            bdatb = runner_change.bdatb.price_list[:3][::-1]
            bdatl = runner_change.bdatl.price_list[:3]

            back_price_vol_format = '{:>12}' * len(bdatb)
            lay_price_vol_format = '{:<12}' * len(bdatl)

            bdatb_prices = back_price_vol_format.format(*[p.price for p in bdatb])
            bdatl_prices = lay_price_vol_format.format(*[p.price for p in bdatl])
            bdatb_sizes = back_price_vol_format.format(*['£' + format_value(p.vol) for p in bdatb])
            bdatl_sizes = lay_price_vol_format.format(*['£' + format_value(p.vol) for p in bdatl])

            market_result += ladder_format.format("Runner " + str(runner_change.id), bdatb_prices, bdatl_prices)
            market_result += ladder_format.format("£" + format_value(runner_change.tv), bdatb_sizes, bdatl_sizes)

        return market_result + '\n'

    def __repr__(self):
        return str(vars(self))
