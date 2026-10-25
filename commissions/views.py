from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

from .forms import CommissionCreativeForm, CommissionCustomerForm
from .models import CommissionOrder
from .pricing import (
    calculate_commission_total,
    get_artwork_price,
    get_shipping_cost,
)


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
    Collect customer details and display commission pricing.

    Creative preferences determine the artwork price.
    Shipping depends on the selected delivery region.
    No order is created until checkout is implemented.
    """
    preferences = request.session.get("commission_creative")

    if not preferences:
        return redirect("commissions:creative")

    artwork_format = preferences.get("artwork_format")
    artwork_size = preferences.get("artwork_size", "")

    # Reject incomplete or unsupported session selections.
    try:
        artwork_price = get_artwork_price(
            artwork_format,
            artwork_size,
        )
    except ValueError:
        return redirect("commissions:creative")

    requires_shipping = artwork_format in ["print", "framed"]

    if request.method == "POST":
        form = CommissionCustomerForm(
            request.POST,
            artwork_format=artwork_format,
        )

        if form.is_valid():
            customer_details = form.cleaned_data

            # Combine first and last name for the existing model.
            customer_details["full_name"] = (
                f"{customer_details['first_name']} " f"{customer_details['last_name']}"
            )

            # Combine address components for the existing model.
            if requires_shipping:
                address = (
                    f"{customer_details['street']} "
                    f"{customer_details['house_number']}"
                )

                if customer_details["address_line_2"]:
                    address += f"\n{customer_details['address_line_2']}"

                customer_details["shipping_address"] = address
            else:
                customer_details["shipping_address"] = ""

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
            "street": saved_details.get("street", ""),
            "house_number": saved_details.get("house_number", ""),
            "address_line_2": saved_details.get("address_line_2", ""),
            "city": saved_details.get("city", ""),
            "postal_code": saved_details.get("postal_code", ""),
            "country": saved_details.get("country", ""),
        }

        form = CommissionCustomerForm(
            initial=initial,
            artwork_format=artwork_format,
        )

    # Prepare the pricing shown when the page first loads.
    selected_region = form["delivery_region"].value() or ""

    shipping_cost = None
    total_price = None

    if not requires_shipping:
        prices = calculate_commission_total(
            artwork_format,
            artwork_size,
        )
        shipping_cost = prices["shipping_cost"]
        total_price = prices["total_price"]

    elif selected_region in dict(CommissionOrder.DELIVERY_REGION_CHOICES):
        prices = calculate_commission_total(
            artwork_format,
            artwork_size,
            selected_region,
        )
        shipping_cost = prices["shipping_cost"]
        total_price = prices["total_price"]

    # These amounts come from the same pricing configuration
    # used by the server. JavaScript only updates the display.
    europe_shipping = None
    international_shipping = None

    if requires_shipping:
        europe_shipping = get_shipping_cost(
            artwork_format,
            "europe_uk",
        )
        international_shipping = get_shipping_cost(
            artwork_format,
            "international",
        )

    format_labels = dict(CommissionOrder.FORMAT_CHOICES)
    size_labels = dict(CommissionOrder.SIZE_CHOICES)

    creative_approach = (
        "Surprise me"
        if preferences.get("creative_direction") == "surprise"
        else "Your idea"
    )

    return render(
        request,
        "commissions/customer_details.html",
        {
            "form": form,
            "requires_shipping": requires_shipping,
            "creative_approach": creative_approach,
            "artwork_format_label": format_labels[artwork_format],
            "artwork_size_label": size_labels.get(artwork_size, ""),
            "artwork_price": artwork_price,
            "shipping_cost": shipping_cost,
            "total_price": total_price,
            "europe_shipping": europe_shipping,
            "international_shipping": international_shipping,
        },
    )
