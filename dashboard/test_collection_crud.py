from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.messages import get_messages
from django.test import TestCase, override_settings
from django.urls import reverse

from artworks.models import Artwork, Collection
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
class CollectionEditTests(TestCase):
    """
    Test editing collections and selecting cover artwork.
    """

    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()

        cls.artist = user_model.objects.create_user(
            username="collectioneditartist",
            password="testpassword123",
        )
        artist_group, _ = Group.objects.get_or_create(name="Artists")
        cls.artist.groups.add(artist_group)

        cls.collection = Collection.objects.create(
            name="Original Collection",
            description="Original description.",
        )
        cls.artwork = Artwork.objects.create(
            title="Selected Cover",
            collection=cls.collection,
            image="artworks/selected.jpg",
        )
        cls.other_collection = Collection.objects.create(
            name="Other Collection",
            description="Another collection.",
        )
        cls.other_artwork = Artwork.objects.create(
            title="Other Artwork",
            collection=cls.other_collection,
            image="artworks/other.jpg",
        )

    def setUp(self):
        self.client.force_login(self.artist)
        self.url = reverse(
            "dashboard:collection_edit",
            kwargs={"slug": self.collection.slug},
        )
        self.valid_data = {
            "name": "Updated Collection",
            "description": "Updated description.",
            "cover_artwork": str(self.artwork.pk),
        }

    def test_edit_page_displays_existing_collection(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "dashboard/collection_form.html",
        )
        self.assertEqual(
            response.context["form"].instance,
            self.collection,
        )
        self.assertContains(response, self.artwork.title)

    def test_valid_post_updates_collection_and_redirects(self):
        response = self.client.post(self.url, self.valid_data)
        self.collection.refresh_from_db()

        self.assertEqual(self.collection.name, "Updated Collection")
        self.assertEqual(
            self.collection.description,
            "Updated description.",
        )
        self.assertEqual(
            self.collection.slug,
            "original-collection",
        )
        self.assertRedirects(
            response,
            reverse(
                "dashboard:collection_overview",
                kwargs={"slug": self.collection.slug},
            ),
        )

    def test_valid_post_saves_selected_cover(self):
        self.client.post(self.url, self.valid_data)
        self.collection.refresh_from_db()

        self.assertEqual(
            self.collection.cover_artwork,
            self.artwork,
        )

    def test_empty_cover_selection_uses_fallback(self):
        self.collection.cover_artwork = self.artwork
        self.collection.save()

        data = {**self.valid_data, "cover_artwork": ""}
        self.client.post(self.url, data)
        self.collection.refresh_from_db()

        self.assertIsNone(self.collection.cover_artwork)
        self.assertEqual(self.collection.cover, self.artwork)

    def test_invalid_form_does_not_update_collection(self):
        data = {
            **self.valid_data,
            "name": "",
        }

        response = self.client.post(self.url, data)
        self.collection.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertIn("name", response.context["form"].errors)
        self.assertEqual(self.collection.name, "Original Collection")
        self.assertIsNone(self.collection.cover_artwork)

    def test_duplicate_name_is_rejected(self):
        data = {
            **self.valid_data,
            "name": self.other_collection.name,
        }

        response = self.client.post(self.url, data)
        self.collection.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertIn("name", response.context["form"].errors)
        self.assertEqual(self.collection.name, "Original Collection")

    def test_cover_from_another_collection_is_rejected(self):
        data = {
            **self.valid_data,
            "cover_artwork": str(self.other_artwork.pk),
        }

        response = self.client.post(self.url, data)
        self.collection.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].non_field_errors())
        self.assertEqual(self.collection.name, "Original Collection")
        self.assertIsNone(self.collection.cover_artwork)

    def test_nonexistent_cover_is_rejected(self):
        data = {
            **self.valid_data,
            "cover_artwork": "999999",
        }

        response = self.client.post(self.url, data)
        self.collection.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].non_field_errors())
        self.assertIsNone(self.collection.cover_artwork)

    def test_nonnumeric_cover_is_rejected_gracefully(self):
        data = {
            **self.valid_data,
            "cover_artwork": "invalid",
        }

        response = self.client.post(self.url, data)
        self.collection.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].non_field_errors())
        self.assertIsNone(self.collection.cover_artwork)

    def test_missing_collection_returns_404(self):
        url = reverse(
            "dashboard:collection_edit",
            kwargs={"slug": "nonexistent-collection"},
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_anonymous_user_cannot_edit_collection(self):
        self.client.logout()

        response = self.client.post(self.url, self.valid_data)
        self.collection.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.collection.name, "Original Collection")

    def test_regular_user_cannot_edit_collection(self):
        regular_user = get_user_model().objects.create_user(
            username="regularcollectioneditor",
            password="testpassword123",
        )
        self.client.force_login(regular_user)

        response = self.client.post(self.url, self.valid_data)
        self.collection.refresh_from_db()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.collection.name, "Original Collection")

    def test_superuser_can_edit_collection(self):
        superuser = get_user_model().objects.create_superuser(
            username="collectioneditsuperuser",
            email="admin@example.com",
            password="testpassword123",
        )
        self.client.force_login(superuser)

        response = self.client.post(self.url, self.valid_data)
        self.collection.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.collection.name, "Updated Collection")
