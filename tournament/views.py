import csv

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from .models import Tournament, Event, Fencer, Result


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


class FencerResults(generic.ListView):
    """
    Shows results for the currently-logged in fencer.
    """

    template_name = "tournament/fencer_results.html"
    context_object_name = "results"

    def get_queryset(self):
        """
        Get the results for the currently-logged in user only.
        Returns:
            Results for the currently-logged in user
        """
        current_fencer = Fencer.objects.get(pk=self.request.user.pk)
        return Result.objects.filter(fencer=current_fencer).order_by("-pk")


class EventResults(generic.ListView):
    """
    Shows results for a given event.
    """

    template_name = "tournament/event_results.html"
    context_object_name = "results"

    def get_queryset(self):
        """
        Get the results for the given event only.
        Returns:
            Results for the given event
        """
        event = Event.objects.get(pk=self.kwargs["event_id"])
        return Result.objects.filter(event=event).order_by(
            "event__name", "place"
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        """Add both the event and its results to available context."""
        context = super(EventResults, self).get_context_data(**kwargs)
        event = Event.objects.get(pk=self.kwargs["event_id"])
        context["event"] = event
        return context


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


@staff_member_required
def export_tournament(request, tournament_id):
    """
    Exports the registrations for each event in a tournament. The CSV exported contains fencers' names, events, and
    ratings.
    Args:
        request: Django request object
        tournament_id: the tournament whose registrations to export

    Returns:

    """
    response = HttpResponse(content_type="text/csv")
    response[
        "Content-Disposition"
    ] = "attachment; filename='tournament_export.csv'"
    writer = csv.writer(response)
    writer.writerow(["First Name", "Last Name", "Event", "Weapon Rating"])

    tournament = Tournament.objects.get(pk=tournament_id)
    events = tournament.event_set.all()
    for event in events:
        for fencer in event.fencers.all():
            if event.weapon == "E":
                rating = fencer.epee_rating
                year = fencer.epee_year
            elif event.weapon == "F":
                rating = fencer.foil_rating
                year = fencer.foil_year
            else:
                rating = fencer.sabre_rating
                year = fencer.sabre_year

            writer.writerow(
                [
                    fencer.first_name,
                    fencer.last_name,
                    event.name,
                    "{}{}".format(rating, year),
                ]
            )

    return response
