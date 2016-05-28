from unittest import TestCase

from client.cache.cache import Cache
from client.domain.marketchange.marketchange import MarketChange
from client.domain.marketchange.marketstatus import MarketStatus


class TestCache(TestCase):
    def setUp(self):
        self.cache = Cache()

    def test_on_receive_receiveClosedMarket_notAdded(self):
        market_change = TestCache.create_market_change_with_status(MarketStatus.CLOSED)
        market_changes = [market_change]
        self.cache.on_receive(market_changes)

        self.assertEqual(len(self.cache.markets), 0)

    def test_on_receive_receiveOpenMarket_added(self):
        market_change = TestCache.create_market_change_with_status(MarketStatus.OPEN)
        market_changes = [market_change]
        self.cache.on_receive(market_changes)

        self.assertEqual(len(self.cache.markets), 1)

    def test_on_receive_receiveImgWithCosedMarket_removeFromCache(self):
        market_change = TestCache.create_market_change_with_status(MarketStatus.OPEN)
        market_changes = [market_change]
        self.cache.on_receive(market_changes)

        self.assertEqual(len(self.cache.markets), 1)

        # create an update to close the market (with the same market id)
        market_change = TestCache.create_market_change_with_status(MarketStatus.CLOSED)
        market_changes = [market_change]
        self.cache.on_receive(market_changes)

        self.assertEqual(len(self.cache.markets), 0)

    def test_on_receive_marketBecomesClosed_removeFromCache(self):
        market_change = TestCache.create_market_change_with_status(MarketStatus.OPEN)
        market_changes = [market_change]
        self.cache.on_receive(market_changes)

        self.assertEqual(len(self.cache.markets), 1)

        # not img -> remove from cache when updating
        market_change = TestCache.create_market_change_with_img_and_status(False, MarketStatus.CLOSED)
        market_changes = [market_change]
        self.cache.on_receive(market_changes)

        self.assertEqual(len(self.cache.markets), 0)

    def test_on_receive_receiveNonImgClosedMarket_ignore(self):
        market_change = TestCache.create_market_change_with_img_and_status(False, MarketStatus.CLOSED)
        market_changes = [market_change]
        self.cache.on_receive(market_changes)

        self.assertEqual(len(self.cache.markets), 0)

    def test_get_market_marketNotExist_returnNone(self):
        market = self.cache.get_market("abc")

        self.assertEqual(market, None)

    def test_get_market_marketExists_returnMarket(self):
        market_change = TestCache.create_market_change_with_status(MarketStatus.OPEN)
        market_changes = [market_change]
        market_id = market_change.id

        self.cache.on_receive(market_changes)
        market = self.cache.get_market(market_id)

        self.assertEqual(market, market_change)

    @staticmethod
    def create_market_change_with_img_and_status(img: bool, status: MarketStatus):
        return MarketChange({"id": 5, "img": img, "marketDefinition": {"status": status.name}})

    @staticmethod
    def create_market_change_with_status(status: MarketStatus):
        return TestCache.create_market_change_with_img_and_status(True, status)
