from django.test import SimpleTestCase

from .forms import CommissionCreativeForm, CommissionCustomerForm


class CommissionCreativeFormTest(SimpleTestCase):
    """Tests validation of commission creative preferences."""

    def valid_form_data(self, **overrides):
        """Return valid creative preferences for reuse."""
        data = {
            "creative_direction": "idea",
            "story": "A dreamlike landscape with classical elements.",
            "moods": ["dreamlike", "nostalgic"],
            "colours": ["blue", "pink"],
            "imagery": "classical",
            "artwork_format": "digital",
        }
        data.update(overrides)
        return data

    def test_valid_idea_submission(self):
        """A complete creative brief is valid."""
        form = CommissionCreativeForm(data=self.valid_form_data())
        self.assertTrue(form.is_valid())

    def test_story_required_for_idea(self):
        """An idea commission requires a meaningful story."""
        for story in ["", "   "]:
            with self.subTest(story=story):
                form = CommissionCreativeForm(data=self.valid_form_data(story=story))
                self.assertFalse(form.is_valid())
                self.assertIn("story", form.errors)

    def test_story_maximum_length(self):
        """Stories exceeding 1000 characters are rejected."""
        form = CommissionCreativeForm(data=self.valid_form_data(story="A" * 1001))
        self.assertFalse(form.is_valid())
        self.assertIn("story", form.errors)

    def test_idea_requires_creative_preferences(self):
        """Idea commissions require moods, colours and imagery."""
        for field, empty_value in [
            ("moods", []),
            ("colours", []),
            ("imagery", ""),
        ]:
            with self.subTest(field=field):
                form = CommissionCreativeForm(
                    data=self.valid_form_data(**{field: empty_value})
                )
                self.assertFalse(form.is_valid())
                self.assertIn(field, form.errors)

    def test_moods_selection_limits(self):
        """Idea commissions allow one or two moods."""
        for moods, expected_valid in [
            ([], False),
            (["dreamlike"], True),
            (["dreamlike", "romantic"], True),
            (["dreamlike", "romantic", "serene"], False),
        ]:
            with self.subTest(moods=moods):
                form = CommissionCreativeForm(data=self.valid_form_data(moods=moods))
                self.assertEqual(form.is_valid(), expected_valid)

    def test_colours_selection_limits(self):
        """Idea commissions allow one or two colours."""
        for colours, expected_valid in [
            ([], False),
            (["blue"], True),
            (["blue", "pink"], True),
            (["blue", "pink", "yellow"], False),
        ]:
            with self.subTest(colours=colours):
                form = CommissionCreativeForm(
                    data=self.valid_form_data(colours=colours)
                )
                self.assertEqual(form.is_valid(), expected_valid)

    def test_invalid_choices_rejected(self):
        """Unrecognised creative choices are rejected."""
        fields = [
            "creative_direction",
            "moods",
            "colours",
            "imagery",
            "artwork_format",
            "artwork_size",
        ]

        for field in fields:
            with self.subTest(field=field):
                invalid_value = (
                    ["invalid"] if field in ["moods", "colours"] else "invalid"
                )
                form = CommissionCreativeForm(
                    data=self.valid_form_data(**{field: invalid_value})
                )
                self.assertFalse(form.is_valid())
                self.assertIn(field, form.errors)

    def test_surprise_without_preferences(self):
        """Surprise commissions need no creative preferences."""
        form = CommissionCreativeForm(
            data=self.valid_form_data(
                creative_direction="surprise",
                story="",
                moods=[],
                colours=[],
                imagery="",
            )
        )
        self.assertTrue(form.is_valid())

    def test_surprise_clears_creative_preferences(self):
        """Surprise commissions discard submitted creative details."""
        form = CommissionCreativeForm(
            data=self.valid_form_data(creative_direction="surprise")
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["story"], "")
        self.assertEqual(form.cleaned_data["moods"], [])
        self.assertEqual(form.cleaned_data["colours"], [])
        self.assertEqual(form.cleaned_data["imagery"], "")

    def test_physical_artwork_requires_size(self):
        """Prints and framed artwork require dimensions."""
        for artwork_format in ["print", "framed"]:
            with self.subTest(artwork_format=artwork_format):
                form = CommissionCreativeForm(
                    data=self.valid_form_data(
                        artwork_format=artwork_format,
                        artwork_size="",
                    )
                )
                self.assertFalse(form.is_valid())
                self.assertIn("artwork_size", form.errors)

    def test_valid_physical_artwork(self):
        """Both physical formats accept supported sizes."""
        for artwork_format in ["print", "framed"]:
            for artwork_size in ["30x40", "50x70"]:
                with self.subTest(
                    artwork_format=artwork_format,
                    artwork_size=artwork_size,
                ):
                    form = CommissionCreativeForm(
                        data=self.valid_form_data(
                            artwork_format=artwork_format,
                            artwork_size=artwork_size,
                        )
                    )
                    self.assertTrue(form.is_valid())

    def test_digital_artwork_clears_size(self):
        """Digital commissions do not retain physical dimensions."""
        form = CommissionCreativeForm(
            data=self.valid_form_data(
                artwork_format="digital",
                artwork_size="30x40",
            )
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["artwork_size"], "")


