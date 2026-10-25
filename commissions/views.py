from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

from .forms import CommissionCreativeForm, CommissionCustomerForm


def commission_creative(request):
    """
    Display and validate creative commission preferences.

    Save validated preferences in the session before
    continuing to customer details.
    """
    if request.method == "POST":
        # Authentication must also be enforced on the server.
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Please log in to create a commission.")

        form = CommissionCreativeForm(request.POST)

        if form.is_valid():
            request.session["commission_creative"] = form.cleaned_data

            # Continue directly to customer details.
            return redirect("commissions:customer_details")

    else:
        # Restore previously saved preferences.
        saved_preferences = request.session.get("commission_creative")
        form = CommissionCreativeForm(initial=saved_preferences)

    return render(
        request,
        "commissions/commission.html",
        {"form": form},
    )


@login_required
def commission_customer_details(request):
    """
    Collect customer information for a commission.

    The artwork format comes from validated session data.
    Customer details are temporarily saved until checkout
    and order creation are implemented.
    """
    preferences = request.session.get("commission_creative")

    if not preferences:
        return redirect("commissions:creative")

    artwork_format = preferences.get("artwork_format")

    if artwork_format not in ["digital", "print", "framed"]:
        return redirect("commissions:creative")

    requires_shipping = artwork_format in ["print", "framed"]

    if request.method == "POST":
        form = CommissionCustomerForm(
            request.POST,
            artwork_format=artwork_format,
        )

        if form.is_valid():
            customer_details = form.cleaned_data

            customer_details["full_name"] = (
                f"{customer_details['first_name']} " f"{customer_details['last_name']}"
            )

            request.session["commission_customer"] = customer_details

            messages.success(
                request,
                "Your customer details have been saved.",
            )

            return redirect("commissions:customer_details")

    else:
        saved_details = request.session.get("commission_customer", {})

        initial = {
            "first_name": saved_details.get(
                "first_name",
                request.user.first_name,
            ),
            "last_name": saved_details.get(
                "last_name",
                request.user.last_name,
            ),
            "email": saved_details.get(
                "email",
                request.user.email,
            ),
            "delivery_region": saved_details.get("delivery_region", ""),
            "shipping_address": saved_details.get("shipping_address", ""),
            "city": saved_details.get("city", ""),
            "postal_code": saved_details.get("postal_code", ""),
            "country": saved_details.get("country", ""),
        }

        form = CommissionCustomerForm(
            initial=initial,
            artwork_format=artwork_format,
        )

    return render(
        request,
        "commissions/customer_details.html",
        {
            "form": form,
            "requires_shipping": requires_shipping,
            "artwork_format": artwork_format,
            "artwork_size": preferences.get("artwork_size", ""),
        },
    )
