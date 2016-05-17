from src.client.domain.marketchange.runner import Runner
from src.client.domain.marketchange.marketchange import MarketChange
from src.client.domain.marketchange.marketstatus import MarketStatus
from src.client.utils.utils import format_value


class Cache:
    def __init__(self):
        self._markets = dict()

    def on_receive(self, market_changes: list()):
        for market_change in market_changes:
            if hasattr(market_change, "img") and market_change.img:
                market_id = market_change.id
                if market_change.market_def.status != MarketStatus.CLOSED:
                    self._markets[market_id] = market_change
                else:
                    # remove if full img and already in cache
                    if market_id in self._markets:
                        self._markets.pop(market_id)
            else:
                self._update_market(market_change)

    def _update_market(self, market_change: MarketChange):
        market_id = market_change.id
        market = self._markets[market_id]
        market.update(market_change)

        # remove market from cache if closed
        if market.market_def.status == MarketStatus.CLOSED:
            self._markets.pop(market_id)

    def formatted_string(self):
        ladder_format = '{:<15} {:<50} {:>50} {:<10} \n'

        result = ''

        for marketId, market in self._markets.items():
            market_status = market.market_def.status

            result += "Market {} (£{}) - {}\n".format(marketId, format_value(market.tv), market_status)

            if market_status == MarketStatus.CLOSED or not hasattr(market, "rc"):
                continue

            runner_changes = market.rc

            for runner_id, runner_change in runner_changes.items():
                if market.market_def.runners[runner_id].status != Runner.RunnerStatus.ACTIVE:
                    continue

                bdatb = runner_change.bdatb.price_list[:3][::-1]
                bdatl = runner_change.bdatl.price_list[:3]

                back_price_vol_format = '{:>12}' * len(bdatb)
                lay_price_vol_format = '{:<12}' * len(bdatl)

                bdatb_prices = back_price_vol_format.format(*[p.price for p in bdatb])
                bdatl_prices = lay_price_vol_format.format(*[p.price for p in bdatl])
                bdatb_sizes = back_price_vol_format.format(*['£' + str(p.vol) for p in bdatb])
                bdatl_sizes = lay_price_vol_format.format(*['£' + str(p.vol) for p in bdatl])

                result += ladder_format.format("Runner " + str(runner_change.id), bdatb_prices, bdatl_prices,
                                               self._get_ltp_string(runner_change.ltp))
                result += ladder_format.format("£" + format_value(runner_change.tv), bdatb_sizes, bdatl_sizes, "")

        return result

    @staticmethod
    def _get_ltp_string(ltp):
        if ltp is not None:
            return str(ltp)
        else:
            return ""

    @property
    def markets(self):
        return self._markets

    def __repr__(self):
        return str(vars(self))
