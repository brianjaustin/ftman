from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from .models import Tournament, Event, Fencer


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


class FencerProfile(LoginRequiredMixin, generic.UpdateView):
    """
    Allows fencers to update their ratings and years earned.
    """

    model = Fencer
    fields = [
        "epee_rating",
        "epee_year",
        "foil_rating",
        "foil_year",
        "sabre_rating",
        "sabre_year",
    ]
    success_url = reverse_lazy("fencer_profile")

    def get_object(self, queryset=None):
        """
        Get the current user as the object being edited, so we don't have to specify an id.
        Returns:
            The current user
        """
        return self.request.user


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
