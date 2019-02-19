from django.views import generic

from .models import Tournament


class TournamentList(generic.ListView):
    """
    Displays a list of tournaments.
    """

    model = Tournament
    context_object_name = "tournaments"


class TournamentDetail(generic.DetailView):
    """
    Displays detail for a specific tournament, determined by the primary
    key given.
    """

    model = Tournament
    context_object_name = "tournament"
