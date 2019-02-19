from django.urls import path

from . import views

urlpatterns = [
    path("", views.TournamentList.as_view(), name="tournament_list"),
    # Tournament model urls
    path(
        "tournament/", views.TournamentList.as_view(), name="tournament_list"
    ),
    path(
        "tournament/<int:pk>",
        views.TournamentDetail.as_view(),
        name="tournament_detail",
    ),
]
