from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .forms import CommissionCreativeForm


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
    """Display customer details after creative preferences."""

    if "commission_creative" not in request.session:
        return redirect("commissions:creative")

    return render(
        request,
        "commissions/customer_details.html",
        {"account_email": request.user.email},
    )
