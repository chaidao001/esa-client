from unittest import TestCase

from client.domain.marketchange.marketchange import MarketChange


class TestMarketChange(TestCase):
    def test_update_updateMarketChangeWhenEmptyBefore_addToCache(self):
        market_change = TestMarketChange.create_market_change()
        incoming_market_change = TestMarketChange.create_market_change_with_runner_change("111")
        self.assertEqual(len(market_change.rc), 0)

        market_change.update(incoming_market_change)

        self.assertEqual(len(market_change.rc), 1)

    def test_update_receiveUpdateOnNewMarket_addToCache(self):
        market_change = TestMarketChange.create_market_change_with_runner_change("111")
        incoming_market_change = TestMarketChange.create_market_change_with_runner_change("222")
        self.assertEqual(len(market_change.rc), 1)

        market_change.update(incoming_market_change)

        self.assertEqual(len(market_change.rc), 2)

    def test_update_receiveUpdateOnExistingMarket_updateCorrectly(self):
        runner_id = "111"
        market_change = TestMarketChange.create_market_change_with_runner_change_and_spn(runner_id, 5)
        incoming_market_change = TestMarketChange.create_market_change_with_runner_change_and_spn(runner_id, 6)
        self.assertEqual(len(market_change.rc), 1)
        self.assertEqual(market_change.rc[runner_id].spn, 5)

        market_change.update(incoming_market_change)

        self.assertEqual(len(market_change.rc), 1)
        self.assertEqual(market_change.rc[runner_id].spn, 6)

    def test_init_imgNotInResponse_returnFalse(self):
        market_change = TestMarketChange.create_market_change()

        self.assertEqual(market_change.img, False)

    def test_init_imgInResponse_returnTrue(self):
        market_change = TestMarketChange.create_market_change_with_img()

        self.assertEqual(market_change.img, True)

    @staticmethod
    def create_market_change():
        return MarketChange({"id": 5})

    @staticmethod
    def create_market_change_with_img():
        return MarketChange({"id": 5, "img": True})

    @staticmethod
    def create_market_change_with_runner_change(runner_id):
        return TestMarketChange.create_market_change_with_runner_change_and_spn(runner_id, 5)

    @staticmethod
    def create_market_change_with_runner_change_and_spn(runner_id, spn):
        return MarketChange({"id": 5, "rc": [{"id": runner_id, "spn": spn}]})
