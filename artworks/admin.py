from django.contrib import admin
from django.utils.html import format_html

from .models import Artwork, Collection


@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
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
