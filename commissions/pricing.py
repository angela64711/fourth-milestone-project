"""
Commission artwork prices and shipping calculations.

All amounts are in EUR. These functions are also used
when creating orders, so browser values cannot determine
the amount charged.
"""

from decimal import Decimal

ARTWORK_PRICES = {
    ("digital", ""): Decimal("180.00"),
    ("print", "30x40"): Decimal("200.00"),
    ("print", "50x70"): Decimal("220.00"),
    ("framed", "30x40"): Decimal("260.00"),
    ("framed", "50x70"): Decimal("300.00"),
}

SHIPPING_PRICES = {
    "print": {
        "europe_uk": Decimal("15.00"),
        "international": Decimal("30.00"),
    },
    "framed": {
        "europe_uk": Decimal("25.00"),
        "international": Decimal("50.00"),
    },
}


def get_artwork_price(artwork_format, artwork_size=""):
    """Return the price for a valid format and size."""

    try:
        return ARTWORK_PRICES[(artwork_format, artwork_size)]
    except KeyError:
        raise ValueError("Invalid artwork format or size.") from None


def get_shipping_cost(artwork_format, delivery_region=""):
    """
    Return shipping cost for the selected delivery region.

    Digital commissions have no shipping cost.
    Physical commissions require a valid delivery region.
    """

    if artwork_format == "digital":
        return Decimal("0.00")

    try:
        return SHIPPING_PRICES[artwork_format][delivery_region]
    except KeyError:
        raise ValueError("Invalid artwork format or delivery region.") from None


def calculate_commission_total(
    artwork_format,
    artwork_size="",
    delivery_region="",
):
    """Calculate the authoritative commission amounts."""

    artwork_price = get_artwork_price(
        artwork_format,
        artwork_size,
    )

    shipping_cost = get_shipping_cost(
        artwork_format,
        delivery_region,
    )

    return {
        "artwork_price": artwork_price,
        "shipping_cost": shipping_cost,
        "total_price": artwork_price + shipping_cost,
    }
