from functools import wraps

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import Http404
from django.db import transaction
from django.db.models import F, Count
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import IncomingMessage
from artworks.models import Artwork, Collection
from commissions.models import CommissionOrder

from .forms import ArtworkForm, CollectionForm


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
    sort = request.GET.get("sort", "recent")

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


@artist_required
def artwork_add(request):
    """
    Allow authorized artists to add a new artwork.
    """
    if request.method == "POST":
        form = ArtworkForm(request.POST, request.FILES)

        if form.is_valid():
            artwork = form.save()

            messages.success(request, f'"{artwork.title}" was added successfully.')

            return redirect("dashboard:artwork_overview", slug=artwork.slug)
    else:
        form = ArtworkForm()

    context = {
        "form": form,
    }

    return render(request, "dashboard/artwork_form.html", context)


@artist_required
def artwork_edit(request, slug):
    """
    Allow authorized artists to edit an existing artwork.
    """
    artwork = get_object_or_404(Artwork, slug=slug)

    if request.method == "POST":
        form = ArtworkForm(
            request.POST,
            request.FILES,
            instance=artwork,
        )

        if form.is_valid():
            artwork = form.save()

            messages.success(
                request,
                f'"{artwork.title}" was updated successfully.',
            )

            return redirect(
                "dashboard:artwork_overview",
                slug=artwork.slug,
            )
    else:
        form = ArtworkForm(instance=artwork)

    context = {
        "form": form,
        "artwork": artwork,
        "page_title": "Edit Artwork",
        "submit_label": "Save Changes",
    }

    return render(request, "dashboard/artwork_form.html", context)


@artist_required
def artwork_delete(request, slug):
    """
    Allow authorized artists to delete an existing artwork.
    """
    artwork = get_object_or_404(Artwork, slug=slug)

    if request.method == "POST":
        artwork_title = artwork.title
        artwork.delete()

        messages.success(
            request,
            f'"{artwork_title}" was deleted successfully.',
        )
        return redirect("dashboard:home")

    context = {
        "artwork": artwork,
        "page_title": "Delete Artwork",
        "submit_label": "Delete Artwork",
    }

    return render(request, "dashboard/artwork_delete.html", context)


@artist_required
def collection_list(request):
    """
    Display all collections with their covers and artwork counts.
    """
    collections = Collection.objects.annotate(artwork_count=Count("artworks")).order_by(
        "display_order", "id"
    )

    context = {
        "collections": collections,
    }

    return render(request, "dashboard/collection_list.html", context)


@artist_required
@require_POST
def collection_move(request, pk, direction):
    """
    Move a collection one position up or down in display order.
    """
    if direction not in ("up", "down"):
        return redirect("dashboard:collection_list")

    with transaction.atomic():
        collections = list(
            Collection.objects.select_for_update().order_by("display_order", "id")
        )

        current_index = next(
            (
                index
                for index, collection in enumerate(collections)
                if collection.pk == pk
            ),
            None,
        )

        if current_index is None:
            raise Http404("Collection not found.")

        neighbour_index = current_index - 1 if direction == "up" else current_index + 1

        if 0 <= neighbour_index < len(collections):
            current = collections[current_index]
            neighbour = collections[neighbour_index]

            current.display_order, neighbour.display_order = (
                neighbour.display_order,
                current.display_order,
            )

            current.save(update_fields=["display_order"])
            neighbour.save(update_fields=["display_order"])

    return redirect("dashboard:collection_list")


@artist_required
def collection_add(request):
    """
    Allow artists to create a new artwork collection.
    """
    if request.method == "POST":
        form = CollectionForm(request.POST)

        if form.is_valid():
            collection = form.save()

            messages.success(
                request,
                f'"{collection.name}" was added successfully.',
            )

            return redirect(
                "dashboard:collection_list",
            )
    else:
        form = CollectionForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "dashboard/collection_form.html",
        context,
    )


