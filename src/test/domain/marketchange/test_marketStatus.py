from unittest import TestCase

from client.domain.marketchange.marketstatus import MarketStatus


class TestMarketStatus(TestCase):
    def test_MarketStatus_createMarketStatusFromString_createdCorrectly(self):
        self.assertEqual(MarketStatus["OPEN"], MarketStatus.OPEN)

        self.assertEqual(MarketStatus["CLOSED"], MarketStatus.CLOSED)
