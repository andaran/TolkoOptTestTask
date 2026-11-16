import asyncio
import unittest
from decimal import Decimal

from starter import recommend_price, sample_fetch_offers


class RecommendPriceTests(unittest.IsolatedAsyncioTestCase):
    async def test_standard_calculation(self):
        result = await recommend_price(
            sample_fetch_offers,
            current_price=Decimal("4900.00"),
            min_price=Decimal("4500.00"),
        )

        self.assertEqual(result["price"], Decimal("4728.00"))
        self.assertEqual(result["decision"], "APPLY")

    async def test_timeout_keeps_current_price(self):
        async def slow_fetch_offers():
            await asyncio.Event().wait()

        current_price = Decimal("4900.00")
        result = await recommend_price(
            slow_fetch_offers,
            current_price=current_price,
            min_price=Decimal("4500.00"),
            timeout_s=0.01,
        )

        self.assertEqual(result["price"], current_price)
        self.assertEqual(result["decision"], "HOLD")


if __name__ == "__main__":
    unittest.main()
