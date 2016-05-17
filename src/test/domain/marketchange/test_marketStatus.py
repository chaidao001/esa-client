from unittest import TestCase

from client.domain.marketchange.marketstatus import MarketStatus


class TestMarketStatus(TestCase):
    def test_create_market_status_from_string(self):
        self.assertEqual(MarketStatus["OPEN"], MarketStatus.OPEN)

        self.assertEqual(MarketStatus["CLOSED"], MarketStatus.CLOSED)
