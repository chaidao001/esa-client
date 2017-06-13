import logging

from ..domain.marketchange.marketchange import MarketChange
from ..domain.marketchange.marketstatus import MarketStatus

market_logger = logging.getLogger('marketData')

class Cache:
    def __init__(self):
        self._markets = dict()

    def on_receive(self, market_changes: list()):
        for market_change in market_changes:
            if market_change.img:
                self._process_market_img(market_change)
            else:
                self._update_market(market_change)

            market_id = market_change.id
            if market_id in self._markets:
                market_logger.info(self._markets[market_id])

    def _process_market_img(self, market_change: MarketChange):
        market_id = market_change.id

        if market_change.market_definition.status == MarketStatus.CLOSED:
            # remove if full img and already in cache
            if market_id in self._markets:
                logging.info("Market %s is closed.  Removing from cache" % market_id)
                self._markets.pop(market_id)
            else:
                logging.info("Market %s is closed.  Ignore image" % market_id)
        else:
            self._markets[market_id] = market_change

    def _update_market(self, market_change: MarketChange):
        market_id = market_change.id

        if market_id in self._markets:
            market = self._markets[market_id]
            market.update(market_change)

            # remove market from cache if closed
            if market.market_definition.status == MarketStatus.CLOSED:
                logging.info("Market %s is closed.  Removing from cache" % market_id)
                self._markets.pop(market_id)
        else:
            logging.info("Market %s not in cache.  Ignore" % market_id)

    @property
    def markets(self):
        return self._markets

    @property
    def market_ids(self):
        return self._markets.keys()

    def get_market(self, market_id):
        if market_id in self._markets:
            return self._markets[market_id]

    def __iter__(self):
        return self._markets

    def __len__(self):
        return len(self._markets)

    def __repr__(self):
        return str(vars(self))
