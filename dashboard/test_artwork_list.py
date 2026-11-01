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
        """
        Test that artworks display newest first by default.
        """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "dashboard/artwork_list.html",
        )
        self.assertEqual(
            self.get_artwork_titles(response),
            ["Silent Dream", "Golden Sky", "Blue Dream"],
        )

    def test_search_matches_titles_case_insensitively(self):
        response = self.client.get(self.url, {"q": "DREAM"})

        self.assertEqual(
            self.get_artwork_titles(response),
            ["Silent Dream", "Blue Dream"],
        )

    def test_filter_by_collection(self):
        response = self.client.get(
            self.url,
            {"collection": self.collection.pk},
        )

        self.assertEqual(
            self.get_artwork_titles(response),
            ["Silent Dream", "Blue Dream"],
        )

    def test_filter_by_year_availability(self):
        expected = {
            "present": ["Golden Sky", "Blue Dream"],
            "missing": ["Silent Dream"],
        }

        for value, titles in expected.items():
            with self.subTest(year=value):
                response = self.client.get(self.url, {"year": value})
                self.assertEqual(
                    self.get_artwork_titles(response),
                    titles,
                )

    def test_filter_by_etsy_url_availability(self):
        expected = {
            "present": ["Blue Dream"],
            "missing": ["Silent Dream", "Golden Sky"],
        }

        for value, titles in expected.items():
            with self.subTest(etsy=value):
                response = self.client.get(self.url, {"etsy": value})
                self.assertEqual(
                    self.get_artwork_titles(response),
                    titles,
                )

    def test_filter_by_description_availability(self):
        expected = {
            "present": ["Blue Dream"],
            "missing": ["Silent Dream", "Golden Sky"],
        }

        for value, titles in expected.items():
            with self.subTest(description=value):
                response = self.client.get(
                    self.url,
                    {"description": value},
                )
                self.assertEqual(
                    self.get_artwork_titles(response),
                    titles,
                )

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
        self.assertEqual(
            response.context["page_obj"].paginator.num_pages,
            2,
        )

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
        self.assertEqual(
            response.context["page_obj"].number,
            1,
        )

        response = self.client.get(self.url, {"page": 999})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["page_obj"].number,
            2,
        )
