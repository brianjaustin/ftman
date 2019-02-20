from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.views import generic

from .models import Tournament, Event


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


@login_required
def register_fencer(request, event_id):
    """
    Register the current fencer (user) for the given tournament.
    Args:
        request: Django request object, used to retrieve the current user
        event_id: the event to register the current user for
    Returns:
        redirect to tournament_detail
    """
    event = get_object_or_404(Event, pk=event_id)
    fencer = request.user
    if event.can_fence(fencer):
        event.fencers.add(fencer)
        messages.success(
            request, "Registered successfully for {}".format(event)
        )
    else:
        messages.error(request, "Failed to register for {}".format(event))
    return redirect("tournament_detail", pk=event.tournament.pk)
