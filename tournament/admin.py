from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Fencer, Tournament, Event, Result


class FencerAdmin(UserAdmin):
    model = Fencer
    fieldsets = UserAdmin.fieldsets + (
        (
            "Ratings",
            {"fields": ("foil_rating", "epee_rating", "sabre_rating")},
        ),
    )
    list_display = [
        "email",
        "username",
        "foil_rating",
        "epee_rating",
        "sabre_rating",
    ]


admin.site.register(Fencer, FencerAdmin)
admin.site.register(Tournament)
admin.site.register(Event)
admin.site.register(Result)
