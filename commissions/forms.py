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
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    colours = forms.MultipleChoiceField(
        choices=CommissionOrder.COLOUR_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    imagery = forms.ChoiceField(
        choices=CommissionOrder.IMAGERY_CHOICES,
        required=False,
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

    def clean_moods(self):
        """Allow a maximum of two mood selections."""
        moods = self.cleaned_data["moods"]

        if len(moods) > 2:
            raise forms.ValidationError("Please select no more than two moods.")

        return moods

    def clean_colours(self):
        """Allow a maximum of two colour selections."""
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

        creative_direction = cleaned_data.get("creative_direction")

        if creative_direction == "idea":
            # Creative preferences are required for a specific idea.
            story = cleaned_data.get("story", "")

            if not story.strip():
                self.add_error("story", "Please describe your idea for the artwork.")

            if not cleaned_data.get("moods") and "moods" not in self.errors:
                self.add_error("moods", "Please select at least one mood.")

            if not cleaned_data.get("colours") and "colours" not in self.errors:
                self.add_error("colours", "Please select at least one colour.")

            if not cleaned_data.get("imagery") and "imagery" not in self.errors:
                self.add_error("imagery", "Please select an imagery direction.")

        elif creative_direction == "surprise":
            # Ignore creative preferences for surprise commissions.
            cleaned_data["story"] = ""
            cleaned_data["moods"] = []
            cleaned_data["colours"] = []
            cleaned_data["imagery"] = ""

        # Physical artwork requires a size.
        artwork_format = cleaned_data.get("artwork_format")

        if artwork_format in ["print", "framed"]:
            if not cleaned_data.get("artwork_size"):
                self.add_error("artwork_size", "Please select an artwork size.")

        elif artwork_format == "digital":
            # Digital artwork does not require physical dimensions.
            cleaned_data["artwork_size"] = ""

        return cleaned_data


class CommissionCustomerForm(forms.Form):
    """
    Collect customer contact and delivery details.

    Shipping fields are required for physical artwork.
    The artwork format comes from validated session data.
    """

    first_name = forms.CharField(max_length=70)
    last_name = forms.CharField(max_length=70)
    email = forms.EmailField()

    delivery_region = forms.ChoiceField(
        choices=CommissionOrder.DELIVERY_REGION_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    street = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "autocomplete": "address-line1",
            }
        ),
    )

    house_number = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    address_line_2 = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "autocomplete": "address-line2",
            }
        ),
    )

    city = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "autocomplete": "address-level2",
            }
        ),
    )

    postal_code = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "autocomplete": "postal-code",
            }
        ),
    )

    country = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "autocomplete": "country-name",
            }
        ),
    )

    def __init__(self, *args, artwork_format=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.artwork_format = artwork_format

    def clean(self):
        """Validate delivery details for physical commissions."""
        cleaned_data = super().clean()

        shipping_fields = [
            "delivery_region",
            "street",
            "house_number",
            "city",
            "postal_code",
            "country",
        ]

        if self.artwork_format in ["print", "framed"]:
            for field_name in shipping_fields:
                if not cleaned_data.get(field_name):
                    if field_name not in self.errors:
                        self.add_error(
                            field_name,
                            "This field is required for physical artwork.",
                        )

        elif self.artwork_format == "digital":
            for field_name in shipping_fields + ["address_line_2"]:
                cleaned_data[field_name] = ""

        return cleaned_data
