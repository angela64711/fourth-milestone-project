from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.artwork_list, name="home"),
    path("artwork/add/", views.artwork_add, name="artwork_add"),
    path("artwork/<slug:slug>/edit/", views.artwork_edit, name="artwork_edit"),
    path("artwork/<slug:slug>/delete/", views.artwork_delete, name="artwork_delete"),
    path("artwork/<slug:slug>/", views.artwork_overview, name="artwork_overview"),
]