class CommissionCustomerFormTest(SimpleTestCase):
    """Tests customer contact details and conditional shipping."""

    def valid_customer_data(self, **overrides):
        """Return valid customer and shipping details."""
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

    def test_valid_digital_customer(self):
        """Digital orders accept contact details without shipping."""
        form = CommissionCustomerForm(
            data=self.valid_customer_data(),
            artwork_format="digital",
        )
        self.assertTrue(form.is_valid())

    def test_required_contact_fields(self):
        """First name, last name and email are required."""
        for field in ["first_name", "last_name", "email"]:
            with self.subTest(field=field):
                form = CommissionCustomerForm(
                    data=self.valid_customer_data(**{field: ""}),
                    artwork_format="digital",
                )
                self.assertFalse(form.is_valid())
                self.assertIn(field, form.errors)

    def test_invalid_email_rejected(self):
        """Customer email must have a valid format."""
        form = CommissionCustomerForm(
            data=self.valid_customer_data(email="not-an-email"),
            artwork_format="digital",
        )
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_physical_artwork_requires_shipping(self):
        """Prints and framed orders require complete delivery details."""
        required_fields = [
            "delivery_region",
            "street",
            "house_number",
            "city",
            "postal_code",
            "country",
        ]

        for artwork_format in ["print", "framed"]:
            for field in required_fields:
                with self.subTest(
                    artwork_format=artwork_format,
                    field=field,
                ):
                    form = CommissionCustomerForm(
                        data=self.valid_customer_data(**{field: ""}),
                        artwork_format=artwork_format,
                    )
                    self.assertFalse(form.is_valid())
                    self.assertIn(field, form.errors)

    def test_valid_physical_customer(self):
        """Complete shipping information is accepted."""
        for artwork_format in ["print", "framed"]:
            with self.subTest(artwork_format=artwork_format):
                form = CommissionCustomerForm(
                    data=self.valid_customer_data(),
                    artwork_format=artwork_format,
                )
                self.assertTrue(form.is_valid())

    def test_address_line_2_optional(self):
        """Additional address information is not mandatory."""
        form = CommissionCustomerForm(
            data=self.valid_customer_data(address_line_2=""),
            artwork_format="print",
        )
        self.assertTrue(form.is_valid())

    def test_invalid_delivery_region(self):
        """Unsupported delivery regions are rejected."""
        form = CommissionCustomerForm(
            data=self.valid_customer_data(delivery_region="invalid_region"),
            artwork_format="print",
        )
        self.assertFalse(form.is_valid())
        self.assertIn("delivery_region", form.errors)

    def test_digital_clears_shipping_details(self):
        """Digital commissions discard unnecessary delivery data."""
        form = CommissionCustomerForm(
            data=self.valid_customer_data(),
            artwork_format="digital",
        )
        self.assertTrue(form.is_valid())

        shipping_fields = [
            "delivery_region",
            "street",
            "house_number",
            "address_line_2",
            "city",
            "postal_code",
            "country",
        ]

        for field in shipping_fields:
            with self.subTest(field=field):
                self.assertEqual(form.cleaned_data[field], "")
