from django.contrib import admin
from django.urls import include, path

from ftman import views

urlpatterns = [
    # ACME URL for LetsEncrypt
    path(
        ".well-known/acme-challenge/<str:_>",
        views.acme_challenge,
        name="acme-challenge",
    ),
    # Tournament URLs
    path("", include("tournament.urls")),
    # Authentication URLs
    path("users/", include("django.contrib.auth.urls")),
    path("auth/", include("allauth.urls")),
    # Admin URLs
    path("admin/", admin.site.urls),
]
