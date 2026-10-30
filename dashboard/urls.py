from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.artwork_list, name="home"),
]
