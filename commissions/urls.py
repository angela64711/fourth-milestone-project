from django.urls import path

from . import views

app_name = "commissions"

urlpatterns = [
    path(
        "",
        views.commission_creative,
        name="creative",
    ),
    path(
        "customer-details/",
        views.commission_customer_details,
        name="customer_details",
    ),
    path(
        "checkout/",
        views.commission_checkout,
        name="checkout",
    ),
    path(
        "verify-payment/<uuid:order_number>/",
        views.commission_verify_payment,
        name="verify_payment",
    ),
    path(
        "success/<uuid:order_number>/",
        views.commission_success,
        name="success",
    ),
]
