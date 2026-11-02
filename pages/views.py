import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.db import DatabaseError
from django.shortcuts import redirect, render

from dashboard.models import IncomingMessage

from .forms import ContactForm

logger = logging.getLogger(__name__)


def index(request):
    return render(request, "pages/index.html")


def about(request):
    return render(request, "pages/about.html")


def retail(request):
    return render(request, "pages/retail.html")


def collaborations(request):
    return render(request, "pages/collaborations.html")


def in_situ(request):
    return render(request, "pages/in-situ.html")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]

            email_message = EmailMessage(
                subject=f"Portfolio contact: {subject}",
                body=f"From: {name}\nEmail: {email}\n\n{message}",
                to=[settings.CONTACT_EMAIL],
                reply_to=[email],
            )

            try:
                email_message.send(fail_silently=False)
            except Exception:
                logger.exception("Contact email sending failed.")
                messages.error(
                    request, "Your message could not be sent. Please try again later."
                )

            else:
                try:
                    IncomingMessage.objects.create(
                        name=name,
                        email=email,
                        subject=subject,
                        message=message,
                    )
                except DatabaseError:
                    logger.exception(
                        "Contact email sent, but message could not be saved."
                    )

                messages.success(
                    request, "Thank you! Your message has been sent successfully."
                )
                return redirect("contact")
    else:
        form = ContactForm()

    return render(request, "pages/contact.html", {"form": form})
