from decimal import Decimal

from django.test import SimpleTestCase

from .pricing import (
    calculate_commission_total,
    get_artwork_price,
    get_shipping_cost,
)


class CommissionPricingTest(SimpleTestCase):
    """Tests server-side commission pricing calculations."""

    def test_artwork_prices(self):
        """Each format and size has the correct artwork price."""
        prices = [
            ("digital", "", "180.00"),
            ("print", "30x40", "200.00"),
            ("print", "50x70", "220.00"),
            ("framed", "30x40", "260.00"),
            ("framed", "50x70", "300.00"),
        ]

        for artwork_format, size, expected in prices:
            with self.subTest(format=artwork_format, size=size):
                self.assertEqual(
                    get_artwork_price(artwork_format, size),
                    Decimal(expected),
                )

    def test_shipping_prices(self):
        """Shipping depends on format and delivery region."""
        prices = [
            ("print", "europe_uk", "15.00"),
            ("print", "international", "30.00"),
            ("framed", "europe_uk", "25.00"),
            ("framed", "international", "50.00"),
        ]

        for artwork_format, region, expected in prices:
            with self.subTest(format=artwork_format, region=region):
                self.assertEqual(
                    get_shipping_cost(artwork_format, region),
                    Decimal(expected),
                )

    def test_digital_shipping_is_free(self):
        """Digital commissions have no shipping cost."""
        self.assertEqual(
            get_shipping_cost("digital"),
            Decimal("0.00"),
        )

    def test_commission_totals(self):
        """Total price equals artwork price plus shipping."""
        cases = [
            ("digital", "", "", "180.00"),
            ("print", "30x40", "europe_uk", "215.00"),
            ("print", "50x70", "international", "250.00"),
            ("framed", "30x40", "europe_uk", "285.00"),
            ("framed", "50x70", "international", "350.00"),
        ]

        for artwork_format, size, region, expected in cases:
            with self.subTest(
                format=artwork_format,
                size=size,
                region=region,
            ):
                result = calculate_commission_total(artwork_format, size, region)

                self.assertEqual(
                    result["total_price"],
                    Decimal(expected),
                )
                self.assertEqual(
                    result["total_price"],
                    result["artwork_price"] + result["shipping_cost"],
                )

    def test_invalid_artwork_format_or_size(self):
        """Unsupported artwork combinations raise ValueError."""
        invalid_cases = [
            ("invalid", ""),
            ("print", ""),
            ("framed", "invalid"),
            ("digital", "30x40"),
        ]

        for artwork_format, size in invalid_cases:
            with self.subTest(format=artwork_format, size=size):
                with self.assertRaises(ValueError):
                    get_artwork_price(artwork_format, size)

    def test_invalid_shipping_options(self):
        """Unsupported shipping combinations raise ValueError."""
        invalid_cases = [
            ("print", ""),
            ("print", "invalid"),
            ("framed", ""),
            ("invalid", "europe_uk"),
        ]

        for artwork_format, region in invalid_cases:
            with self.subTest(format=artwork_format, region=region):
                with self.assertRaises(ValueError):
                    get_shipping_cost(artwork_format, region)
