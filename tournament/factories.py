import random

import factory
from django.utils import timezone

from .models import Event
from .models import Fencer
from .models import Result
from .models import Tournament


class FencerFactory(factory.DjangoModelFactory):
    """
    Factory used for tests involving the Fencer model.
    """

    class Meta:
        model = Fencer

    email = factory.Faker("email")
    password = factory.Faker("password")


class TournamentFactory(factory.DjangoModelFactory):
    """
    Factory used for tests involving the Tournament model.
    """

    class Meta:
        model = Tournament

    name = factory.Faker("text")
    registration_open = timezone.now() - timezone.timedelta(
        days=random.randint(0, 100)
    )
    registration_close = timezone.now() + timezone.timedelta(
        days=random.randint(0, 100)
    )
    registration_fee = random.randint(0, 100)


class EventFactory(factory.DjangoModelFactory):
    """
    Factory used for tests involving the Event model.
    """

    class Meta:
        model = Event

    name = factory.Faker("text")
    fencers_max = random.randint(1, 100)
    tournament = factory.SubFactory(TournamentFactory)


class ResultFactory(factory.DjangoModelFactory):
    """
    Factory used for tests involving the Result model.
    """

    class Meta:
        model = Result

    fencer = factory.SubFactory(FencerFactory)
    event = factory.SubFactory(EventFactory)
    place = 1
    comments = ""
