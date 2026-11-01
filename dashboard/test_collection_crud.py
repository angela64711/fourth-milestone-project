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
class CollectionListTests(TestCase):
    """
    Test the artist dashboard collection list.
    """

    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()

        cls.artist_user = user_model.objects.create_user(
            username="testartist",
            password="testpassword123",
        )

        artist_group = Group.objects.create(name="Artists")
        cls.artist_user.groups.add(artist_group)

        cls.first_collection = Collection.objects.create(
            name="First Collection",
            slug="first-collection",
            description="First test collection.",
        )

        cls.second_collection = Collection.objects.create(
            name="Second Collection",
            slug="second-collection",
            description="Second test collection.",
        )

        cls.empty_collection = Collection.objects.create(
            name="Empty Collection",
            slug="empty-collection",
            description="A collection without artworks.",
        )

        cls.zebra_artwork = Artwork.objects.create(
            title="Zebra Artwork",
            collection=cls.first_collection,
            image="artworks/zebra.jpg",
        )

        cls.apple_artwork = Artwork.objects.create(
            title="Apple Artwork",
            collection=cls.first_collection,
            image="artworks/apple.jpg",
        )

        cls.other_artwork = Artwork.objects.create(
            title="Other Artwork",
            collection=cls.second_collection,
            image="artworks/other.jpg",
        )

    def setUp(self):
        self.client.force_login(self.artist_user)
        self.url = reverse("dashboard:collection_list")

    def test_collection_list_loads(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "dashboard/collection_list.html",
        )

    def test_all_collections_displayed(self):
        response = self.client.get(self.url)

        collections = response.context["collections"]

        self.assertEqual(len(collections), 3)
        self.assertIn(self.first_collection, collections)
        self.assertIn(self.second_collection, collections)
        self.assertIn(self.empty_collection, collections)

    def test_collection_artwork_counts(self):
        response = self.client.get(self.url)

        collections = {
            collection.pk: collection for collection in response.context["collections"]
        }

        self.assertEqual(
            collections[self.first_collection.pk].artwork_count,
            2,
        )
        self.assertEqual(
            collections[self.second_collection.pk].artwork_count,
            1,
        )
        self.assertEqual(
            collections[self.empty_collection.pk].artwork_count,
            0,
        )

    def test_automatic_collection_cover(self):
        response = self.client.get(self.url)

        collections = {
            collection.pk: collection for collection in response.context["collections"]
        }

        first_collection = collections[self.first_collection.pk]

        self.assertEqual(
            first_collection.ordered_artworks[0],
            self.apple_artwork,
        )

    def test_collections_follow_display_order(self):
        response = self.client.get(self.url)

        collections = list(response.context["collections"])

        self.assertEqual(
            collections,
            [
                self.first_collection,
                self.second_collection,
                self.empty_collection,
            ],
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
class CollectionOrderingTests(TestCase):
    """
    Test changing collection display order in the artist dashboard.
    """

    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()

        cls.artist_user = user_model.objects.create_user(
            username="orderingartist",
            password="testpassword123",
        )

        artist_group = Group.objects.create(name="Artists")
        cls.artist_user.groups.add(artist_group)

        cls.first_collection = Collection.objects.create(
            name="First Collection",
            slug="first-collection",
            description="First test collection.",
        )

        cls.second_collection = Collection.objects.create(
            name="Second Collection",
            slug="second-collection",
            description="Second test collection.",
        )

        cls.third_collection = Collection.objects.create(
            name="Third Collection",
            slug="third-collection",
            description="Third test collection.",
        )

    def setUp(self):
        self.client.force_login(self.artist_user)

    def test_move_collection_down(self):
        """
        Moving the first collection down swaps it with the second.
        """
        url = reverse(
            "dashboard:collection_move",
            args=[self.first_collection.pk, "down"],
        )

        response = self.client.post(url)

        self.assertRedirects(
            response,
            reverse("dashboard:collection_list"),
        )

        collections = list(Collection.objects.all())

        self.assertEqual(
            collections,
            [
                self.second_collection,
                self.first_collection,
                self.third_collection,
            ],
        )

    def test_move_collection_up(self):
        """
        Moving the second collection up swaps it with the first.
        """
        url = reverse(
            "dashboard:collection_move",
            args=[self.second_collection.pk, "up"],
        )

        response = self.client.post(url)

        self.assertRedirects(
            response,
            reverse("dashboard:collection_list"),
        )

        collections = list(Collection.objects.all())

        self.assertEqual(
            collections,
            [
                self.second_collection,
                self.first_collection,
                self.third_collection,
            ],
        )

    def test_order_change_is_persisted(self):
        """
        Updated display order is saved in the database.
        """
        original_order = self.first_collection.display_order

        url = reverse(
            "dashboard:collection_move",
            args=[self.first_collection.pk, "down"],
        )

        self.client.post(url)

        self.first_collection.refresh_from_db()
        self.second_collection.refresh_from_db()

        self.assertEqual(
            self.first_collection.display_order,
            original_order + 1,
        )
        self.assertEqual(
            self.second_collection.display_order,
            original_order,
        )
