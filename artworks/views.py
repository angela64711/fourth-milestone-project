from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.html import format_html
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse

from .models import Artwork, Collection, Favourite


def collections(request):
    """
    Display collections containing artworks, with automatic covers.
    """
    collections = Collection.objects.filter(artworks__isnull=False).distinct()

    return render(
        request,
        "artworks/collections.html",
        {"collections": collections},
    )


def artworks(request, slug):
    """
    Display a collection and its paginated artworks.
    """
    collection = get_object_or_404(Collection, slug=slug)

    artworks = Artwork.objects.filter(collection=collection).order_by(
        "-year",
        "title",
    )

    paginator = Paginator(artworks, 24)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "collection": collection,
        "page_obj": page_obj,
    }

    return render(request, "artworks/artworks.html", context)


def artwork_detail(request, slug):
    """
    Display an artwork and its details, including favourite status.
    """
    artwork = get_object_or_404(Artwork, slug=slug)

    is_favourite = (
        request.user.is_authenticated
        and Favourite.objects.filter(
            user=request.user,
            artwork=artwork,
        ).exists()
    )

    context = {
        "artwork": artwork,
        "gallery_page": request.GET.get("page", "1"),
        "is_favourite": is_favourite,
        "from_favourites": request.GET.get("from") == "favourites",
    }

    return render(request, "artworks/artwork_detail.html", context)


@login_required
@require_POST
def toggle_favourite(request, slug):
    """
    Add or remove an artwork from the user's favourites.
    """
    artwork = get_object_or_404(Artwork, slug=slug)

    favourite, created = Favourite.objects.get_or_create(
        user=request.user,
        artwork=artwork,
    )

    if created:
        favourites_url = reverse("profiles:my_account") + "#my-favourites"

        # Include a link to My Favourites in the success message when artwork is added.
        messages.success(
            request,
            format_html(
                'Artwork added to your favourites. <a href="{}">View My Favourites</a>',
                favourites_url,
            ),
        )
    else:
        favourite.delete()
        messages.success(request, "Artwork removed from your favourites.")

    if request.POST.get("from") == "favourites":
        return redirect(
            f"{reverse('artwork_detail', args=[artwork.slug])}?from=favourites"
        )

    page = request.POST.get("page", "1")
    return redirect(f"{reverse('artwork_detail', args=[artwork.slug])}?page={page}")
