from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from artworks.models import Artwork, Collection, Favourite
from commissions.models import CommissionOrder


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
class MyAccountViewTest(TestCase):
    """Tests My Account access, favourites and paid commissions."""

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            username="profileuser",
            password="TestPassword123!",
        )
        cls.other_user = User.objects.create_user(
            username="otherprofileuser",
            password="TestPassword123!",
        )

        cls.collection = Collection.objects.create(
            name="Profile Test Collection",
            description="Collection for profile tests.",
        )
        cls.artwork = Artwork.objects.create(
            title="Profile Test Artwork",
            collection=cls.collection,
            image="artworks/profile-test.jpg",
        )
        cls.other_artwork = Artwork.objects.create(
            title="Other Profile Artwork",
            collection=cls.collection,
            image="artworks/other-profile-test.jpg",
        )

        cls.favourite = Favourite.objects.create(
            user=cls.user,
            artwork=cls.artwork,
        )
        cls.other_favourite = Favourite.objects.create(
            user=cls.other_user,
            artwork=cls.other_artwork,
        )

        cls.paid_order = CommissionOrder.objects.create(
            user=cls.user,
            creative_direction="idea",
            story="A dreamlike landscape.",
            moods=["dreamlike", "serene"],
            colours=["pink", "blue"],
            artwork_format="digital",
            artwork_price="100.00",
            total_price="100.00",
            full_name="Profile Test User",
            email="profile@example.com",
            payment_status="paid",
        )

        cls.pending_order = CommissionOrder.objects.create(
            user=cls.user,
            creative_direction="surprise",
            artwork_format="digital",
            artwork_price="100.00",
            total_price="100.00",
            full_name="Profile Test User",
            email="profile@example.com",
            payment_status="pending",
        )

        cls.other_order = CommissionOrder.objects.create(
            user=cls.other_user,
            creative_direction="surprise",
            artwork_format="digital",
            artwork_price="100.00",
            total_price="100.00",
            full_name="Other Profile User",
            email="other@example.com",
            payment_status="paid",
        )

        cls.url = reverse("profiles:my_account")

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_my_account_page_loads_for_logged_in_user(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profiles/my_account.html")

    def test_only_current_users_favourites_are_displayed(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)
        favourites = response.context["favourites"]

        self.assertIn(self.favourite, favourites)
        self.assertNotIn(self.other_favourite, favourites)
        self.assertEqual(len(favourites), 1)

    def test_only_current_users_paid_orders_are_displayed(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)
        orders = response.context["orders"]

        self.assertIn(self.paid_order, orders)
        self.assertNotIn(self.pending_order, orders)
        self.assertNotIn(self.other_order, orders)
        self.assertEqual(len(orders), 1)

    def test_mood_and_colour_labels_are_converted(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)
        order = response.context["orders"][0]

        self.assertEqual(
            order.mood_labels,
            ["Dreamlike", "Serene"],
        )
        self.assertEqual(
            order.colour_labels,
            ["Dusty Rose", "Navy Blue"],
        )

    def test_empty_account_has_no_favourites_or_orders(self):
        empty_user = get_user_model().objects.create_user(
            username="emptyprofileuser",
            password="TestPassword123!",
        )
        self.client.force_login(empty_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["favourites"]), 0)
        self.assertEqual(len(response.context["orders"]), 0)
