from django import forms

from .models import CommissionOrder


class CommissionCreativeForm(forms.Form):
    """
    Collect and validate the creative preferences for a commission.

    Validated data will be stored in the session before the
    customer completes their order details.
    """

    creative_direction = forms.ChoiceField(
        choices=CommissionOrder.CREATIVE_DIRECTION_CHOICES,
        widget=forms.RadioSelect,
    )

    # Required conditionally based on creative_direction selection
    story = forms.CharField(
        max_length=1000,
        required=False,
        widget=forms.Textarea(attrs={"rows": 5}),
    )

    moods = forms.MultipleChoiceField(
        choices=CommissionOrder.MOOD_CHOICES,
        widget=forms.CheckboxSelectMultiple,
    )

    colours = forms.MultipleChoiceField(
        choices=CommissionOrder.COLOUR_CHOICES,
        widget=forms.CheckboxSelectMultiple,
    )

    imagery = forms.ChoiceField(
        choices=CommissionOrder.IMAGERY_CHOICES,
        widget=forms.RadioSelect,
    )

    artwork_format = forms.ChoiceField(
        choices=CommissionOrder.FORMAT_CHOICES,
        widget=forms.RadioSelect,
    )

    # Required conditionally based on artwork_format selection
    artwork_size = forms.ChoiceField(
        choices=CommissionOrder.SIZE_CHOICES,
        required=False,
        widget=forms.RadioSelect,
    )

    # Required conditionally based on artwork_format selection
    delivery_region = forms.ChoiceField(
        choices=CommissionOrder.DELIVERY_REGION_CHOICES,
        required=False,
        widget=forms.RadioSelect,
    )

    def clean_moods(self):
        """Require between one and two mood selections."""
        moods = self.cleaned_data["moods"]

        if len(moods) > 2:
            raise forms.ValidationError("Please select no more than two moods.")

        return moods

    def clean_colours(self):
        """Require between one and two colour selections."""
        colours = self.cleaned_data["colours"]

        if len(colours) > 2:
            raise forms.ValidationError("Please select no more than two colours.")

        return colours

    def clean(self):
        """
        Validate conditional requirements for creative direction
        and artwork format.
        """
        cleaned_data = super().clean()

        # Require a story when the customer has a specific idea.
        creative_direction = cleaned_data.get("creative_direction")
        story = cleaned_data.get("story", "")

        if creative_direction == "idea" and not story.strip():
            self.add_error("story", "Please describe your idea for the artwork.")

        # Physical artwork requires size and delivery region.
        artwork_format = cleaned_data.get("artwork_format")

        if artwork_format in ["print", "framed"]:
            if not cleaned_data.get("artwork_size"):
                self.add_error("artwork_size", "Please select an artwork size.")

            if not cleaned_data.get("delivery_region"):
                self.add_error("delivery_region", "Please select a delivery region.")

        elif artwork_format == "digital":
            # Ignore physical delivery choices for digital artwork.
            cleaned_data["artwork_size"] = ""
            cleaned_data["delivery_region"] = ""

        return cleaned_data
