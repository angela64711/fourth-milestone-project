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
        ]

        for url, template in pages:
            with self.subTest(url=url):
                response = self.client.get(url)

                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, template)


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
class DashboardArtworkListTests(TestCase):
    """
    Test dashboard artwork searching, filtering, sorting and pagination.
    """

    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        cls.artist = user_model.objects.create_user(
            username="listartist",
            password="testpassword123",
        )
        artist_group, _ = Group.objects.get_or_create(name="Artists")
        cls.artist.groups.add(artist_group)

        cls.collection = Collection.objects.create(
            name="Dreamscapes",
            slug="dreamscapes",
            description="Dreamlike artworks.",
        )
        cls.other_collection = Collection.objects.create(
            name="Collages",
            slug="collages",
            description="Collage artworks.",
        )

        cls.first = Artwork.objects.create(
            title="Blue Dream",
            collection=cls.collection,
            year=2024,
            description="A blue composition.",
            image="artworks/blue.jpg",
            etsy_url="https://www.etsy.com/listing/111111111",
        )
        cls.second = Artwork.objects.create(
            title="Golden Sky",
            collection=cls.other_collection,
            year=2022,
            image="artworks/golden.jpg",
        )
        cls.third = Artwork.objects.create(
            title="Silent Dream",
            collection=cls.collection,
            image="artworks/silent.jpg",
        )

    def setUp(self):
        self.client.force_login(self.artist)
        self.url = reverse("dashboard:home")

    def get_artwork_titles(self, response):
        return [artwork.title for artwork in response.context["page_obj"].object_list]

    def test_artwork_list_displays_all_artworks(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/artwork_list.html")
        self.assertEqual(
            self.get_artwork_titles(response),
            ["Blue Dream", "Golden Sky", "Silent Dream"],
        )

    def test_search_matches_titles_case_insensitively(self):
        response = self.client.get(self.url, {"q": "DREAM"})

        self.assertEqual(
            self.get_artwork_titles(response),
            ["Blue Dream", "Silent Dream"],
        )

    def test_filter_by_collection(self):
        response = self.client.get(
            self.url,
            {"collection": self.collection.pk},
        )

        self.assertEqual(
            self.get_artwork_titles(response),
            ["Blue Dream", "Silent Dream"],
        )

    def test_filter_by_year_availability(self):
        expected = {
            "present": ["Blue Dream", "Golden Sky"],
            "missing": ["Silent Dream"],
        }

        for value, titles in expected.items():
            with self.subTest(year=value):
                response = self.client.get(self.url, {"year": value})
                self.assertEqual(self.get_artwork_titles(response), titles)

    def test_filter_by_etsy_url_availability(self):
        expected = {
            "present": ["Blue Dream"],
            "missing": ["Golden Sky", "Silent Dream"],
        }

        for value, titles in expected.items():
            with self.subTest(etsy=value):
                response = self.client.get(self.url, {"etsy": value})
                self.assertEqual(self.get_artwork_titles(response), titles)

    def test_filter_by_description_availability(self):
        expected = {
            "present": ["Blue Dream"],
            "missing": ["Golden Sky", "Silent Dream"],
        }

        for value, titles in expected.items():
            with self.subTest(description=value):
                response = self.client.get(
                    self.url,
                    {"description": value},
                )
                self.assertEqual(self.get_artwork_titles(response), titles)

    def test_sort_by_year_descending_with_missing_last(self):
        response = self.client.get(self.url, {"sort": "year"})

        self.assertEqual(
            self.get_artwork_titles(response),
            ["Blue Dream", "Golden Sky", "Silent Dream"],
        )

    def test_sort_by_title(self):
        response = self.client.get(self.url, {"sort": "title"})

        self.assertEqual(
            self.get_artwork_titles(response),
            ["Blue Dream", "Golden Sky", "Silent Dream"],
        )

    def test_pagination_limits_artworks_to_36_per_page(self):
        for number in range(37):
            Artwork.objects.create(
                title=f"Extra Artwork {number:02d}",
                collection=self.collection,
                image=f"artworks/extra-{number}.jpg",
            )

        response = self.client.get(self.url)

        self.assertEqual(len(response.context["page_obj"]), 36)
        self.assertEqual(response.context["page_obj"].paginator.num_pages, 2)

        response = self.client.get(self.url, {"page": 2})

        self.assertEqual(len(response.context["page_obj"]), 4)

    def test_filters_are_preserved_in_pagination_query_string(self):
        response = self.client.get(
            self.url,
            {
                "q": "Dream",
                "collection": self.collection.pk,
                "page": 2,
            },
        )

        query_string = response.context["query_string"]

        self.assertIn("q=Dream", query_string)
        self.assertIn(
            f"collection={self.collection.pk}",
            query_string,
        )
        self.assertNotIn("page=", query_string)
