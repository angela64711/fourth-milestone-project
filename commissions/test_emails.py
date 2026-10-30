from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings

from .emails import send_confirmation_email
from .models import CommissionOrder


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="frankmoth@example.com",
)
class CommissionConfirmationEmailTest(TestCase):
    """Tests commission confirmation email content and delivery."""

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="emailcustomer",
            email="account@example.com",
            password="testpass123",
        )

    def setUp(self):
        self.order = CommissionOrder.objects.create(
            user=self.user,
            creative_direction="idea",
            story="A dreamlike landscape with classical elements.",
            moods=["dreamlike", "nostalgic"],
            colours=["blue", "pink"],
            imagery="classical",
            artwork_format="print",
            artwork_size="30x40",
            delivery_region="europe_uk",
            artwork_price=Decimal("200.00"),
            shipping_cost=Decimal("15.00"),
            total_price=Decimal("215.00"),
            full_name="Test Customer",
            email="checkout@example.com",
            shipping_address="Example Street 12",
            city="Berlin",
            postal_code="10115",
            country="Germany",
            payment_status="paid",
        )

    def test_paid_order_sends_confirmation_email(self):
        """A paid commission sends one email to the checkout address."""
        result = send_confirmation_email(self.order)

        self.order.refresh_from_db()

        self.assertTrue(result)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].to,
            ["checkout@example.com"],
        )
        self.assertTrue(self.order.confirmation_email_sent)

    def test_email_contains_order_details(self):
        """The email includes the order reference, choices and payment."""
        send_confirmation_email(self.order)

        email = mail.outbox[0]

        self.assertIn(
            str(self.order.order_number),
            email.subject,
        )
        self.assertIn(
            str(self.order.order_number),
            email.body,
        )
        self.assertIn("Fine Art Print", email.body)
        self.assertIn("30 × 40 cm", email.body)
        self.assertIn(
            "A dreamlike landscape with classical elements.",
            email.body,
        )
        self.assertIn("Dreamlike", email.body)
        self.assertIn("Nostalgic", email.body)
        self.assertIn("Navy Blue", email.body)
        self.assertIn("Dusty Rose", email.body)
        self.assertIn("Classical & Sculptural", email.body)
        self.assertIn("€200.00", email.body)
        self.assertIn("€15.00", email.body)
        self.assertIn("€215.00", email.body)
        self.assertIn("Payment status: Paid", email.body)
        self.assertIn("Example Street 12", email.body)
        self.assertIn("10115 Berlin", email.body)
        self.assertIn("Germany", email.body)

    def test_confirmation_email_is_not_sent_twice(self):
        """Repeated calls do not send another confirmation email."""
        first_result = send_confirmation_email(self.order)
        second_result = send_confirmation_email(self.order)

        self.order.refresh_from_db()

        self.assertTrue(first_result)
        self.assertFalse(second_result)
        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue(self.order.confirmation_email_sent)

    def test_unpaid_order_does_not_send_email(self):
        """A pending payment cannot trigger a confirmation email."""
        self.order.payment_status = "pending"
        self.order.save(update_fields=["payment_status"])

        result = send_confirmation_email(self.order)

        self.order.refresh_from_db()

        self.assertFalse(result)
        self.assertEqual(len(mail.outbox), 0)
        self.assertFalse(self.order.confirmation_email_sent)

    def test_surprise_order_email_omits_empty_preferences(self):
        """Surprise commissions do not display empty creative fields."""
        self.order.creative_direction = "surprise"
        self.order.story = ""
        self.order.moods = []
        self.order.colours = []
        self.order.imagery = ""
        self.order.artwork_format = "digital"
        self.order.artwork_size = ""
        self.order.shipping_address = ""
        self.order.save()

        result = send_confirmation_email(self.order)

        self.assertTrue(result)
        self.assertEqual(len(mail.outbox), 1)

        body = mail.outbox[0].body

        self.assertIn("Let us surprise you", body)
        self.assertIn("Digital Collage", body)
        self.assertNotIn("Your story:", body)
        self.assertNotIn("Moods:", body)
        self.assertNotIn("Colours:", body)
        self.assertNotIn("Imagery:", body)
        self.assertNotIn("SHIPPING ADDRESS", body)

    @patch("commissions.emails.send_mail")
    def test_email_failure_does_not_change_payment_status(self, mock_send):
        """An email error leaves the paid order intact."""
        mock_send.side_effect = ConnectionError("Email server unavailable")

        result = send_confirmation_email(self.order)

        self.order.refresh_from_db()

        self.assertFalse(result)
        self.assertEqual(self.order.payment_status, "paid")
        self.assertFalse(self.order.confirmation_email_sent)
        mock_send.assert_called_once()
