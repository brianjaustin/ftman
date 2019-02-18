from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

RATINGS = (('A', 'A'),
           ('B', 'B'),
           ('C', 'C'),
           ('D', 'D',),
           ('E', 'E'),
           ('U', 'U'))

WEAPONS = (('E', 'Epee'), ('F', 'Foil'), ('S', 'Sabre'))


class Fencer(AbstractUser):
    """
    Represents an individual fencer who has ratings for foil, epee, and sabre.

    Fencers have ratings for each weapon, which may be A-E or U. Years are not currently stored for non-U ratings,
    so fencers or administrators will need to update their ratings by hand every 4 years (assuming that ratings are
    not renewed). Note that one must set set this as `AUTH_USER_MODEL` in `settings.py` or face errors from Django.
    """
    foil_rating = models.CharField(max_length=1, choices=RATINGS, default='U')
    foil_year = models.PositiveIntegerField(blank=True, null=True)
    epee_rating = models.CharField(max_length=1, choices=RATINGS, default='U')
    epee_year = models.PositiveIntegerField(blank=True, null=True)
    sabre_rating = models.CharField(max_length=1, choices=RATINGS, default='U')
    sabre_year = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        """
        Default string representation of a user is their username.
        Returns:
            The fencer/user's username
        """
        return self.username


class Tournament(models.Model):
    """
    Represents a tournament, comprised of Events in which Fencers compete.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    registration_open = models.DateTimeField()
    registration_close = models.DateTimeField()
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        """
        Default string representation of a tournament is its name.
        Returns:
            This tournament's name
        """
        return self.name

    def can_register(self, time=timezone.now()):
        """
        Determines if fencers may register at the given time.
        Args:
            time: the time to check, defaults to now

        Returns:
            True if fencers may register at the specified time, False otherwise
        """
        return self.registration_close >= time >= self.registration_open

    class Meta:
        """
        Order tournaments by when they take place.
        """
        ordering = ('-registration_close', '-registration_open')


class Event(models.Model):
    """
    Represents an individual event that is part of a Tournament.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    weapon = models.CharField(max_length=1, choices=WEAPONS, default='E')
    fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    rating_min = models.CharField(max_length=1, choices=RATINGS, default='U', verbose_name="Minimum Rating")
    rating_max = models.CharField(max_length=1, choices=RATINGS, default='A', verbose_name="Maximum Rating")
    fencers_max = models.IntegerField(verbose_name="Maximum Number of Fencers")
    tournament = models.ForeignKey(Tournament, models.CASCADE)
    fencers = models.ManyToManyField(Fencer)

    def __str__(self):
        """
        Default string representation of an event is its name.
        Returns:
            This event's name
        """
        return self.name

    def can_fence(self, fencer):
        """
        Determines if the given fencer can fence in this event.

        A fencer is allowed to fence in an event if their rating for the event's weapon is between the bounds
        specified for the event.
        Args:
            fencer: the fencer to check

        Returns:
            True if the fencer may participate, False otherwise
        """
        if self.weapon == 'E':
            return self.rating_max >= fencer.epee_rating >= self.rating_min
        elif self.weapon == 'F':
            return self.rating_max >= fencer.foil_rating >= self.rating_min
        else:
            return self.rating_max >= fencer.sabre_rating >= self.rating_min


class Result(models.Model):
    """
    Represents a Fencer's results in an event. Currently only place is supported, but other information may
    be tracked in comments.
    """
    fencer = models.ForeignKey(Fencer, models.CASCADE)
    event = models.ForeignKey(Event, models.CASCADE)
    place = models.IntegerField()
    comments = models.TextField()

    def __str__(self):
        """
        Default string representation for results is the fencer's name plus event name.
        Returns:
            This result's fencer and event
        """
        return "{} in {}".format(self.fencer, self.event)
