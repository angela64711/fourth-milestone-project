from django.contrib import admin

from .models import CommissionOrder


@admin.register(CommissionOrder)
class CommissionOrderAdmin(admin.ModelAdmin):
    """
    Configure how commission orders appear in Django admin.
    """

    list_display = (
        "order_number",
        "full_name",
        "artwork_format",
        "total_price",
        "payment_status",
        "created_on",
    )

    list_filter = (
        "payment_status",
        "artwork_format",
        "created_on",
    )

    search_fields = (
        "order_number",
        "full_name",
        "email",
    )

    readonly_fields = (
        "order_number",
        "created_on",
        "updated_on",
        "stripe_payment_intent",
    )
