from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Artwork, Collection, Favourite


@override_settings(
    STORAGES={
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
)
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


@override_settings(
    STORAGES={
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
)
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
        response = self.client.get(
            reverse("artworks", args=[self.collection.slug])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "artworks/artworks.html")
        self.assertEqual(response.context["collection"], self.collection)
        self.assertIn(self.artwork, response.context["page_obj"])
        self.assertNotIn(self.other_artwork, response.context["page_obj"])

    def test_invalid_collection_slug_returns_404(self):
        response = self.client.get(
            reverse("artworks", args=["nonexistent-collection"])
        )

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


@override_settings(
    STORAGES={
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
)
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
        response = self.client.get(
            reverse("artwork_detail", args=[self.artwork.slug])
        )

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


@override_settings(
    STORAGES={
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
)
class ArtworkFavouriteStatusViewTest(TestCase):
    """
    Tests favourite status and navigation on artwork detail pages.
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="favouriteuser",
            password="TestPassword123!",
        )
        cls.collection = Collection.objects.create(
            name="Favourite Collection",
            description="Collection for favourite view tests.",
        )
        cls.artwork = Artwork.objects.create(
            title="Favourite Detail Artwork",
            collection=cls.collection,
            image="artworks/favourite-detail.jpg",
        )
        cls.url = reverse("artwork_detail", args=[cls.artwork.slug])

    def test_anonymous_user_sees_login_prompt(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Add to Favourites")
        self.assertContains(response, "favouriteAuthModal")
        self.assertFalse(response.context["is_favourite"])

    def test_logged_in_user_sees_unsaved_artwork(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertFalse(response.context["is_favourite"])
        self.assertContains(response, "Add to Favourites")

    def test_saved_artwork_displays_remove_button(self):
        Favourite.objects.create(
            user=self.user,
            artwork=self.artwork,
        )
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertTrue(response.context["is_favourite"])
        self.assertContains(response, "Remove from Favourites")

    def test_navigation_returns_to_my_favourites(self):
        response = self.client.get(
            self.url,
            {"from": "favourites"},
        )

        self.assertTrue(response.context["from_favourites"])
        self.assertContains(response, "Back to My Favourites")
        self.assertContains(
            response,
            reverse("profiles:my_account"),
        )


@override_settings(
    STORAGES={
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
)
class ToggleFavouriteViewTest(TestCase):
    """
    Tests favourite creation, removal, permissions and redirects.
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="toggleuser",
            password="TestPassword123!",
        )
        cls.collection = Collection.objects.create(
            name="Toggle Collection",
            description="Collection for toggle tests.",
        )
        cls.artwork = Artwork.objects.create(
            title="Toggle Test Artwork",
            collection=cls.collection,
            image="artworks/toggle.jpg",
        )
        cls.url = reverse("toggle_favourite", args=[cls.artwork.slug])
        cls.detail_url = reverse(
            "artwork_detail",
            args=[cls.artwork.slug],
        )

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)
        self.assertFalse(Favourite.objects.exists())

    def test_get_request_is_not_allowed(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 405)
        self.assertFalse(Favourite.objects.exists())

    def test_post_adds_favourite(self):
        self.client.force_login(self.user)

        response = self.client.post(self.url)

        self.assertTrue(
            Favourite.objects.filter(
                user=self.user,
                artwork=self.artwork,
            ).exists()
        )
        self.assertRedirects(
            response,
            f"{self.detail_url}?page=1",
        )

    def test_post_removes_existing_favourite(self):
        Favourite.objects.create(
            user=self.user,
            artwork=self.artwork,
        )
        self.client.force_login(self.user)

        response = self.client.post(self.url)

        self.assertFalse(
            Favourite.objects.filter(
                user=self.user,
                artwork=self.artwork,
            ).exists()
        )
        self.assertRedirects(
            response,
            f"{self.detail_url}?page=1",
        )

    def test_gallery_page_is_preserved_after_toggle(self):
        self.client.force_login(self.user)

        response = self.client.post(
            self.url,
            {"page": "3"},
        )

        self.assertRedirects(
            response,
            f"{self.detail_url}?page=3",
        )

    def test_favourites_origin_is_preserved_after_toggle(self):
        self.client.force_login(self.user)

        response = self.client.post(
            self.url,
            {"from": "favourites"},
        )

        self.assertRedirects(
            response,
            f"{self.detail_url}?from=favourites",
        )

    def test_success_message_contains_favourites_link(self):
        self.client.force_login(self.user)

        response = self.client.post(
            self.url,
            follow=True,
        )

        favourites_url = reverse("profiles:my_account") + "#my-favourites"

        self.assertContains(response, "Artwork added to your favourites.")
        self.assertContains(response, "View My Favourites")
        self.assertContains(response, f'href="{favourites_url}"')

    def test_invalid_artwork_returns_404(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("toggle_favourite", args=["nonexistent-artwork"])
        )

        self.assertEqual(response.status_code, 404)
        self.assertFalse(Favourite.objects.exists())
