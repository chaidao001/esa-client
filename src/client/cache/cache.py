import logging

from src.client.domain.marketchange.marketchange import MarketChange
from src.client.domain.marketchange.marketstatus import MarketStatus
from src.client.domain.marketchange.runner import Runner
from src.client.utils.utils import format_value


class Cache:
    def __init__(self):
        self._markets = dict()

    def on_receive(self, market_changes: list()):
        for market_change in market_changes:
            market_id = market_change.id
            if market_change.img:
                if market_change.market_def.status != MarketStatus.CLOSED:
                    self._markets[market_id] = market_change
                else:
                    # remove if full img and already in cache
                    if market_id in self._markets:
                        logging.info("Market %s is closed.  Removing from cache" % market_id)
                        self._markets.pop(market_id)
                    else:
                        logging.info("Market %s is closed.  Ignore" % market_id)
            else:
                self._update_market(market_change)

    def _update_market(self, market_change: MarketChange):
        market_id = market_change.id

        if market_id not in self._markets:
            if hasattr(market_change, "market_def") and market_change.market_def.status == MarketStatus.CLOSED:
                logging.info("Market %s has been closed and removed from cache.  Ignore" % market_id)
            else:
                logging.info("Market {} not in cache.  Ignore".format(market_id))
        else:
            market = self._markets[market_id]
            market.update(market_change)

            # remove market from cache if closed
            if market.market_def.status == MarketStatus.CLOSED:
                logging.info("Market %s is closed.  Removing from cache" % market_id)
                self._markets.pop(market_id)

    def formatted_string(self, market_id: str):
        if market_id not in self._markets:
            return ""

        ladder_format = '{:<15} {:<50} {:>50}\n'

        market = self._markets[market_id]
        market_status = market.market_def.status

        if market_status == MarketStatus.CLOSED or not hasattr(market, "rc"):
            return ""

        market_result = "Market {} (£{}) - {}\n".format(market_id, format_value(market.tv), market_status)

        runner_changes = market.rc

        for runner_id, runner_change in runner_changes.items():
            if market.market_def.runners[runner_id].status != Runner.RunnerStatus.ACTIVE \
                    or not hasattr(runner_change, "bdatb") or runner_change.bdatb.size() < 3 \
                    or not hasattr(runner_change, "bdatl") or runner_change.bdatl.size() < 3:
                continue

            bdatb = runner_change.bdatb.price_list[:3][::-1]
            bdatl = runner_change.bdatl.price_list[:3]

            back_price_vol_format = '{:>12}' * len(bdatb)
            lay_price_vol_format = '{:<12}' * len(bdatl)

            bdatb_prices = back_price_vol_format.format(*[p.price for p in bdatb])
            bdatl_prices = lay_price_vol_format.format(*[p.price for p in bdatl])
            bdatb_sizes = back_price_vol_format.format(*['£' + str(p.vol) for p in bdatb])
            bdatl_sizes = lay_price_vol_format.format(*['£' + str(p.vol) for p in bdatl])

            market_result += ladder_format.format("Runner " + str(runner_change.id), bdatb_prices, bdatl_prices)
            market_result += ladder_format.format("£" + format_value(runner_change.tv), bdatb_sizes, bdatl_sizes)

        return market_result + '\n'

    @property
    def markets(self):
        return self._markets

    def get_market(self, market_id):
        return self._markets[market_id]

    def __repr__(self):
        return str(vars(self))
