from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase, override_settings
from django.urls import reverse

from artworks.models import Artwork, Collection


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
class DashboardPermissionTests(TestCase):
    """
    Test access to the artist dashboard for different user roles.
    """

    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()

        cls.regular_user = user_model.objects.create_user(
            username="regularuser",
            password="testpassword123",
        )

        cls.artist_user = user_model.objects.create_user(
            username="testartist",
            password="testpassword123",
        )

        cls.artist_group = Group.objects.create(name="Artists")
        cls.artist_user.groups.add(cls.artist_group)

        cls.superuser = user_model.objects.create_superuser(
            username="testadmin",
            email="admin@example.com",
            password="testpassword123",
        )

        cls.collection = Collection.objects.create(
            name="Test Collection",
            slug="test-collection",
            description="A collection for testing.",
        )

        cls.artwork = Artwork.objects.create(
            title="Test Artwork",
            collection=cls.collection,
            image="artworks/test.jpg",
        )

    def setUp(self):
        self.url = reverse("dashboard:home")

    def test_anonymous_user_redirected_to_login(self):
        response = self.client.get(self.url)

        self.assertRedirects(
            response,
            f"/accounts/login/?next={self.url}",
        )

    def test_regular_user_cannot_access_dashboard(self):
        self.client.force_login(self.regular_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 403)

    def test_artist_can_access_dashboard(self):
        self.client.force_login(self.artist_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/artwork_list.html")

    def test_superuser_can_access_dashboard(self):
        self.client.force_login(self.superuser)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/artwork_list.html")

    def test_anonymous_user_redirected_from_artwork_pages(self):
        urls = [
            reverse("dashboard:artwork_add"),
            reverse(
                "dashboard:artwork_overview",
                kwargs={"slug": self.artwork.slug},
            ),
            reverse(
                "dashboard:artwork_edit",
                kwargs={"slug": self.artwork.slug},
            ),
        ]

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)

                self.assertRedirects(
                    response,
                    f"/accounts/login/?next={url}",
                )

    def test_regular_user_cannot_access_artwork_pages(self):
        self.client.force_login(self.regular_user)

        urls = [
            reverse("dashboard:artwork_add"),
            reverse(
                "dashboard:artwork_overview",
                kwargs={"slug": self.artwork.slug},
            ),
            reverse(
                "dashboard:artwork_edit",
                kwargs={"slug": self.artwork.slug},
            ),
        ]

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)

                self.assertEqual(response.status_code, 403)

    def test_artist_can_access_artwork_pages(self):
        self.client.force_login(self.artist_user)

        pages = [
            (
                reverse("dashboard:artwork_add"),
                "dashboard/artwork_form.html",
            ),
            (
                reverse(
                    "dashboard:artwork_overview",
                    kwargs={"slug": self.artwork.slug},
                ),
                "dashboard/artwork_overview.html",
            ),
            (
                reverse(
                    "dashboard:artwork_edit",
                    kwargs={"slug": self.artwork.slug},
                ),
                "dashboard/artwork_form.html",
            ),
        ]

        for url, template in pages:
            with self.subTest(url=url):
                response = self.client.get(url)

                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, template)

    def test_superuser_can_access_artwork_pages(self):
        self.client.force_login(self.superuser)

        pages = [
            (
                reverse("dashboard:artwork_add"),
                "dashboard/artwork_form.html",
            ),
            (
                reverse(
                    "dashboard:artwork_overview",
                    kwargs={"slug": self.artwork.slug},
                ),
                "dashboard/artwork_overview.html",
            ),
            (
                reverse(
                    "dashboard:artwork_edit",
                    kwargs={"slug": self.artwork.slug},
                ),
                "dashboard/artwork_form.html",
            ),
        ]

        for url, template in pages:
            with self.subTest(url=url):
                response = self.client.get(url)

                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, template)

    @override_settings(DEBUG=False)
    def test_regular_user_sees_custom_403_page(self):
        self.client.force_login(self.regular_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, "403.html")
        self.assertContains(
            response,
            "Some spaces are reserved for the artist.",
            status_code=403,
        )
