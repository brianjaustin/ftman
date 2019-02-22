from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Tournament URL schemes
    path("", include("tournament.urls")),
    # Native Django auth schemes
    path("users/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
]
