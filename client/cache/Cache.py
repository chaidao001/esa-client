from client.domain.marketchange import MarketChange
from client.utils.utils import format_value


class Cache:
    def __init__(self):
        self._markets = dict()

    def on_receive(self, market_changes: list()):
        for market_change in market_changes:
            if hasattr(market_change, "img") and market_change.img:
                self._markets[market_change.id] = market_change
            else:
                self._update_market(market_change)

    def _update_market(self, market_change: MarketChange):
        self._markets[market_change.id].update(market_change)

    def formatted_string(self):
        ladder_format = '{:<15} {:<50} {:>50} {:<10} \n'

        result = ''

        for marketId, market in self._markets.items():
            market_status = market.market_def.status

            result += "Market {} (£{}) - {}\n".format(marketId, format_value(market.tv), market_status)

            if market_status == "CLOSED":
                continue

            runners = market.market_def.runners
            runner_changes = market.rc

            for runner in runners:
                if runner.status != "ACTIVE":
                    continue

                rc = runner_changes[runner.id]

                bdatb = rc.bdatb.price_list[:3][::-1]
                bdatl = rc.bdatl.price_list[:3]

                back_price_vol_format = '{:>12}' * len(bdatb)
                lay_price_vol_format = '{:<12}' * len(bdatl)

                bdatb_prices = back_price_vol_format.format(*[p.price for p in bdatb])
                bdatl_prices = lay_price_vol_format.format(*[p.price for p in bdatl])
                bdatb_sizes = back_price_vol_format.format(*['£' + str(p.vol) for p in bdatb])
                bdatl_sizes = lay_price_vol_format.format(*['£' + str(p.vol) for p in bdatl])

                result += ladder_format.format("Runner " + str(runner.id), bdatb_prices, bdatl_prices, self._get_ltp_string(rc.ltp))
                result += ladder_format.format("£" + format_value(rc.tv), bdatb_sizes, bdatl_sizes, "")

        return result

    def _get_ltp_string(self, ltp):
        if ltp is not None:
            return str(ltp)
        else:
            return ""

    def __repr__(self):
        return str(vars(self))
