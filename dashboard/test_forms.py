from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from artworks.models import Artwork, Collection
from .forms import ArtworkForm


class ArtworkFormTests(TestCase):
    """
    Test artwork form validation and required fields.
    """

    @classmethod
    def setUpTestData(cls):
        cls.collection = Collection.objects.create(
            name="Test Collection",
            slug="test-collection",
            description="A collection for testing.",
        )

    def setUp(self):
        self.valid_data = {
            "title": "Example Artwork",
            "collection": self.collection.pk,
            "year": 2026,
            "description": "An artwork for testing.",
            "etsy_url": "https://www.etsy.com/listing/123456789",
        }

    def get_test_image(self):
        """
        Create a small valid GIF image for form testing.
        """
        return SimpleUploadedFile(
            "test.gif",
            (
                b"GIF89a\x01\x00\x01\x00\x80\x00\x00"
                b"\x00\x00\x00\xff\xff\xff!"
                b"\xf9\x04\x01\x00\x00\x00\x00,"
                b"\x00\x00\x00\x00\x01\x00\x01\x00"
                b"\x00\x02\x02D\x01\x00;"
            ),
            content_type="image/gif",
        )

    def test_valid_artwork_form(self):
        form = ArtworkForm(
            data=self.valid_data,
            files={"image": self.get_test_image()},
        )

        self.assertTrue(form.is_valid(), form.errors)

    def test_required_fields(self):
        for field in ("title", "collection", "image"):
            with self.subTest(field=field):
                data = self.valid_data.copy()
                files = {"image": self.get_test_image()}

                if field == "image":
                    files = {}
                else:
                    data.pop(field)

                form = ArtworkForm(data=data, files=files)

                self.assertFalse(form.is_valid())
                self.assertIn(field, form.errors)

    def test_optional_fields_can_be_empty(self):
        data = {
            "title": "Minimal Artwork",
            "collection": self.collection.pk,
        }

        form = ArtworkForm(
            data=data,
            files={"image": self.get_test_image()},
        )

        self.assertTrue(form.is_valid(), form.errors)

    def test_duplicate_title_is_rejected_case_insensitively(self):
        Artwork.objects.create(
            title="Example Artwork",
            collection=self.collection,
            image="artworks/existing.jpg",
        )

        data = self.valid_data.copy()
        data["title"] = "EXAMPLE ARTWORK"

        form = ArtworkForm(
            data=data,
            files={"image": self.get_test_image()},
        )

        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)

    def test_duplicate_etsy_url_is_rejected(self):
        Artwork.objects.create(
            title="Existing Artwork",
            collection=self.collection,
            image="artworks/existing.jpg",
            etsy_url="https://www.etsy.com/listing/123456789",
        )

        form = ArtworkForm(
            data=self.valid_data,
            files={"image": self.get_test_image()},
        )

        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)

    def test_negative_year_is_rejected(self):
        data = self.valid_data.copy()
        data["year"] = -1

        form = ArtworkForm(
            data=data,
            files={"image": self.get_test_image()},
        )

        self.assertFalse(form.is_valid())
        self.assertIn("year", form.errors)
