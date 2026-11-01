from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from artworks.models import Artwork, Collection
from dashboard.forms import ArtworkForm


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
class DashboardArtworkOverviewTests(TestCase):
    """Test the artist dashboard artwork overview page."""

    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()

        cls.artist = user_model.objects.create_user(
            username="overviewartist",
            password="testpassword123",
        )
        artist_group, _ = Group.objects.get_or_create(name="Artists")
        cls.artist.groups.add(artist_group)

        cls.collection = Collection.objects.create(
            name="Test Collection",
            slug="test-collection",
            description="A collection for testing.",
        )

        cls.artwork = Artwork.objects.create(
            title="Test Artwork",
            collection=cls.collection,
            year=2025,
            image="artworks/test.jpg",
        )

    def setUp(self):
        self.client.force_login(self.artist)
        self.url = reverse(
            "dashboard:artwork_overview",
            kwargs={"slug": self.artwork.slug},
        )

    def test_artwork_overview_displays_correct_artwork(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "dashboard/artwork_overview.html",
        )
        self.assertEqual(
            response.context["artwork"],
            self.artwork,
        )

    def test_nonexistent_artwork_returns_404(self):
        url = reverse(
            "dashboard:artwork_overview",
            kwargs={"slug": "nonexistent-artwork"},
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)


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
class DashboardArtworkAddTests(TestCase):
    """Test adding artworks through the artist dashboard."""

    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()

        cls.artist = user_model.objects.create_user(
            username="addartist",
            password="testpassword123",
        )
        artist_group, _ = Group.objects.get_or_create(name="Artists")
        cls.artist.groups.add(artist_group)

        cls.collection = Collection.objects.create(
            name="Test Collection",
            slug="test-collection",
            description="A collection for testing.",
        )

    def setUp(self):
        self.client.force_login(self.artist)
        self.url = reverse("dashboard:artwork_add")

    def get_test_image(self):
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

    def test_add_artwork_page_displays_form(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "dashboard/artwork_form.html",
        )
        self.assertIsInstance(
            response.context["form"],
            ArtworkForm,
        )

    def test_valid_post_creates_artwork_and_redirects(self):
        response = self.client.post(
            self.url,
            {
                "title": "New Artwork",
                "collection": self.collection.pk,
                "year": 2026,
                "description": "A newly created artwork.",
                "image": self.get_test_image(),
            },
        )

        artwork = Artwork.objects.get(title="New Artwork")

        self.assertEqual(Artwork.objects.count(), 1)
        self.assertRedirects(
            response,
            reverse(
                "dashboard:artwork_overview",
                kwargs={"slug": artwork.slug},
            ),
        )

    def test_success_message_after_creating_artwork(self):
        response = self.client.post(
            self.url,
            {
                "title": "New Artwork",
                "collection": self.collection.pk,
                "image": self.get_test_image(),
            },
        )

        messages = [str(message) for message in get_messages(response.wsgi_request)]

        self.assertIn(
            '"New Artwork" was added successfully.',
            messages,
        )

    def test_invalid_post_does_not_create_artwork(self):
        response = self.client.post(
            self.url,
            {
                "title": "",
                "collection": self.collection.pk,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Artwork.objects.count(), 0)
        self.assertFalse(response.context["form"].is_valid())
        self.assertIn("title", response.context["form"].errors)
        self.assertIn("image", response.context["form"].errors)
