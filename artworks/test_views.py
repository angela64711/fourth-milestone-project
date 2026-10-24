from django.test import TestCase
from django.urls import reverse

from .models import Artwork, Collection


class CollectionsViewTest(TestCase):
    """
    Tests the collections listing page and its filtering.
    """

    @classmethod
    def setUpTestData(cls):
        cls.populated_collection = Collection.objects.create(
            name="Populated Collection",
            slug="populated-collection",
            description="Contains artwork.",
        )
        cls.empty_collection = Collection.objects.create(
            name="Empty Collection",
            slug="empty-collection",
            description="Contains no artwork.",
        )
        Artwork.objects.create(
            title="Test Artwork",
            slug="test-artwork",
            collection=cls.populated_collection,
            image="artworks/test.jpg",
        )

    def test_collections_page_loads(self):
        response = self.client.get(reverse("art"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "artworks/collections.html")

    def test_only_populated_collections_are_displayed(self):
        response = self.client.get(reverse("art"))

        collections = response.context["collections"]

        self.assertIn(self.populated_collection, collections)
        self.assertNotIn(self.empty_collection, collections)
        self.assertContains(response, "Populated Collection")
        self.assertNotContains(response, "Empty Collection")


class CollectionGalleryViewTest(TestCase):
    """
    Tests collection galleries, invalid slugs and pagination.
    """

    @classmethod
    def setUpTestData(cls):
        cls.collection = Collection.objects.create(
            name="Test Collection",
            slug="test-collection",
            description="A collection for testing.",
        )
        cls.other_collection = Collection.objects.create(
            name="Other Collection",
            slug="other-collection",
            description="Another collection.",
        )

        cls.artwork = Artwork.objects.create(
            title="Gallery Artwork",
            slug="gallery-artwork",
            collection=cls.collection,
            image="artworks/gallery.jpg",
        )

        cls.other_artwork = Artwork.objects.create(
            title="Other Artwork",
            slug="other-artwork",
            collection=cls.other_collection,
            image="artworks/other.jpg",
        )

    def test_gallery_displays_correct_collection_and_artworks(self):
        response = self.client.get(reverse("artworks", args=[self.collection.slug]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "artworks/artworks.html")
        self.assertEqual(response.context["collection"], self.collection)
        self.assertIn(self.artwork, response.context["page_obj"])
        self.assertNotIn(self.other_artwork, response.context["page_obj"])

    def test_invalid_collection_slug_returns_404(self):
        response = self.client.get(reverse("artworks", args=["nonexistent-collection"]))

        self.assertEqual(response.status_code, 404)

    def test_gallery_pagination_after_24_artworks(self):
        for number in range(24):
            Artwork.objects.create(
                title=f"Extra Artwork {number}",
                slug=f"extra-artwork-{number}",
                collection=self.collection,
                image="artworks/test.jpg",
            )

        url = reverse("artworks", args=[self.collection.slug])
        first_page = self.client.get(url)
        second_page = self.client.get(url, {"page": 2})

        self.assertEqual(first_page.context["page_obj"].number, 1)
        self.assertEqual(len(first_page.context["page_obj"]), 24)
        self.assertTrue(first_page.context["page_obj"].has_next())

        self.assertEqual(second_page.context["page_obj"].number, 2)
        self.assertEqual(len(second_page.context["page_obj"]), 1)
        self.assertFalse(second_page.context["page_obj"].has_next())


class ArtworkDetailViewTest(TestCase):
    """
    Tests artwork details, invalid slugs and gallery navigation.
    """

    @classmethod
    def setUpTestData(cls):
        cls.collection = Collection.objects.create(
            name="Test Collection",
            slug="test-collection",
            description="A collection for testing.",
        )

        cls.artwork = Artwork.objects.create(
            title="Detail Test Artwork",
            slug="detail-test-artwork",
            collection=cls.collection,
            year=2024,
            description="An artwork created for testing.",
            image="artworks/detail.jpg",
        )

    def test_artwork_detail_displays_correct_information(self):
        response = self.client.get(reverse("artwork_detail", args=[self.artwork.slug]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "artworks/artwork_detail.html")
        self.assertEqual(response.context["artwork"], self.artwork)
        self.assertContains(response, self.artwork.title)
        self.assertContains(response, self.artwork.description)
        self.assertContains(response, self.collection.name)

    def test_invalid_artwork_slug_returns_404(self):
        response = self.client.get(
            reverse("artwork_detail", args=["nonexistent-artwork"])
        )

        self.assertEqual(response.status_code, 404)

    def test_gallery_page_parameter_is_preserved(self):
        response = self.client.get(
            reverse("artwork_detail", args=[self.artwork.slug]),
            {"page": 3},
        )

        self.assertEqual(response.context["gallery_page"], "3")
        self.assertContains(
            response,
            f'{reverse("artworks", args=[self.collection.slug])}?page=3',
        )
