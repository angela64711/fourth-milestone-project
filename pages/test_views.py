from unittest.mock import patch

from django.contrib.messages import get_messages
from django.core import mail
from django.db import DatabaseError
from django.test import TestCase, override_settings
from django.urls import reverse

from dashboard.models import IncomingMessage


@override_settings(
    STORAGES={
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    },
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    CONTACT_EMAIL="artist@example.com",
)
class StaticPagesViewTest(TestCase):
    """Tests the informational pages and their templates."""

    def test_static_pages_load_correct_templates(self):
        pages = {
            "home": "pages/index.html",
            "about": "pages/about.html",
            "retail": "pages/retail.html",
            "collaborations": "pages/collaborations.html",
            "in_situ": "pages/in-situ.html",
        }

        for url_name, template in pages.items():
            with self.subTest(page=url_name):
                response = self.client.get(reverse(url_name))

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
    },
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    CONTACT_EMAIL="artist@example.com",
)
class ContactViewTest(TestCase):
    """Tests contact form display, submission and error handling."""

    def setUp(self):
        self.url = reverse("contact")
        self.valid_data = {
            "name": "Test Visitor",
            "email": "visitor@example.com",
            "subject": "Artwork enquiry",
            "message": "I would like to ask about your artwork.",
        }

    def test_contact_page_displays_form(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/contact.html")
        self.assertIn("form", response.context)

    def test_invalid_submission_does_not_send_or_save(self):
        invalid_data = self.valid_data.copy()
        invalid_data["email"] = "invalid-email"

        response = self.client.post(self.url, invalid_data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["form"].is_valid())
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(IncomingMessage.objects.count(), 0)

    def test_valid_submission_sends_email_and_saves_message(self):
        response = self.client.post(self.url, self.valid_data)

        self.assertRedirects(response, self.url)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(IncomingMessage.objects.count(), 1)

        sent_email = mail.outbox[0]
        self.assertEqual(
            sent_email.subject,
            "Portfolio contact: Artwork enquiry",
        )
        self.assertEqual(sent_email.to, ["artist@example.com"])
        self.assertEqual(
            sent_email.reply_to,
            ["visitor@example.com"],
        )
        self.assertIn(self.valid_data["message"], sent_email.body)

        saved_message = IncomingMessage.objects.get()
        self.assertEqual(saved_message.name, "Test Visitor")
        self.assertEqual(saved_message.email, "visitor@example.com")
        self.assertEqual(saved_message.subject, "Artwork enquiry")
        self.assertEqual(
            saved_message.message,
            self.valid_data["message"],
        )

        messages = [str(message) for message in get_messages(response.wsgi_request)]
        self.assertIn(
            "Thank you! Your message has been sent successfully.",
            messages,
        )

    @patch("pages.views.EmailMessage.send")
    def test_email_failure_does_not_save_message(self, mock_send):
        mock_send.side_effect = Exception("Email service unavailable")

        with patch("pages.views.logger.exception"):
            response = self.client.post(self.url, self.valid_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(IncomingMessage.objects.count(), 0)

        messages = [str(message) for message in get_messages(response.wsgi_request)]
        self.assertIn(
            "Your message could not be sent. Please try again later.",
            messages,
        )

    @patch("pages.views.IncomingMessage.objects.create")
    def test_database_failure_after_email_is_handled(self, mock_create):
        mock_create.side_effect = DatabaseError("Database unavailable")

        with patch("pages.views.logger.exception"):
            response = self.client.post(self.url, self.valid_data)

        self.assertRedirects(response, self.url)
        self.assertEqual(len(mail.outbox), 1)

        messages = [str(message) for message in get_messages(response.wsgi_request)]
        self.assertIn(
            "Thank you! Your message has been sent successfully.",
            messages,
        )
