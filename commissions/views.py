from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

from .forms import CommissionCreativeForm


def commission_creative(request):
    """
    Display and validate the creative commission form.

    Store validated preferences in the session before proceeding
    to the customer details and payment workflow.
    """
    if request.method == "POST":
        # Authentication must be enforced on the server.
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Please log in to submit a commission.")

        form = CommissionCreativeForm(request.POST)

        if form.is_valid():
            # Save validated preferences, not raw POST data.
            request.session["commission_creative"] = form.cleaned_data

            # Temporary redirect until the checkout view exists.
            return redirect("commissions:creative")

    else:
        # Restore preferences when returning to the form.
        saved_preferences = request.session.get("commission_creative")
        form = CommissionCreativeForm(initial=saved_preferences)

    return render(
        request,
        "commissions/commission.html",
        {"form": form},
    )
