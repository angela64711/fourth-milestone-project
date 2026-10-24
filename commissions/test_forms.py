from django.test import SimpleTestCase

from .forms import CommissionCreativeForm


class CommissionCreativeFormTest(SimpleTestCase):
    """Tests validation of commission creative preferences."""

    def test_story_required_when_creative_direction_is_idea(self):
        """
        Test that choosing 'idea' without a story
        makes the commission form invalid.
        """
        form_data = {
            "creative_direction": "idea",
            "story": "",
            "moods": ["dreamlike"],
            "colours": ["blue"],
            "imagery": "nature",
            "artwork_format": "digital",
        }

        form = CommissionCreativeForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("story", form.errors)
