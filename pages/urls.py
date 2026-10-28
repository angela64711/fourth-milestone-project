from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("about/", views.about, name="about"),
    path("where-to-buy/", views.retail, name="retail"),
    path("collaborations/", views.collaborations, name="collaborations"),
]
