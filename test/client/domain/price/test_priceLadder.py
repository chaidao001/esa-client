from unittest import TestCase

from src.client.domain.price.priceladder import PriceLadder
from src.client.domain.price.pricevol import PriceVol


class TestPriceLadder(TestCase):
    def setUp(self):
        self.price_ladder = PriceLadder([[0, 1, 2], [3, 4, 5]])

    def test_update_update_updateCorrectly(self):
        incoming_price_ladder = PriceLadder([[0, 6, 7], [8, 9, 10]])
        self.price_ladder.update(incoming_price_ladder)

        self.assertEqual(len(self.price_ladder), 3)
        self.assertEqual(self.price_ladder, PriceLadder([[0, 6, 7], [3, 4, 5], [8, 9, 10]]))

    def test_update_updateZeros_removeZeroValues(self):
        incoming_price_ladder = PriceLadder([[0, 6, 0], [8, 9, 10]])
        self.price_ladder.update(incoming_price_ladder)

        self.assertEqual(len(self.price_ladder), 2)
        self.assertEqual(self.price_ladder, PriceLadder([[3, 4, 5], [8, 9, 10]]))

    def test_price_list_emptyLadder_returnEmptyList(self):
        self.price_ladder = PriceLadder(list())

        self.assertEqual(self.price_ladder.price_list, list())

    def test_price_list_nonEmptyLadder_returnNonEmptyList(self):
        self.assertEqual(self.price_ladder.price_list, [PriceVol([1, 2]), PriceVol([4, 5])])

    def test_price_list_NotOrderedLadder_returnOrderedList(self):
        self.price_ladder = PriceLadder([[0, 1, 2], [9, 10, 11], [3, 4, 5]])
        self.assertEqual(self.price_ladder.price_list, [PriceVol([1, 2]), PriceVol([4, 5]), PriceVol([10, 11])])

    def test_size_emptyLadder_returnZero(self):
        self.price_ladder = PriceLadder(list())

        self.assertEqual(len(self.price_ladder), 0)

    def test_size_nonEmptyLadder_returnSize(self):
        self.assertEqual(len(self.price_ladder), 2)

    def test_get_price_at_position_returnPriceCorrectly(self):
        price = self.price_ladder.get_price_at_position(0)

        self.assertEqual(price, PriceVol([1, 2]))
