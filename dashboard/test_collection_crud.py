from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.messages import get_messages
from django.test import TestCase, override_settings
from django.urls import reverse

from artworks.models import Collection
from dashboard.forms import CollectionForm


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
class CollectionAddTests(TestCase):
    """
    Test creating collections through the artist dashboard.
    """

    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()

        cls.artist = user_model.objects.create_user(
            username="collectionaddartist",
            password="testpassword123",
        )

        artist_group, _ = Group.objects.get_or_create(
            name="Artists",
        )
        cls.artist.groups.add(artist_group)

    def setUp(self):
        self.client.force_login(self.artist)
        self.url = reverse("dashboard:collection_add")
        self.valid_data = {
            "name": "Digital Dreams",
            "description": "A collection of digital artworks.",
        }

    def test_add_collection_page_displays_form(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "dashboard/collection_form.html",
        )
        self.assertIsInstance(
            response.context["form"],
            CollectionForm,
        )

    def test_valid_post_creates_collection_and_redirects(self):
        response = self.client.post(
            self.url,
            self.valid_data,
        )

        collection = Collection.objects.get(
            name="Digital Dreams",
        )

        self.assertEqual(Collection.objects.count(), 1)
        self.assertEqual(collection.slug, "digital-dreams")
        self.assertEqual(collection.display_order, 1)

        self.assertRedirects(
            response,
            reverse("dashboard:collection_list"),
        )

    def test_success_message_after_creating_collection(self):
        response = self.client.post(
            self.url,
            self.valid_data,
        )

        messages = [str(message) for message in get_messages(response.wsgi_request)]

        self.assertIn(
            '"Digital Dreams" was added successfully.',
            messages,
        )

    def test_invalid_post_does_not_create_collection(self):
        response = self.client.post(
            self.url,
            {
                "name": "",
                "description": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Collection.objects.count(), 0)
        self.assertFalse(response.context["form"].is_valid())
        self.assertIn("name", response.context["form"].errors)
        self.assertIn("description", response.context["form"].errors)

    def test_duplicate_name_does_not_create_collection(self):
        Collection.objects.create(
            name="Digital Dreams",
            description="An existing collection.",
        )

        response = self.client.post(
            self.url,
            self.valid_data,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Collection.objects.count(), 1)
        self.assertIn(
            "name",
            response.context["form"].errors,
        )

    def test_anonymous_user_cannot_access_add_page(self):
        self.client.logout()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)

    def test_regular_user_cannot_access_add_page(self):
        user_model = get_user_model()

        regular_user = user_model.objects.create_user(
            username="regularcollectionuser",
            password="testpassword123",
        )

        self.client.force_login(regular_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 403)

    def test_regular_user_cannot_create_collection(self):
        user_model = get_user_model()

        regular_user = user_model.objects.create_user(
            username="regularcollectionposter",
            password="testpassword123",
        )

        self.client.force_login(regular_user)

        response = self.client.post(
            self.url,
            self.valid_data,
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Collection.objects.count(), 0)

    def test_superuser_can_create_collection(self):
        user_model = get_user_model()

        superuser = user_model.objects.create_superuser(
            username="collectionsuperuser",
            password="testpassword123",
            email="admin@example.com",
        )

        self.client.force_login(superuser)

        response = self.client.post(
            self.url,
            self.valid_data,
        )

        self.assertRedirects(
            response,
            reverse("dashboard:collection_list"),
        )
        self.assertTrue(
            Collection.objects.filter(
                name="Digital Dreams",
            ).exists()
        )
