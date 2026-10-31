from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.artwork_list, name="home"),
    path("artwork/<slug:slug>/", views.artwork_overview, name="artwork_overview"),
]
