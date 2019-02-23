from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Fencer, Tournament, Event, Result


class FencerAdmin(UserAdmin):
    """
    Admin setup for custom user model, so custom fields show up.
    """

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


class ResultInline(admin.TabularInline):
    """
    Inline editing for results in the event admin page.
    """

    model = Result


class EventAdmin(admin.ModelAdmin):
    """
    Sets the results inline for the Event model.
    """

    model = Result
    inlines = [ResultInline]


admin.site.register(Fencer, FencerAdmin)
admin.site.register(Tournament)
admin.site.register(Event, EventAdmin)
