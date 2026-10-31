from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import F
from django.shortcuts import get_object_or_404, render

from artworks.models import Artwork, Collection


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
    Display artworks with search, filters and pagination.
    """
    artworks = Artwork.objects.select_related("collection")

    # Read filter values from the URL
    query = request.GET.get("q", "").strip()
    collection = request.GET.get("collection", "")
    year = request.GET.get("year", "")
    etsy = request.GET.get("etsy", "")
    description = request.GET.get("description", "")
    sort = request.GET.get("sort", "title")

    # Search by artwork title
    if query:
        artworks = artworks.filter(title__icontains=query)

    # Filter by collection
    if collection.isdigit():
        artworks = artworks.filter(collection_id=int(collection))

    # Filter by year availability
    if year == "present":
        artworks = artworks.filter(year__isnull=False)
    elif year == "missing":
        artworks = artworks.filter(year__isnull=True)

    # Filter by Etsy URL availability
    if etsy == "present":
        artworks = artworks.exclude(etsy_url="")
    elif etsy == "missing":
        artworks = artworks.filter(etsy_url="")

    # Filter by description availability
    if description == "present":
        artworks = artworks.exclude(description="")
    elif description == "missing":
        artworks = artworks.filter(description="")

    # Sort artworks
    if sort == "year":
        artworks = artworks.order_by(F("year").desc(nulls_last=True), "title", "pk")
    elif sort == "recent":
        artworks = artworks.order_by("-created_on", "pk")
    else:
        artworks = artworks.order_by("title", "pk")

    # Paginate the filtered queryset
    paginator = Paginator(artworks, 36)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Preserve filters when navigating between pages
    query_params = request.GET.copy()
    query_params.pop("page", None)

    context = {
        "artworks": page_obj,
        "page_obj": page_obj,
        "collections": Collection.objects.order_by("display_order", "name"),
        "selected_collection": collection,
        "selected_year": year,
        "selected_etsy": etsy,
        "selected_description": description,
        "query_string": query_params.urlencode(),
    }

    return render(request, "dashboard/artwork_list.html", context)


@artist_required
def artwork_overview(request, slug):
    """
    Display an individual artwork and its details in the artist dashboard.
    """
    artwork = get_object_or_404(Artwork, slug=slug)

    context = {
        "artwork": artwork,
    }

    return render(request, "dashboard/artwork_overview.html", context)
