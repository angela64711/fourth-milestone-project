from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from allauth.account.models import EmailAddress

from .forms import CommissionCreativeForm


def commission_creative(request):
    """
    Display and validate creative commission preferences.

    Store validated preferences in the session and show the
    email confirmation modal before customer details.
    """
    if request.method == "POST":
        # Authentication must be enforced on the server.
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Please log in to create a commission.")

        form = CommissionCreativeForm(request.POST)

        if form.is_valid():
            # Store only validated creative preferences.
            request.session["commission_creative"] = form.cleaned_data

            # Open the email confirmation modal after redirecting.
            request.session["show_email_modal"] = True

            return redirect("commissions:creative")

    else:
        # Restore preferences when returning to the form.
        saved_preferences = request.session.get("commission_creative")
        form = CommissionCreativeForm(initial=saved_preferences)

    # Retrieve and remove the one-time modal flag.
    show_email_modal = request.session.pop("show_email_modal", False)

    email_address = None

    if show_email_modal and request.user.is_authenticated:
        # Retrieve the customer's primary Allauth email record.
        email_address = EmailAddress.objects.filter(
            user=request.user,
            primary=True,
        ).first()

        # Fallback if no email record is marked as primary.
        if email_address is None:
            email_address = EmailAddress.objects.filter(
                user=request.user,
                email__iexact=request.user.email,
            ).first()

    return render(
        request,
        "commissions/commission.html",
        {
            "form": form,
            "show_email_modal": show_email_modal,
            "email_address": email_address,
        },
    )


@login_required
@require_POST
def commission_send_verification(request):
    """Send an Allauth verification email for the customer's account."""

    if "commission_creative" not in request.session:
        return redirect("commissions:creative")

    email_address = EmailAddress.objects.filter(
        user=request.user,
        primary=True,
    ).first()

    if email_address is None:
        email_address = EmailAddress.objects.filter(
            user=request.user,
            email__iexact=request.user.email,
        ).first()

    if email_address is None:
        messages.error(
            request, "No email address was found. Please update your account email."
        )

    elif email_address.verified:
        messages.info(request, "Your email address is already verified.")

    else:
        email_address.send_confirmation(request)
        messages.success(request, "Verification email sent. Please check your inbox.")

    return redirect("commissions:creative")


@login_required
def commission_customer_details(request):
    """Allow verified customers to continue to order details."""

    if "commission_creative" not in request.session:
        return redirect("commissions:creative")

    email_address = EmailAddress.objects.filter(
        user=request.user,
        primary=True,
        verified=True,
    ).first()

    if email_address is None:
        messages.error(request, "Please verify your email address before continuing.")
        request.session["show_email_modal"] = True
        return redirect("commissions:creative")

    return render(
        request,
        "commissions/customer_details.html",
        {"email_address": email_address},
    )
