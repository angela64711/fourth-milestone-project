from django import forms

from artworks.models import Artwork


class ArtworkForm(forms.ModelForm):
    """
    Form for artists to create and edit artworks.
    """

    class Meta:
        model = Artwork
        fields = [
            "title",
            "collection",
            "year",
            "description",
            "image",
            "etsy_url",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "collection": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "year": forms.NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "etsy_url": forms.URLInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }
