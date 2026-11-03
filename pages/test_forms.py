from django.test import SimpleTestCase

from .forms import ContactForm


class ContactFormTest(SimpleTestCase):
    """Tests contact form fields and validation."""

    def setUp(self):
        self.valid_data = {
            "name": "Test Visitor",
            "email": "visitor@example.com",
            "subject": "Artwork enquiry",
            "message": "I would like to ask about your artwork.",
        }

    def test_form_accepts_valid_data(self):
        form = ContactForm(data=self.valid_data)

        self.assertTrue(form.is_valid())

    def test_all_fields_are_required(self):
        for field in self.valid_data:
            with self.subTest(field=field):
                invalid_data = self.valid_data.copy()
                invalid_data[field] = ""

                form = ContactForm(data=invalid_data)

                self.assertFalse(form.is_valid())
                self.assertIn(field, form.errors)

    def test_invalid_email_is_rejected(self):
        invalid_data = self.valid_data.copy()
        invalid_data["email"] = "not-an-email"

        form = ContactForm(data=invalid_data)

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_name_maximum_length(self):
        valid_data = self.valid_data.copy()
        valid_data["name"] = "A" * 100

        self.assertTrue(ContactForm(data=valid_data).is_valid())

        valid_data["name"] = "A" * 101

        form = ContactForm(data=valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_subject_maximum_length(self):
        valid_data = self.valid_data.copy()
        valid_data["subject"] = "A" * 150

        self.assertTrue(ContactForm(data=valid_data).is_valid())

        valid_data["subject"] = "A" * 151

        form = ContactForm(data=valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("subject", form.errors)

    def test_message_maximum_length(self):
        valid_data = self.valid_data.copy()
        valid_data["message"] = "A" * 2000

        self.assertTrue(ContactForm(data=valid_data).is_valid())

        valid_data["message"] = "A" * 2001

        form = ContactForm(data=valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("message", form.errors)
