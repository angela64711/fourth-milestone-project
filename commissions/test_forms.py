from django.test import SimpleTestCase

from .forms import CommissionCreativeForm


class CommissionCreativeFormTest(SimpleTestCase):
    """Tests validation of commission creative preferences."""

    def valid_form_data(self, **overrides):
        """
        Return valid creative preferences for reuse across tests.
        Individual tests can override specific fields.
        """
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
        """Test that a complete creative brief is valid."""
        form = CommissionCreativeForm(data=self.valid_form_data())

        self.assertTrue(form.is_valid())

    def test_story_required_when_creative_direction_is_idea(self):
        """
        Test that choosing 'idea' without a story
        makes the commission form invalid.
        """
        form = CommissionCreativeForm(data=self.valid_form_data(story=""))

        self.assertFalse(form.is_valid())
        self.assertIn("story", form.errors)

    def test_story_optional_for_surprise(self):
        """Test that surprise commissions do not require a story."""
        form = CommissionCreativeForm(
            data=self.valid_form_data(
                creative_direction="surprise",
                story="",
            )
        )

        self.assertTrue(form.is_valid())

    def test_whitespace_only_story_is_invalid(self):
        """Test that whitespace does not satisfy the story requirement."""
        form = CommissionCreativeForm(data=self.valid_form_data(story="   "))

        self.assertFalse(form.is_valid())
        self.assertIn("story", form.errors)

    def test_story_maximum_length(self):
        """Test that a story longer than 1000 characters is rejected."""
        form = CommissionCreativeForm(data=self.valid_form_data(story="A" * 1001))

        self.assertFalse(form.is_valid())
        self.assertIn("story", form.errors)

    def test_moods_selection_limits(self):
        """Test that customers must select one or two moods."""
        for moods, expected_valid in [
            ([], False),
            (["dreamlike"], True),
            (["dreamlike", "romantic"], True),
            (["dreamlike", "romantic", "serene"], False),
        ]:
            with self.subTest(moods=moods):
                form = CommissionCreativeForm(data=self.valid_form_data(moods=moods))

                self.assertEqual(form.is_valid(), expected_valid)

                if not expected_valid:
                    self.assertIn("moods", form.errors)

    def test_colours_selection_limits(self):
        """Test that customers must select one or two colours."""
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

                if not expected_valid:
                    self.assertIn("colours", form.errors)

    def test_invalid_mood_or_colour_rejected(self):
        """Test that choices outside the model options are rejected."""
        for field in ["moods", "colours"]:
            with self.subTest(field=field):
                form = CommissionCreativeForm(
                    data=self.valid_form_data(**{field: ["invalid_choice"]})
                )

                self.assertFalse(form.is_valid())
                self.assertIn(field, form.errors)

    def test_invalid_single_choice_rejected(self):
        """Test that unrecognised single-choice values are rejected."""
        fields = [
            "creative_direction",
            "imagery",
            "artwork_format",
        ]

        for field in fields:
            with self.subTest(field=field):
                form = CommissionCreativeForm(
                    data=self.valid_form_data(**{field: "invalid_choice"})
                )

                self.assertFalse(form.is_valid())
                self.assertIn(field, form.errors)

    def test_physical_artwork_requires_size(self):
        """Test that print and framed artwork require dimensions."""
        for artwork_format in ["print", "framed"]:
            with self.subTest(artwork_format=artwork_format):
                form = CommissionCreativeForm(
                    data=self.valid_form_data(
                        artwork_format=artwork_format,
                        artwork_size="",
                        delivery_region="europe_uk",
                    )
                )

                self.assertFalse(form.is_valid())
                self.assertIn("artwork_size", form.errors)

    def test_physical_artwork_requires_delivery_region(self):
        """Test that print and framed artwork require a region."""
        for artwork_format in ["print", "framed"]:
            with self.subTest(artwork_format=artwork_format):
                form = CommissionCreativeForm(
                    data=self.valid_form_data(
                        artwork_format=artwork_format,
                        artwork_size="30x40",
                        delivery_region="",
                    )
                )

                self.assertFalse(form.is_valid())
                self.assertIn("delivery_region", form.errors)

    def test_valid_physical_artwork(self):
        """Test that complete physical artwork selections are valid."""
        for artwork_format in ["print", "framed"]:
            with self.subTest(artwork_format=artwork_format):
                form = CommissionCreativeForm(
                    data=self.valid_form_data(
                        artwork_format=artwork_format,
                        artwork_size="50x70",
                        delivery_region="international",
                    )
                )

                self.assertTrue(form.is_valid())

    def test_digital_artwork_does_not_require_delivery(self):
        """Test that digital commissions need no physical options."""
        form = CommissionCreativeForm(
            data=self.valid_form_data(
                artwork_format="digital",
                artwork_size="",
                delivery_region="",
            )
        )

        self.assertTrue(form.is_valid())

    def test_digital_artwork_clears_physical_options(self):
        """Test that digital orders discard unnecessary physical options."""
        form = CommissionCreativeForm(
            data=self.valid_form_data(
                artwork_format="digital",
                artwork_size="30x40",
                delivery_region="europe_uk",
            )
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["artwork_size"], "")
        self.assertEqual(form.cleaned_data["delivery_region"], "")
