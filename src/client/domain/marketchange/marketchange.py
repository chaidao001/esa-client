import src.client.utils.utils

from .marketdefinition import MarketDefinition
from .runnerchange import RunnerChange


class MarketChange:
    def __init__(self, response):
        self.id = response["id"]
        if "rc" in response:
            self.rc = {rc["id"]: RunnerChange(rc) for rc in response["rc"]}
        else:
            self.rc = dict()
        if "img" in response:
            self.img = response["img"]
        else:
            self.img = False
        if "marketDefinition" in response:
            self.market_definition = MarketDefinition(response["marketDefinition"])
        if "tv" in response:
            self.tv = response["tv"]

    def update(self, market_change):
        if hasattr(market_change, "market_definition"):
            self.market_definition = market_change.market_definition

        for runner_id, runner_change in market_change.rc.items():
            if runner_id in self.rc:
                self.rc[runner_id].update(runner_change)
            else:
                self.rc[runner_id] = runner_change

        if hasattr(market_change, "tv"):
            self.tv = market_change.tv

    def formatted_string(self):

        ladder_format = '{:<15} {:<50} {:>50}\n'

        market_status = self.market_definition.status

        market_result = "Market {} (£{}) - {}\n".format(self.id, src.client.utils.utils.format_value(self.tv),
                                                        market_status.name)

        for runner in self.market_definition.runners:
            runner_id = runner.id

            if runner_id not in self.rc:
                continue

            runner_change = self.rc[runner_id]

            bdatb = runner_change.bdatb.price_list[:3][::-1]
            bdatl = runner_change.bdatl.price_list[:3]

            back_price_vol_format = '{:>12}' * len(bdatb)
            lay_price_vol_format = '{:<12}' * len(bdatl)

            bdatb_prices = back_price_vol_format.format(*[p.price for p in bdatb])
            bdatl_prices = lay_price_vol_format.format(*[p.price for p in bdatl])
            bdatb_sizes = back_price_vol_format.format(
                *['£' + src.client.utils.utils.format_value(p.vol) for p in bdatb])
            bdatl_sizes = lay_price_vol_format.format(
                *['£' + src.client.utils.utils.format_value(p.vol) for p in bdatl])

            market_result += ladder_format.format("Runner " + str(runner_change.id), bdatb_prices, bdatl_prices)
            market_result += ladder_format.format("£" + src.client.utils.utils.format_value(runner_change.tv),
                                                  bdatb_sizes, bdatl_sizes)

        return market_result + '\n'

    def __repr__(self):
        return str(vars(self))
