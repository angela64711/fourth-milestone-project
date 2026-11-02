from django.contrib import admin

from .models import IncomingMessage


@admin.register(IncomingMessage)
class IncomingMessageAdmin(admin.ModelAdmin):
    list_display = ("created_on", "name", "email", "subject")
    ordering = ("-created_on",)
    readonly_fields = (
        "name",
        "email",
        "subject",
        "message",
        "created_on",
    )

    def has_add_permission(self, request):
        return False
