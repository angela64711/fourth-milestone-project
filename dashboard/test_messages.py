from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import IncomingMessage


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
class MessageDashboardTests(TestCase):
    """
    Test incoming message listing, display and permissions
    in the artist dashboard.
    """

    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()

        cls.artist = user_model.objects.create_user(
            username="messageartist",
            password="testpassword123",
        )

        artist_group, _ = Group.objects.get_or_create(
            name="Artists",
        )
        cls.artist.groups.add(artist_group)

        cls.regular_user = user_model.objects.create_user(
            username="messageregular",
            password="testpassword123",
        )

        cls.superuser = user_model.objects.create_superuser(
            username="messageadmin",
            email="admin@example.com",
            password="testpassword123",
        )

        cls.first_message = IncomingMessage.objects.create(
            name="First Sender",
            email="first@example.com",
            subject="First enquiry",
            message="This is the first contact message.",
        )

        cls.second_message = IncomingMessage.objects.create(
            name="Second Sender",
            email="second@example.com",
            subject="Second enquiry",
            message="This is the second contact message.",
        )

    def setUp(self):
        self.client.force_login(self.artist)
        self.list_url = reverse("dashboard:message_list")

    def test_message_list_uses_correct_template(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "dashboard/message_list.html",
        )

    def test_message_list_displays_saved_messages(self):
        response = self.client.get(self.list_url)

        self.assertContains(response, "First Sender")
        self.assertContains(response, "first@example.com")
        self.assertContains(response, "First enquiry")
        self.assertContains(
            response,
            "This is the first contact message.",
        )

        self.assertContains(response, "Second Sender")
        self.assertContains(response, "Second enquiry")

    def test_messages_are_ordered_newest_first(self):
        response = self.client.get(self.list_url)

        incoming_messages = list(response.context["incoming_messages"])

        self.assertEqual(
            incoming_messages,
            [self.second_message, self.first_message],
        )

    def test_empty_message_list_displays_empty_state(self):
        IncomingMessage.objects.all().delete()

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No messages yet")
        self.assertQuerySetEqual(
            response.context["incoming_messages"],
            [],
        )

    def test_anonymous_user_redirected_to_login(self):
        self.client.logout()

        response = self.client.get(self.list_url)

        self.assertRedirects(
            response,
            f"/accounts/login/?next={self.list_url}",
        )

    def test_regular_user_cannot_access_messages(self):
        self.client.force_login(self.regular_user)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 403)

    def test_superuser_can_access_messages(self):
        self.client.force_login(self.superuser)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "dashboard/message_list.html",
        )
