from django.urls import path

from . import views

urlpatterns = [
    path("", views.TournamentList.as_view(), name="tournament_list"),
    # Fencer-related URLs
    path(
        "fencer/profile/", views.FencerProfile.as_view(), name="fencer_profile"
    ),
    path(
        "fencer/results/", views.FencerResults.as_view(), name="fencer_results"
    ),
    # Tournament-related urls
    path(
        "tournament/", views.TournamentList.as_view(), name="tournament_list"
    ),
    path(
        "tournament/<int:pk>",
        views.TournamentDetail.as_view(),
        name="tournament_detail",
    ),
    path(
        "tournament/<int:tournament_id>/export",
        views.export_tournament,
        name="tournament_export",
    ),
    # Event-related urls
    path(
        "event/<int:event_id>/register",
        views.register_fencer,
        name="event_register",
    ),
    path(
        "event/<int:event_id>/results",
        views.EventResults.as_view(),
        name="event_results",
    ),
]
