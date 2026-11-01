from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.artwork_list, name="home"),
    path(
        "artwork/add/",
        views.artwork_add,
        name="artwork_add",
    ),
    path(
        "artwork/<slug:slug>/edit/",
        views.artwork_edit,
        name="artwork_edit",
    ),
    path(
        "artwork/<slug:slug>/delete/",
        views.artwork_delete,
        name="artwork_delete",
    ),
    path(
        "artwork/<slug:slug>/",
        views.artwork_overview,
        name="artwork_overview",
    ),
    path(
        "collections/",
        views.collection_list,
        name="collection_list",
    ),
    path(
        "collections/<int:pk>/move/<str:direction>/",
        views.collection_move,
        name="collection_move",
    ),
    path(
        "collections/add/",
        views.collection_add,
        name="collection_add",
    ),
]
