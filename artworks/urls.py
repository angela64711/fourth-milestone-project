from django.urls import path
from . import views

urlpatterns = [
    path("", views.collections, name="art"),
    path(
        "<slug:slug>/",
        views.artworks,
        name="artworks",
    ),
    path(
        "artwork/<slug:slug>/",
        views.artwork_detail,
        name="artwork_detail",
    ),
    path(
        "artwork/<slug:slug>/favourite/",
        views.toggle_favourite,
        name="toggle_favourite",
    ),
]
