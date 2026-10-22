from django.urls import path
from . import views

urlpatterns = [
    path("", views.collection_list, name="art"),
    path("<slug:slug>/", views.collection_detail, name="collection_detail"),
]
