import logging

from django.conf import settings
from django.core.mail import send_mail

from .models import CommissionOrder

logger = logging.getLogger(__name__)


def send_confirmation_email(order):
    """Send a confirmation email for a paid commission order."""

    if order.payment_status != "paid" or order.confirmation_email_sent:
        return False

    # Converts stored choice values into readable labels.
    mood_labels = dict(CommissionOrder.MOOD_CHOICES)
    colour_labels = dict(CommissionOrder.COLOUR_CHOICES)

    moods = ", ".join(mood_labels.get(mood, mood) for mood in order.moods)
    colours = ", ".join(colour_labels.get(colour, colour) for colour in order.colours)

    # Builds the email from the saved order information.
    lines = [
        f"Dear {order.full_name},",
        "",
        "Thank you for commissioning an artwork from Frank Moth!",
        "Your payment has been received successfully.",
        "",
        "ORDER DETAILS",
        f"Order number: {order.order_number}",
        f"Artwork format: {order.get_artwork_format_display()}",
    ]

    if order.artwork_size:
        lines.append(f"Artwork size: {order.get_artwork_size_display()}")

    lines.extend(
        [
            "",
            "CREATIVE PREFERENCES",
            f"Creative direction: {order.get_creative_direction_display()}",
        ]
    )

    if order.story:
        lines.append(f"Your story: {order.story}")

    if moods:
        lines.append(f"Moods: {moods}")

    if colours:
        lines.append(f"Colours: {colours}")

    if order.imagery:
        lines.append(f"Imagery: {order.get_imagery_display()}")

    lines.extend(
        [
            "",
            "PAYMENT SUMMARY",
            f"Artwork price: €{order.artwork_price:.2f}",
            f"Shipping: €{order.shipping_cost:.2f}",
            f"Total paid: €{order.total_price:.2f}",
            "Payment status: Paid",
        ]
    )

    if order.artwork_format != "digital":
        lines.extend(
            [
                "",
                "SHIPPING ADDRESS",
                order.full_name,
                order.shipping_address,
                f"{order.postal_code} {order.city}",
                order.country,
            ]
        )

    lines.extend(
        [
            "",
            "The artist will contact you when your artwork is ready.",
            "",
            "Thank you for being part of our creative journey. We're excited to create something special for you.",
            "Frank Moth",
        ]
    )

    message = "\n".join(lines)

    try:
        send_mail(
            subject=f"Frank Moth - Order Confirmation {order.order_number}",
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.email],
            fail_silently=False,
        )
    except Exception:
        logger.exception(
            "Failed to send confirmation email for order %s",
            order.order_number,
        )
        return False

    order.confirmation_email_sent = True
    order.save(update_fields=["confirmation_email_sent", "updated_on"])

    return True
