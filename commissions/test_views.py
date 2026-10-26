from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse


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
        self.assertEqual(saved["artwork_format"], "digital")

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

        self.assertRedirects(response, self.url)

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

        self.assertRedirects(response, self.url)

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
