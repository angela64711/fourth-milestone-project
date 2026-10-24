from django.core.exceptions import ValidationError
from django.db.models.deletion import ProtectedError
from django.test import TestCase

from .models import Artwork, Collection


class ArtworkModelTest(TestCase):
    """
    Tests the creation, validation and relationships of artwork records.
    """

    @classmethod
    def setUpTestData(cls):
        cls.collection = Collection.objects.create(
            name="Test Collection",
            slug="test-collection",
            description="A collection for testing.",
        )

    def test_create_artwork_with_title_and_image(self):
        artwork = Artwork.objects.create(
            title="Example Artwork",
            slug="example-artwork",
            collection=self.collection,
            image="artworks/example.jpg",
        )

        saved_artwork = Artwork.objects.get(pk=artwork.pk)

        self.assertEqual(saved_artwork.title, "Example Artwork")
        self.assertEqual(saved_artwork.image.name, "artworks/example.jpg")

    def test_artwork_titles_must_be_unique(self):
        Artwork.objects.create(
            title="Example Artwork",
            slug="first-artwork",
            collection=self.collection,
            image="artworks/first.jpg",
        )

        duplicate = Artwork(
            title="Example Artwork",
            slug="second-artwork",
            collection=self.collection,
            image="artworks/second.jpg",
        )

        with self.assertRaises(ValidationError):
            duplicate.full_clean()

    def test_artwork_string_method_returns_title(self):
        artwork = Artwork.objects.create(
            title="Example Artwork",
            slug="example-artwork",
            collection=self.collection,
            image="artworks/example.jpg",
        )

        self.assertEqual(str(artwork), "Example Artwork")

    def test_artwork_slugs_must_be_unique(self):
        Artwork.objects.create(
            title="First Artwork",
            slug="shared-slug",
            collection=self.collection,
            image="artworks/first.jpg",
        )

        duplicate = Artwork(
            title="Second Artwork",
            slug="shared-slug",
            collection=self.collection,
            image="artworks/second.jpg",
        )

        # full_clean() checks the model's unique slug constraint.
        with self.assertRaises(ValidationError):
            duplicate.full_clean()

    def test_collection_with_artwork_cannot_be_deleted(self):
        Artwork.objects.create(
            title="Protected Artwork",
            slug="protected-artwork",
            collection=self.collection,
            image="artworks/protected.jpg",
        )

        # PROTECT prevents deleting a collection that still has artworks.
        with self.assertRaises(ProtectedError):
            self.collection.delete()

        # Confirm that both records remain in the database.
        self.assertTrue(Collection.objects.filter(pk=self.collection.pk).exists())
        self.assertTrue(Artwork.objects.filter(slug="protected-artwork").exists())


class CollectionModelTest(TestCase):
    """
    Tests collection display ordering and string representation.
    """

    def test_first_collection_receives_display_order_one(self):
        collection = Collection.objects.create(
            name="First Collection",
            slug="first-collection",
            description="First collection for testing.",
        )

        self.assertEqual(collection.display_order, 1)

    def test_new_collection_receives_next_display_order(self):
        Collection.objects.create(
            name="First Collection",
            slug="first-collection",
            description="First collection for testing.",
            display_order=5,
        )

        new_collection = Collection.objects.create(
            name="Second Collection",
            slug="second-collection",
            description="Second collection for testing.",
        )

        self.assertEqual(new_collection.display_order, 6)

    def test_collection_string_method_returns_name(self):
        collection = Collection.objects.create(
            name="Dreamscapes",
            slug="dreamscapes",
            description="A collection of dreamlike artworks.",
        )

        self.assertEqual(str(collection), "Dreamscapes")
