from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render

from .forms import ContactForm


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
                to=["angela.kiratzidou@gmail.com"],
                reply_to=[email],
            )

            try:
                email_message.send(fail_silently=False)
            except Exception:
                messages.error(
                    request, "Your message could not be sent. Please try again later."
                )
            else:
                messages.success(
                    request, "Thank you! Your message has been sent successfully."
                )
                return redirect("contact")
    else:
        form = ContactForm()

    return render(request, "pages/contact.html", {"form": form})