@artist_required
def collection_overview(request, slug):
    """
    Display an individual collection and its details
    in the artist dashboard.
    """
    collection = get_object_or_404(Collection, slug=slug)

    context = {
        "collection": collection,
    }

    return render(request, "dashboard/collection_overview.html", context)


@artist_required
def collection_edit(request, slug):
    """
    Allow authorized artists to edit collection details
    and select an artwork from the collection as its cover.
    """
    collection = get_object_or_404(Collection, slug=slug)
    artworks = collection.artworks.order_by("title")

    if request.method == "POST":
        form = CollectionForm(request.POST, instance=collection)
        cover_id = request.POST.get("cover_artwork", "")

        if form.is_valid():

            # Validate the submitted cover ID before querying the database.
            # Reject non-numeric IDs, nonexistent artworks, and artworks from
            # other collections to prevent errors or invalid cover assignments.
            if cover_id:
                selected_cover = (
                    artworks.filter(pk=int(cover_id)).first()
                    if cover_id.isdecimal()
                    else None
                )

                if selected_cover is None:
                    form.add_error(
                        None,
                        "Please select a valid artwork from this collection.",
                    )
                else:
                    collection.cover_artwork = selected_cover
            else:
                collection.cover_artwork = None

            if not form.errors:
                collection = form.save(commit=False)
                collection.save()

                messages.success(
                    request,
                    f'"{collection.name}" was updated successfully.',
                )

                return redirect(
                    "dashboard:collection_overview",
                    slug=collection.slug,
                )
    else:
        form = CollectionForm(instance=collection)

    context = {
        "form": form,
        "collection": collection,
        "artworks": artworks,
        "page_title": "Edit Collection",
        "submit_label": "Save Changes",
    }

    return render(
        request,
        "dashboard/collection_form.html",
        context,
    )


@artist_required
def collection_delete(request, slug):
    """
    Allow authorized artists to delete empty collections.
    Prevent deletion of collections containing artworks.
    """
    collection = get_object_or_404(Collection, slug=slug)

    if request.method == "POST":
        if collection.artworks.exists():
            messages.error(
                request,
                "This collection cannot be deleted because it contains "
                "artworks. Reassign its artworks before deleting it.",
            )
            return redirect(
                "dashboard:collection_overview",
                slug=collection.slug,
            )

        collection_name = collection.name
        collection.delete()

        messages.success(
            request,
            f'"{collection_name}" was deleted successfully.',
        )
        return redirect("dashboard:collection_list")

    context = {
        "collection": collection,
        "page_title": "Delete Collection",
        "submit_label": "Delete Collection",
    }

    return render(
        request,
        "dashboard/collection_delete.html",
        context,
    )


@artist_required
def commission_list(request):
    """
    Display paid commission orders in the artist dashboard.
    Show outstanding orders by default.
    """
    status = request.GET.get("status", "todo")

    if status not in ("todo", "completed", "all"):
        status = "todo"

    orders = CommissionOrder.objects.filter(
        payment_status="paid",
    ).order_by("-created_on")

    if status == "todo":
        orders = orders.filter(is_completed=False)
    elif status == "completed":
        orders = orders.filter(is_completed=True)

    context = {
        "orders": orders,
        "selected_status": status,
    }

    return render(
        request,
        "dashboard/commission_list.html",
        context,
    )


@artist_required
@require_POST
def commission_mark_completed(request, pk):
    """
    Allow authorized artists to mark a paid commission
    as completed.
    """
    order = get_object_or_404(
        CommissionOrder,
        pk=pk,
        payment_status="paid",
    )

    if not order.is_completed:
        order.is_completed = True
        order.save(update_fields=["is_completed", "updated_on"])

        messages.success(
            request,
            "Commission marked as completed.",
        )

    return redirect("dashboard:commission_list")


@artist_required
def message_list(request):
    """
    Display incoming contact messages in the artist dashboard.
    """
    incoming_messages = IncomingMessage.objects.all()

    context = {
        "incoming_messages": incoming_messages,
    }

    return render(
        request,
        "dashboard/message_list.html",
        context,
    )
