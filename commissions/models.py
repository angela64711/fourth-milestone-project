import uuid

from django.conf import settings
from django.db import models


class CommissionOrder(models.Model):
    """
    Stores a bespoke artwork commission, including creative preferences,
    customer details, pricing and payment status.
    """

    # Choices are stored using their identifiers, while Django displays
    # the corresponding human-readable labels.

    CREATIVE_DIRECTION_CHOICES = [
        ("idea", "Give form to a thought"),
        ("surprise", "Be surprised"),
    ]

    MOOD_CHOICES = [
        ("dreamlike", "Dreamlike"),
        ("romantic", "Romantic"),
        ("nostalgic", "Nostalgic"),
        ("mysterious", "Mysterious"),
        ("hopeful", "Hopeful"),
        ("serene", "Serene"),
        ("melancholic", "Melancholic"),
        ("futuristic", "Futuristic"),
    ]

    COLOUR_CHOICES = [
        ("pink", "Pink"),
        ("red", "Red"),
        ("purple", "Purple"),
        ("blue", "Blue"),
        ("blue_grey", "Blue-Grey"),
        ("sage_green", "Sage Green"),
        ("olive_green", "Olive Green"),
        ("yellow", "Yellow"),
        ("terracotta", "Terracotta"),
        ("off_white", "Off-White"),
        ("beige", "Beige"),
        ("black_white", "Black & White"),
    ]

    IMAGERY_CHOICES = [
        ("nature", "Nature & Botanicals"),
        ("classical", "Classical & Sculptural"),
        ("cosmic", "Cosmic & Surreal"),
        ("human", "Human & Nostalgic"),
    ]

    FORMAT_CHOICES = [
        ("digital", "Digital Collage"),
        ("print", "Fine Art Print"),
        ("framed", "Framed Artwork"),
    ]

    SIZE_CHOICES = [
        ("30x40", "30 × 40 cm"),
        ("50x70", "50 × 70 cm"),
    ]

    DELIVERY_REGION_CHOICES = [
        ("europe_uk", "Europe & UK"),
        ("international", "USA, Australia & Rest of the World"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
        ("cancelled", "Cancelled"),
    ]

    # Creative preferences

    creative_direction = models.CharField(
        max_length=20,
        choices=CREATIVE_DIRECTION_CHOICES,
    )

    # Optional for "Be surprised"; required for "Give form to a thought".
    # Conditional validation will be handled by the commission form.
    story = models.TextField(
        max_length=1000,
        blank=True,
    )

    # JSONField stores multiple selections as Python lists.
    # The form will validate allowed values and require 1–2 selections.
    moods = models.JSONField(default=list)
    colours = models.JSONField(default=list)

    imagery = models.CharField(
        max_length=20,
        choices=IMAGERY_CHOICES,
    )

    # Artwork format and delivery

    artwork_format = models.CharField(
        max_length=20,
        choices=FORMAT_CHOICES,
    )

    # Digital artwork requires neither physical dimensions nor shipping.
    artwork_size = models.CharField(
        max_length=10,
        choices=SIZE_CHOICES,
        blank=True,
    )

    delivery_region = models.CharField(
        max_length=20,
        choices=DELIVERY_REGION_CHOICES,
        blank=True,
    )

    # Order pricing
    # Store the agreed amounts so later price changes don't affect
    # existing orders. DecimalField avoids floating-point inaccuracies.
    artwork_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )

    shipping_cost = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
    )

    total_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )

    # Customer information

    # Every commission belongs to a registered user.
    # PROTECT prevents deleting a user who has associated orders.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="commission_orders",
    )

    # Store contact details with each order, independently of changes
    # to the customer's account information.
    full_name = models.CharField(max_length=150)
    email = models.EmailField()

    # Shipping information is optional for digital commissions.
    # Physical orders will require these fields during form validation.
    shipping_address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)

    # Order and payment tracking

    # uuid4 generates a random unique order reference.
    # Passing the function without () generates a new UUID per order.
    order_number = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    # Orders remain pending until Stripe payment is verified.
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="pending",
    )

    # Stripe's PaymentIntent ID links our order to its payment.
    stripe_payment_intent = models.CharField(
        max_length=255,
        blank=True,
    )

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Commission {self.order_number} - {self.full_name}"
