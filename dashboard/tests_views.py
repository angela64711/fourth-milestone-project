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

    def test_combined_search_and_collection_filter(self):
        response = self.client.get(
            self.url,
            {
                "q": "dream",
                "collection": self.collection.pk,
                "year": "present",
            },
        )

        self.assertEqual(
            self.get_artwork_titles(response),
            ["Blue Dream"],
        )

    def test_sort_by_most_recent(self):
        response = self.client.get(self.url, {"sort": "recent"})

        self.assertEqual(
            self.get_artwork_titles(response),
            ["Silent Dream", "Golden Sky", "Blue Dream"],
        )

    def test_invalid_page_number_returns_last_page(self):
        for number in range(37):
            Artwork.objects.create(
                title=f"Pagination Artwork {number:02d}",
                collection=self.collection,
                image=f"artworks/pagination-{number}.jpg",
            )

        response = self.client.get(self.url, {"page": "invalid"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page_obj"].number, 1)

        response = self.client.get(self.url, {"page": 999})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page_obj"].number, 2)


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
