from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render

from artworks.models import Artwork


def artist_required(view_func):
    """
    Restrict access to superusers and members of the Artists group.
    """

    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        user = request.user

        if not (user.is_superuser or user.groups.filter(name="Artists").exists()):
            raise PermissionDenied

        return view_func(request, *args, **kwargs)

    return wrapper


@artist_required
def artwork_list(request):
    """
    Display all artworks for artist management.
    """
    artworks = Artwork.objects.select_related("collection").order_by("title")

    return render(
        request,
        "dashboard/artwork_list.html",
        {"artworks": artworks},
    )
