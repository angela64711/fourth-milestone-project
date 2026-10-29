from django.contrib import admin
from django.utils.html import format_html

from .models import Artwork, Collection


class EtsyURLFilter(admin.SimpleListFilter):
    title = "Has Etsy URL?"
    parameter_name = "has_etsy_url"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Yes"),
            ("no", "No"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.exclude(etsy_url="")
        if self.value() == "no":
            return queryset.filter(etsy_url="")
        return queryset


class DescriptionFilter(admin.SimpleListFilter):
    title = "Has Description?"
    parameter_name = "has_description"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Yes"),
            ("no", "No"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.exclude(description="")
        if self.value() == "no":
            return queryset.filter(description="")
        return queryset


@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ("title", "collection", "year")
    list_filter = (
        "collection",
        "year",
        EtsyURLFilter,
        DescriptionFilter,
    )
    search_fields = ("title",)
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.pk and obj.image:
            return format_html(
                '<img src="{}" style="max-height: 250px; width: auto;" '
                'alt="Artwork preview">',
                obj.image.url,
            )
        return "No image available"

    image_preview.short_description = "Current artwork image"


admin.site.register(Collection)
