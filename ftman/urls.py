from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Tournament URLs
    path("", include("tournament.urls")),
    # Authentication URLs
    path("users/", include("django.contrib.auth.urls")),
    path("auth/", include("allauth.urls")),
    # Admin URLs
    path("admin/", admin.site.urls),
]
