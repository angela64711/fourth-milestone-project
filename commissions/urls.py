from django.urls import path

from . import views

app_name = "commissions"

urlpatterns = [
    path("", views.commission_creative, name="creative"),
    path(
        "customer-details/",
        views.commission_customer_details,
        name="customer_details",
    ),
]
