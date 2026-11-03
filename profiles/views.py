from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from commissions.models import CommissionOrder
from artworks.models import Favourite


@login_required
def my_account(request):
    """
    Display the logged-in user's paid commission history.
    """
    favourites = Favourite.objects.filter(user=request.user).select_related(
        "artwork", "artwork__collection"
    )

    orders = list(
        CommissionOrder.objects.filter(
            user=request.user,
            payment_status="paid",
        ).order_by("-created_on")
    )

    mood_choices = dict(CommissionOrder.MOOD_CHOICES)
    colour_choices = dict(CommissionOrder.COLOUR_CHOICES)

    for order in orders:
        order.mood_labels = [mood_choices.get(value, value) for value in order.moods]
        order.colour_labels = [
            colour_choices.get(value, value) for value in order.colours
        ]

    return render(
        request,
        "profiles/my_account.html",
        {
            "favourites": favourites,
            "orders": orders,
        },
    )
