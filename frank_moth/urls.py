from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("pages.urls")),
    path("art/", include("artworks.urls")),
    path("commissions/", include("commissions.urls")),
    path("profile/", include("profiles.urls")),
]
