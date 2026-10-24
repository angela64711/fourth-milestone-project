from django.urls import path

from . import views

app_name = "commissions"

urlpatterns = [
    path("", views.commission_creative, name="creative"),
]
