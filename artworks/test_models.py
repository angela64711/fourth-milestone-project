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

    def test_etsy_urls_must_be_unique(self):
        Artwork.objects.create(
            title="First Artwork",
            slug="first-artwork",
            collection=self.collection,
            image="artworks/first.jpg",
            etsy_url="https://www.etsy.com/listing/123456789",
        )

        duplicate = Artwork(
            title="Second Artwork",
            slug="second-artwork",
            collection=self.collection,
            image="artworks/second.jpg",
            etsy_url="https://www.etsy.com/listing/123456789",
        )

        with self.assertRaises(ValidationError):
            duplicate.full_clean()

    def test_multiple_artworks_can_have_empty_etsy_urls(self):
        for number in (1, 2):
            artwork = Artwork(
                title=f"Artwork {number}",
                slug=f"artwork-{number}",
                collection=self.collection,
                image=f"artworks/image-{number}.jpg",
                etsy_url="",
            )
            artwork.full_clean()
            artwork.save()

        self.assertEqual(Artwork.objects.filter(etsy_url="").count(), 2)

    def test_etsy_url_maximum_length(self):
        base_url = "https://www.etsy.com/listing/123456789?"
        long_url = base_url + "a" * (207 - len(base_url))

        artwork = Artwork(
            title="Long URL Artwork",
            slug="long-url-artwork",
            collection=self.collection,
            image="artworks/long-url.jpg",
            etsy_url=long_url,
        )

        # A URL of 207 characters should now be accepted.
        artwork.full_clean()

        # A URL exceeding the 300-character limit should be rejected.
        artwork.etsy_url = base_url + "a" * (301 - len(base_url))

        with self.assertRaises(ValidationError):
            artwork.full_clean()

    def test_artwork_titles_must_be_unique_case_insensitively(self):
        Artwork.objects.create(
            title="Example Artwork",
            collection=self.collection,
            image="artworks/first.jpg",
        )

        duplicate = Artwork(
            title="example artwork",
            collection=self.collection,
            image="artworks/second.jpg",
        )

        with self.assertRaises(ValidationError):
            duplicate.full_clean()

    def test_slug_is_generated_automatically(self):
        artwork = Artwork.objects.create(
            title="A Beautiful Dream",
            collection=self.collection,
            image="artworks/dream.jpg",
        )

        self.assertEqual(artwork.slug, "a-beautiful-dream")

    def test_duplicate_generated_slug_receives_numeric_suffix(self):
        Artwork.objects.create(
            title="Dream & Reality",
            collection=self.collection,
            image="artworks/first.jpg",
        )

        artwork = Artwork.objects.create(
            title="Dream Reality",
            collection=self.collection,
            image="artworks/second.jpg",
        )

        self.assertEqual(artwork.slug, "dream-reality-2")

    def test_multiple_slug_collisions_increment_suffix(self):
        titles = [
            "Dream & Reality",
            "Dream Reality",
            "Dream - Reality",
        ]

        artworks = [
            Artwork.objects.create(
                title=title,
                collection=self.collection,
                image=f"artworks/image-{number}.jpg",
            )
            for number, title in enumerate(titles, start=1)
        ]

        self.assertEqual(
            [artwork.slug for artwork in artworks],
            ["dream-reality", "dream-reality-2", "dream-reality-3"],
        )

    def test_slug_is_preserved_when_title_changes(self):
        artwork = Artwork.objects.create(
            title="Original Title",
            collection=self.collection,
            image="artworks/example.jpg",
        )

        artwork.title = "Updated Title"
        artwork.save()
        artwork.refresh_from_db()

        self.assertEqual(artwork.title, "Updated Title")
        self.assertEqual(artwork.slug, "original-title")

    def test_title_edit_cannot_duplicate_another_title(self):
        Artwork.objects.create(
            title="Existing Artwork",
            collection=self.collection,
            image="artworks/first.jpg",
        )

        artwork = Artwork.objects.create(
            title="Different Artwork",
            collection=self.collection,
            image="artworks/second.jpg",
        )

        artwork.title = "EXISTING ARTWORK"

        with self.assertRaises(ValidationError):
            artwork.full_clean()


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

    def test_collection_slug_is_generated_automatically(self):
        collection = Collection.objects.create(
            name="Digital Dreams",
            description="A collection of digital artworks.",
        )

        self.assertEqual(collection.slug, "digital-dreams")

    def test_duplicate_collection_slug_receives_numeric_suffix(self):
        Collection.objects.create(
            name="Dream & Reality",
            description="First collection.",
        )

        collection = Collection.objects.create(
            name="Dream Reality",
            description="Second collection.",
        )

        self.assertEqual(collection.slug, "dream-reality-2")

    def test_collection_slug_is_preserved_when_name_changes(self):
        collection = Collection.objects.create(
            name="Original Collection",
            description="A collection for testing.",
        )

        collection.name = "Renamed Collection"
        collection.save()
        collection.refresh_from_db()

        self.assertEqual(collection.name, "Renamed Collection")
        self.assertEqual(collection.slug, "original-collection")

    def test_collection_cover_is_optional(self):
        collection = Collection.objects.create(
            name="Test Collection",
            description="A collection for testing.",
        )

        self.assertIsNone(collection.cover_artwork)

    def test_collection_can_store_selected_cover_artwork(self):
        collection = Collection.objects.create(
            name="Test Collection",
            description="A collection for testing.",
        )
        artwork = Artwork.objects.create(
            title="Cover Artwork",
            collection=collection,
            image="artworks/cover.jpg",
        )

        collection.cover_artwork = artwork
        collection.save()
        collection.refresh_from_db()

        self.assertEqual(collection.cover_artwork, artwork)

    def test_deleting_selected_artwork_clears_collection_cover(self):
        collection = Collection.objects.create(
            name="Test Collection",
            description="A collection for testing.",
        )
        artwork = Artwork.objects.create(
            title="Cover Artwork",
            collection=collection,
            image="artworks/cover.jpg",
        )
        collection.cover_artwork = artwork
        collection.save()

        artwork.delete()
        collection.refresh_from_db()

        self.assertIsNone(collection.cover_artwork)
        self.assertTrue(Collection.objects.filter(pk=collection.pk).exists())

    def test_cover_returns_manually_selected_artwork(self):
        collection = Collection.objects.create(
            name="Test Collection",
            description="A collection for testing.",
        )
        artwork = Artwork.objects.create(
            title="Selected Cover",
            collection=collection,
            image="artworks/selected.jpg",
        )

        collection.cover_artwork = artwork
        collection.save()

        self.assertEqual(collection.cover, artwork)

    def test_cover_defaults_to_first_artwork_alphabetically(self):
        collection = Collection.objects.create(
            name="Test Collection",
            description="A collection for testing.",
        )

        Artwork.objects.create(
            title="Zebra Dreams",
            collection=collection,
            image="artworks/zebra.jpg",
        )
        first_artwork = Artwork.objects.create(
            title="Autumn Dreams",
            collection=collection,
            image="artworks/autumn.jpg",
        )

        self.assertEqual(collection.cover, first_artwork)

    def test_cover_returns_none_for_empty_collection(self):
        collection = Collection.objects.create(
            name="Empty Collection",
            description="A collection without artworks.",
        )

        self.assertIsNone(collection.cover)
