from django.test import TestCase

from .models import Artwork


class ArtworkModelTest(TestCase):
    """
    Tests the creation and storage of artwork records.
    """

    def test_create_artwork_with_title_and_image(self):
        artwork = Artwork.objects.create(
            title="Example Artwork",
            image="artworks/example.jpg",
        )

        saved_artwork = Artwork.objects.get(pk=artwork.pk)

        self.assertEqual(saved_artwork.title, "Example Artwork")
        self.assertEqual(saved_artwork.image.name, "artworks/example.jpg")
