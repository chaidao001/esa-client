import logging

from ..domain.marketchange.marketchange import MarketChange
from ..domain.marketchange.marketstatus import MarketStatus

market_logger = logging.getLogger('marketData')

class Cache:
    def __init__(self):
        self.markets = dict()

    def on_receive(self, market_changes: list()):
        for market_change in market_changes:
            if market_change.img:
                self._process_market_img(market_change)
            else:
                self._update_market(market_change)

            market_id = market_change.id
            if market_id in self.markets:
                market_logger.info(self.markets[market_id])

    def _process_market_img(self, market_change: MarketChange):
        market_id = market_change.id

        if market_change.market_definition.status == MarketStatus.CLOSED:
            # remove if full img and already in cache
            if market_id in self.markets:
                logging.info("Market %s is closed.  Removing from cache" % market_id)
                self.markets.pop(market_id)
            else:
                logging.info("Market %s is closed.  Ignore image" % market_id)
        else:
            self.markets[market_id] = market_change

    def _update_market(self, market_change: MarketChange):
        market_id = market_change.id

        if market_id in self.markets:
            market = self.markets[market_id]
            market.update(market_change)

            # remove market from cache if closed
            if market.market_definition.status == MarketStatus.CLOSED:
                logging.info("Market %s is closed.  Removing from cache" % market_id)
                self.markets.pop(market_id)
        else:
            logging.info("Market %s not in cache.  Ignore" % market_id)

    @property
    def market_ids(self):
        return self.markets.keys()

    def get_market(self, market_id):
        if market_id in self.markets:
            return self.markets[market_id]

    def __iter__(self):
        return self.markets

    def __len__(self):
        return len(self.markets)

    def __repr__(self):
        return str(vars(self))
