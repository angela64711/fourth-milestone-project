from django.urls import path
from . import views

urlpatterns = [
    path("", views.collections, name="art"),
    path("<slug:slug>/", views.artworks, name="artworks"),
]
