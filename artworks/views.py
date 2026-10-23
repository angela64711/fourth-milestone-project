from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, render

from .models import Artwork, Collection


def collections(request):
    """
    Display collections containing artworks, with automatic covers.
    """
    collections = (
        Collection.objects.filter(artworks__isnull=False)
        .distinct()
        .prefetch_related(
            Prefetch(
                "artworks",
                queryset=Artwork.objects.order_by("title"),
                to_attr="ordered_artworks",
            )
        )
    )

    return render(request, "artworks/collections.html", {"collections": collections})


def artworks(request, slug):
    """
    Display a collection and its paginated artworks.
    """
    collection = get_object_or_404(Collection, slug=slug)

    artworks = Artwork.objects.filter(collection=collection).order_by("-year", "title")

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
    Display an individual artwork and its details.
    """
    artwork = get_object_or_404(Artwork, slug=slug)

    context = {
        "artwork": artwork,
        "gallery_page": request.GET.get("page", "1"),
    }

    return render(request, "artworks/artwork_detail.html", context)
