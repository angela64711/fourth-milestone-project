from django.db.models import Prefetch
from django.shortcuts import render

from .models import Artwork, Collection


def collection_list(request):
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
