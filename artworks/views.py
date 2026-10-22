from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, render

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


def collection_detail(request, slug):
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
