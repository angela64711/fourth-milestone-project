from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

import stripe

from .models import CommissionOrder


@override_settings(
    STORAGES={
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
)
class CommissionCreativeViewTest(TestCase):
    """Tests the creative preferences view and session handling."""

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testcustomer",
            email="customer@example.com",
            password="testpass123",
        )

    def setUp(self):
        self.url = reverse("commissions:creative")

    def valid_form_data(self):
        """Return valid creative preferences for testing."""
        return {
            "creative_direction": "idea",
            "story": "A dreamlike landscape with classical elements.",
            "moods": ["dreamlike", "nostalgic"],
            "colours": ["blue", "pink"],
            "imagery": "classical",
            "artwork_format": "digital",
        }

    def test_creative_page_loads_for_anonymous_user(self):
        """Visitors can view the commission form."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "commissions/commission.html",
        )

    def test_anonymous_user_cannot_submit(self):
        """Unauthenticated submissions are forbidden."""
        response = self.client.post(
            self.url,
            self.valid_form_data(),
        )

        self.assertEqual(response.status_code, 403)
        self.assertNotIn(
            "commission_creative",
            self.client.session,
        )

    def test_invalid_submission_does_not_save_session(self):
        """Invalid preferences are not stored in the session."""
        self.client.force_login(self.user)

        data = self.valid_form_data()
        data["story"] = ""

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("story", response.context["form"].errors)
        self.assertNotIn(
            "commission_creative",
            self.client.session,
        )

    def test_valid_submission_saves_session_and_redirects(self):
        """Valid preferences are saved before customer details."""
        self.client.force_login(self.user)

        response = self.client.post(
            self.url,
            self.valid_form_data(),
        )

        self.assertRedirects(
            response,
            reverse("commissions:customer_details"),
        )

        saved = self.client.session["commission_creative"]

        self.assertEqual(saved["creative_direction"], "idea")
        self.assertEqual(
            saved["moods"],
            ["dreamlike", "nostalgic"],
        )
        self.assertEqual(
            saved["artwork_format"],
            "digital",
        )

    def test_saved_preferences_restored_on_get(self):
        """Returning to the form restores session preferences."""
        self.client.force_login(self.user)

        self.client.post(
            self.url,
            self.valid_form_data(),
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["form"].initial["creative_direction"],
            "idea",
        )
        self.assertEqual(
            response.context["form"].initial["colours"],
            ["blue", "pink"],
        )


@override_settings(
    STORAGES={
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
)
class CommissionCustomerViewTest(TestCase):
    """Tests customer details, sessions and server-side pricing."""

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testcustomer2",
            email="customer@example.com",
            password="testpass123",
            first_name="Test",
            last_name="Customer",
        )

    def setUp(self):
        self.url = reverse("commissions:customer_details")
        self.client.force_login(self.user)

    def set_creative_session(self, artwork_format="digital", artwork_size=""):
        """Store valid creative preferences in the test session."""
        session = self.client.session
        session["commission_creative"] = {
            "creative_direction": "idea",
            "story": "A dreamlike landscape.",
            "moods": ["dreamlike"],
            "colours": ["blue"],
            "imagery": "classical",
            "artwork_format": artwork_format,
            "artwork_size": artwork_size,
        }
        session.save()

    def valid_customer_data(self, **overrides):
        """Return complete customer and shipping details."""
        data = {
            "first_name": "Test",
            "last_name": "Customer",
            "email": "customer@example.com",
            "delivery_region": "europe_uk",
            "street": "Example Street",
            "house_number": "12",
            "address_line_2": "",
            "city": "Berlin",
            "postal_code": "10115",
            "country": "Germany",
        }
        data.update(overrides)
        return data

    def test_anonymous_user_redirected_to_login(self):
        """Customer details require authentication."""
        self.client.logout()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_missing_creative_session_redirects(self):
        """Users cannot skip the creative preferences step."""
        response = self.client.get(self.url)

        self.assertRedirects(
            response,
            reverse("commissions:creative"),
        )

    def test_invalid_creative_session_redirects(self):
        """Unsupported artwork selections are rejected."""
        self.set_creative_session(
            artwork_format="invalid",
        )

        response = self.client.get(self.url)

        self.assertRedirects(
            response,
            reverse("commissions:creative"),
        )

    def test_digital_customer_page_shows_correct_price(self):
        """Digital commissions display their server-calculated price."""
        self.set_creative_session()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "commissions/customer_details.html",
        )
        self.assertEqual(response.context["artwork_price"], 180)
        self.assertEqual(response.context["shipping_cost"], 0)
        self.assertEqual(response.context["total_price"], 180)
        self.assertFalse(response.context["requires_shipping"])

    def test_physical_customer_page_shows_shipping_options(self):
        """Physical commissions display their available shipping prices."""
        self.set_creative_session(
            artwork_format="print",
            artwork_size="30x40",
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["requires_shipping"])
        self.assertEqual(response.context["artwork_price"], 200)
        self.assertEqual(response.context["europe_shipping"], 15)
        self.assertEqual(response.context["international_shipping"], 30)
        self.assertIsNone(response.context["total_price"])

    def test_valid_digital_submission_saves_customer_session(self):
        """Valid contact details are saved without shipping information."""
        self.set_creative_session()

        response = self.client.post(
            self.url,
            self.valid_customer_data(),
        )

        self.assertRedirects(
            response,
            reverse("commissions:checkout"),
            fetch_redirect_response=False,
        )

        saved = self.client.session["commission_customer"]

        self.assertEqual(saved["full_name"], "Test Customer")
        self.assertEqual(saved["email"], "customer@example.com")
        self.assertEqual(saved["shipping_address"], "")
        self.assertEqual(saved["delivery_region"], "")
        self.assertEqual(saved["country"], "")

    def test_valid_physical_submission_combines_shipping_address(self):
        """Physical orders retain shipping details and combine the address."""
        self.set_creative_session(
            artwork_format="framed",
            artwork_size="50x70",
        )

        response = self.client.post(
            self.url,
            self.valid_customer_data(
                address_line_2="Apartment 4",
            ),
        )

        self.assertRedirects(
            response,
            reverse("commissions:checkout"),
            fetch_redirect_response=False,
        )

        saved = self.client.session["commission_customer"]

        self.assertEqual(
            saved["shipping_address"],
            "Example Street 12\nApartment 4",
        )
        self.assertEqual(saved["delivery_region"], "europe_uk")
        self.assertEqual(saved["city"], "Berlin")
        self.assertEqual(saved["country"], "Germany")

    def test_invalid_physical_submission_does_not_save_session(self):
        """Missing shipping details prevent saving customer information."""
        self.set_creative_session(
            artwork_format="print",
            artwork_size="30x40",
        )

        response = self.client.post(
            self.url,
            self.valid_customer_data(postal_code=""),
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("postal_code", response.context["form"].errors)
        self.assertNotIn(
            "commission_customer",
            self.client.session,
        )


@override_settings(
    STRIPE_CURRENCY="eur",
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="frankmoth@example.com",
    STORAGES={
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    },
)
class CommissionPaymentVerificationTest(TestCase):
    """Tests Stripe payment verification and confirmation emails."""

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="paymentcustomer",
            email="payment@example.com",
            password="testpass123",
        )

    def setUp(self):
        self.client.force_login(self.user)

        self.order = CommissionOrder.objects.create(
            user=self.user,
            creative_direction="surprise",
            artwork_format="digital",
            artwork_price=Decimal("180.00"),
            shipping_cost=Decimal("0.00"),
            total_price=Decimal("180.00"),
            full_name="Payment Customer",
            email="payment@example.com",
            stripe_payment_intent="pi_test_success",
        )

    def successful_payment(self):
        """Return a matching, successful Stripe test payment."""
        return stripe.StripeObject.construct_from(
            {
                "id": "pi_test_success",
                "amount": 18000,
                "currency": "eur",
                "status": "succeeded",
                "metadata": {
                    "order_number": str(self.order.order_number),
                },
            },
            "sk_test_mock",
        )

    @patch("commissions.views.stripe.PaymentIntent.retrieve")
    def test_successful_payment_marks_order_paid(self, mock_retrieve):
        """A verified payment marks the order paid and sends confirmation."""
        mock_retrieve.return_value = self.successful_payment()

        response = self.client.post(
            reverse(
                "commissions:verify_payment",
                args=[self.order.order_number],
            )
        )

        self.order.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        self.assertEqual(self.order.payment_status, "paid")
        self.assertEqual(
            response.json()["redirect_url"],
            reverse(
                "commissions:success",
                args=[self.order.order_number],
            ),
        )
        mock_retrieve.assert_called_once_with("pi_test_success")

        # The payment view must trigger the confirmation email.
        self.assertTrue(self.order.confirmation_email_sent)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].to,
            ["payment@example.com"],
        )
        self.assertIn(
            str(self.order.order_number),
            mail.outbox[0].subject,
        )

    @patch("commissions.views.stripe.PaymentIntent.retrieve")
    def test_incomplete_payment_remains_pending(self, mock_retrieve):
        """An incomplete payment must not send a confirmation email."""
        mock_retrieve.return_value = stripe.StripeObject.construct_from(
            {
                "id": "pi_test_success",
                "amount": 18000,
                "currency": "eur",
                "status": "requires_payment_method",
                "metadata": {
                    "order_number": str(self.order.order_number),
                },
            },
            "sk_test_mock",
        )

        response = self.client.post(
            reverse(
                "commissions:verify_payment",
                args=[self.order.order_number],
            )
        )

        self.order.refresh_from_db()

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()["success"])
        self.assertEqual(self.order.payment_status, "pending")
        mock_retrieve.assert_called_once_with("pi_test_success")

        self.assertFalse(self.order.confirmation_email_sent)
        self.assertEqual(len(mail.outbox), 0)

    @patch("commissions.views.stripe.PaymentIntent.retrieve")
    def test_mismatched_payment_details_rejected(self, mock_retrieve):
        """Reject mismatched Stripe payments without sending emails."""
        invalid_cases = [
            ("order_number", "incorrect-order-number"),
            ("amount", 10000),
            ("currency", "usd"),
        ]

        for field, invalid_value in invalid_cases:
            with self.subTest(field=field):
                payment_data = {
                    "id": "pi_test_success",
                    "amount": 18000,
                    "currency": "eur",
                    "status": "succeeded",
                    "metadata": {
                        "order_number": str(self.order.order_number),
                    },
                }

                if field == "order_number":
                    payment_data["metadata"]["order_number"] = invalid_value
                else:
                    payment_data[field] = invalid_value

                mock_retrieve.return_value = stripe.StripeObject.construct_from(
                    payment_data,
                    "sk_test_mock",
                )

                response = self.client.post(
                    reverse(
                        "commissions:verify_payment",
                        args=[self.order.order_number],
                    )
                )

                self.order.refresh_from_db()

                self.assertEqual(response.status_code, 400)
                self.assertFalse(response.json()["success"])
                self.assertEqual(self.order.payment_status, "pending")
                self.assertFalse(self.order.confirmation_email_sent)
                self.assertEqual(len(mail.outbox), 0)

    @patch("commissions.views.stripe.PaymentIntent.retrieve")
    def test_repeated_verification_does_not_resend_email(self, mock_retrieve):
        """Verifying the same payment twice sends only one email."""
        mock_retrieve.return_value = self.successful_payment()

        url = reverse(
            "commissions:verify_payment",
            args=[self.order.order_number],
        )

        first_response = self.client.post(url)
        second_response = self.client.post(url)

        self.order.refresh_from_db()

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(second_response.status_code, 200)
        self.assertEqual(self.order.payment_status, "paid")
        self.assertTrue(self.order.confirmation_email_sent)
        self.assertEqual(len(mail.outbox), 1)

    @patch("commissions.views.stripe.PaymentIntent.retrieve")
    @patch("commissions.views.stripe.PaymentIntent.create")
    def test_checkout_recovers_completed_payment(self, mock_create, mock_retrieve):
        """Checkout recovers a successful payment and sends confirmation."""
        session = self.client.session

        session["commission_creative"] = {
            "creative_direction": "surprise",
            "story": "",
            "moods": [],
            "colours": [],
            "imagery": "",
            "artwork_format": "digital",
            "artwork_size": "",
        }

        session["commission_customer"] = {
            "first_name": "Payment",
            "last_name": "Customer",
            "email": "payment@example.com",
            "delivery_region": "",
            "street": "",
            "house_number": "",
            "address_line_2": "",
            "city": "",
            "postal_code": "",
            "country": "",
        }

        session["commission_order_id"] = self.order.pk
        session.save()

        mock_retrieve.return_value = self.successful_payment()

        response = self.client.get(reverse("commissions:checkout"))

        self.order.refresh_from_db()

        self.assertRedirects(
            response,
            reverse(
                "commissions:success",
                args=[self.order.order_number],
            ),
            fetch_redirect_response=False,
        )
        self.assertEqual(self.order.payment_status, "paid")

        mock_retrieve.assert_called_once_with("pi_test_success")
        mock_create.assert_not_called()

        self.assertNotIn("commission_order_id", self.client.session)
        self.assertNotIn("commission_creative", self.client.session)
        self.assertNotIn("commission_customer", self.client.session)

        # Recovery must send the same confirmation as normal checkout.
        self.assertTrue(self.order.confirmation_email_sent)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].to,
            ["payment@example.com"],
        )

    @patch("commissions.views.stripe.PaymentIntent.retrieve")
    @patch("commissions.emails.send_mail")
    def test_email_failure_does_not_invalidate_payment(self, mock_send, mock_retrieve):
        """A failed email does not undo a successful Stripe payment."""
        mock_retrieve.return_value = self.successful_payment()
        mock_send.side_effect = ConnectionError("Email server unavailable")

        response = self.client.post(
            reverse(
                "commissions:verify_payment",
                args=[self.order.order_number],
            )
        )

        self.order.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        self.assertEqual(self.order.payment_status, "paid")
        self.assertFalse(self.order.confirmation_email_sent)
        mock_send.assert_called_once()

    def test_success_page_does_not_send_another_email(self):
        """Refreshing the success page must not resend confirmation."""
        self.order.payment_status = "paid"
        self.order.confirmation_email_sent = True
        self.order.save(
            update_fields=[
                "payment_status",
                "confirmation_email_sent",
            ]
        )

        url = reverse(
            "commissions:success",
            args=[self.order.order_number],
        )

        first_response = self.client.get(url)
        second_response = self.client.get(url)

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(second_response.status_code, 200)
        self.assertContains(
            first_response,
            "Confirmation email sent",
        )
        self.assertEqual(len(mail.outbox), 0)

    def test_success_page_shows_message_when_email_not_sent(self):
        """A paid order without an email shows the fallback message."""
        self.order.payment_status = "paid"
        self.order.save(update_fields=["payment_status"])

        response = self.client.get(
            reverse(
                "commissions:success",
                args=[self.order.order_number],
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "We couldn't send your confirmation email",
        )
        self.assertEqual(len(mail.outbox), 0)
