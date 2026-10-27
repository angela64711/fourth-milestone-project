from decimal import Decimal

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST

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

            # Clear checkout data when commission preferences change.
            request.session.pop("commission_order_id", None)
            request.session.pop("commission_customer", None)

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
    Validated details are saved before proceeding to checkout.
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
            customer_details = form.cleaned_data.copy()

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

            # New checkout details must not reuse an older pending order.
            request.session.pop("commission_order_id", None)

            return redirect("commissions:checkout")

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

    # JavaScript updates the display; Django calculates final prices.
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


@login_required
def commission_checkout(request):
    """
    Create or retrieve a pending commission and Stripe PaymentIntent.

    The payment itself is confirmed through Stripe.js.
    Server-side payment verification is handled separately.
    """
    preferences = request.session.get("commission_creative")
    customer = request.session.get("commission_customer")

    if not preferences:
        return redirect("commissions:creative")

    if not customer:
        return redirect("commissions:customer_details")

    # Validate stored creative preferences.
    creative_form = CommissionCreativeForm(data=preferences)

    if not creative_form.is_valid():
        messages.error(
            request,
            "Please review your commission preferences.",
        )
        return redirect("commissions:creative")

    creative = creative_form.cleaned_data

    # Validate stored customer details.
    customer_form = CommissionCustomerForm(
        data=customer,
        artwork_format=creative["artwork_format"],
    )

    if not customer_form.is_valid():
        messages.error(
            request,
            "Please review your customer details.",
        )
        return redirect("commissions:customer_details")

    details = customer_form.cleaned_data

    # Calculate the authoritative payment amount on the server.
    try:
        prices = calculate_commission_total(
            creative["artwork_format"],
            creative.get("artwork_size", ""),
            details.get("delivery_region", ""),
        )
    except ValueError:
        messages.error(
            request,
            "Unable to calculate the commission total.",
        )
        return redirect("commissions:creative")

    # Reuse a pending order when checkout is refreshed.
    order_id = request.session.get("commission_order_id")
    order = None

    if order_id:
        order = CommissionOrder.objects.filter(
            pk=order_id,
            user=request.user,
            payment_status="pending",
        ).first()

    if order is None:
        shipping_address = ""

        if creative["artwork_format"] != "digital":
            shipping_address = f"{details['street']} {details['house_number']}"

            if details["address_line_2"]:
                shipping_address += f"\n{details['address_line_2']}"

        order = CommissionOrder.objects.create(
            user=request.user,
            creative_direction=creative["creative_direction"],
            story=creative["story"],
            moods=creative["moods"],
            colours=creative["colours"],
            imagery=creative["imagery"],
            artwork_format=creative["artwork_format"],
            artwork_size=creative.get("artwork_size", ""),
            delivery_region=details.get("delivery_region", ""),
            artwork_price=prices["artwork_price"],
            shipping_cost=prices["shipping_cost"],
            total_price=prices["total_price"],
            full_name=(f"{details['first_name']} {details['last_name']}"),
            email=details["email"],
            shipping_address=shipping_address,
            city=details.get("city", ""),
            postal_code=details.get("postal_code", ""),
            country=details.get("country", ""),
        )

        request.session["commission_order_id"] = order.pk

    # Connect the order to a Stripe PaymentIntent.
    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        if order.stripe_payment_intent:
            intent = stripe.PaymentIntent.retrieve(order.stripe_payment_intent)
        else:
            amount = int(order.total_price * Decimal("100"))

            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=settings.STRIPE_CURRENCY,
                metadata={
                    "order_number": str(order.order_number),
                },
                idempotency_key=f"commission-{order.order_number}",
            )

            order.stripe_payment_intent = intent.id
            order.save(update_fields=["stripe_payment_intent", "updated_on"])

    except stripe.StripeError:
        messages.error(
            request,
            "Payment is temporarily unavailable. Please try again.",
        )
        return redirect("commissions:customer_details")

    # Do not offer another payment for a completed PaymentIntent.
    # The confirmation view will verify and reconcile this status.
    if intent.status == "succeeded":
        expected_amount = int(order.total_price * Decimal("100"))

        payment_matches = (
            intent.id == order.stripe_payment_intent
            and intent.amount == expected_amount
            and intent.currency.lower() == settings.STRIPE_CURRENCY.lower()
            and intent.metadata.to_dict().get("order_number") == str(order.order_number)
        )

        if not payment_matches:
            messages.error(
                request,
                "The payment details could not be verified.",
            )
            return redirect("commissions:customer_details")

        order.payment_status = "paid"
        order.save(update_fields=["payment_status", "updated_on"])

        request.session.pop("commission_order_id", None)
        request.session.pop("commission_creative", None)
        request.session.pop("commission_customer", None)

        return redirect(
            "commissions:success",
            order_number=order.order_number,
        )

    return render(
        request,
        "commissions/checkout.html",
        {
            "order": order,
            "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
            "client_secret": intent.client_secret,
        },
    )


@login_required
@require_POST
def commission_verify_payment(request, order_number):
    """
    Verify payment directly with Stripe before marking an order paid.
    """
    order = get_object_or_404(
        CommissionOrder,
        order_number=order_number,
        user=request.user,
    )

    if not order.stripe_payment_intent:
        return JsonResponse(
            {"success": False, "message": "No payment was found."},
            status=400,
        )

    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        intent = stripe.PaymentIntent.retrieve(order.stripe_payment_intent)
    except stripe.StripeError:
        return JsonResponse(
            {
                "success": False,
                "message": "Payment verification is temporarily unavailable.",
            },
            status=503,
        )

    expected_amount = int(order.total_price * Decimal("100"))

    # Ensure the Stripe payment matches this exact order.
    payment_matches = (
        intent.id == order.stripe_payment_intent
        and intent.amount == expected_amount
        and intent.currency.lower() == settings.STRIPE_CURRENCY.lower()
        and intent.metadata.to_dict().get("order_number") == str(order.order_number)
    )

    if not payment_matches:
        return JsonResponse(
            {
                "success": False,
                "message": "Payment details could not be verified.",
            },
            status=400,
        )

    if intent.status != "succeeded":
        return JsonResponse(
            {
                "success": False,
                "message": "Your payment has not been completed.",
            },
            status=400,
        )

    # Payment is verified; update the existing order.
    if order.payment_status != "paid":
        order.payment_status = "paid"
        order.save(update_fields=["payment_status", "updated_on"])

    # Clear completed checkout information.
    request.session.pop("commission_order_id", None)
    request.session.pop("commission_creative", None)
    request.session.pop("commission_customer", None)

    return JsonResponse(
        {
            "success": True,
            "redirect_url": reverse(
                "commissions:success",
                args=[order.order_number],
            ),
        }
    )


@login_required
def commission_success(request, order_number):
    """Display a successfully paid commission to its customer."""
    order = get_object_or_404(
        CommissionOrder,
        order_number=order_number,
        user=request.user,
        payment_status="paid",
    )

    return render(
        request,
        "commissions/checkout_success.html",
        {"order": order},
    )
