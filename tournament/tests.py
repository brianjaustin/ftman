from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils import timezone

from .models import Tournament, Event


class FencerModelTests(TestCase):

    def test_create_regular_fencer(self):
        """
        Verify that default values are set correctly and that the correct attributes are required.
        Returns:
            None
        """
        user_model = get_user_model()
        fencer = user_model.objects.create_user(email='test@example.com', username='test', password='change-me')
        self.assertEqual(fencer.email, 'test@example.com')
        self.assertEqual(fencer.username, 'test')
        self.assertTrue(fencer.is_active)
        self.assertFalse(fencer.is_staff)
        self.assertFalse(fencer.is_superuser)
        self.assertEqual(fencer.foil_rating, 'U')
        self.assertEqual(fencer.epee_rating, 'U')
        self.assertEqual(fencer.sabre_rating, 'U')
        with self.assertRaises(TypeError):
            user_model.objects.create_user()
            user_model.objects.create_user(email='')
        with self.assertRaises(ValueError):
            user_model.objects.create_user(email='', username='')

    def test_create_superuser_fencer(self):
        """
        Verify that default values are set correctly and that the correct attributes are required.
        Returns:
            None
        """
        user_model = get_user_model()
        fencer = user_model.objects.create_superuser(email='admin@example.com', username='admin', password='admin')
        self.assertEqual(fencer.email, 'admin@example.com')
        self.assertEqual(fencer.username, 'admin')
        self.assertTrue(fencer.is_active)
        self.assertTrue(fencer.is_staff)
        self.assertTrue(fencer.is_superuser)
        self.assertEqual(fencer.foil_rating, 'U')
        self.assertEqual(fencer.epee_rating, 'U')
        self.assertEqual(fencer.sabre_rating, 'U')
        with self.assertRaises(TypeError):
            user_model.objects.create_superuser()
            user_model.objects.create_superuser(email='')
            user_model.objects.create_superuser(email='', username='')
        with self.assertRaises(ValueError):
            user_model.objects.create_superuser(email='', username='', password='')


class TournamentModelTests(TestCase):

    def test_save_tournament(self):
        """
        Check that saving a tournament with missing parameters fails and with all required parameters succeeds.
        Returns:
            None
        """
        tournament = Tournament()
        tournament.name = 'Test Tournament'
        tournament.registration_open = timezone.now() - timezone.timedelta(days=1)
        tournament.registration_close = timezone.now()
        tournament.registration_fee = 0
        tournament.save()
        with self.assertRaises(IntegrityError):
            bad_tournament = Tournament()
            bad_tournament.save()
            bad_tournament.name = 'Test Tournament'
            bad_tournament.save()
            bad_tournament.registration_close = timezone.now()
            bad_tournament.save()
            bad_tournament.registration_open = timezone.now() - timezone.timedelta(days=1)

    def test_can_register(self):
        """
        Verify can_register functions as expected.
        Returns:
            None
        """
        tournament = Tournament(name='Test Tournament')
        tournament.registration_open = timezone.now() - timezone.timedelta(hours=2)
        tournament.registration_close = timezone.now() + timezone.timedelta(hours=1)
        self.assertTrue(tournament.can_register())
        self.assertFalse(tournament.can_register(timezone.now() - timezone.timedelta(hours=3)))
        self.assertFalse(tournament.can_register(timezone.now() + timezone.timedelta(hours=2)))

    def test_ordering(self):
        """
        Test that tournaments are sorted by close first, then open (both ascending).
        Returns:
            None
        """
        yesterday = timezone.now() - timezone.timedelta(days=1)
        now = timezone.now()
        tomorrow = timezone.now() + timezone.timedelta(days=1)
        Tournament(name='Tournament 1', registration_open=yesterday, registration_close=tomorrow,
                   registration_fee=0).save()
        Tournament(name='Tournament 2', registration_open=now, registration_close=tomorrow, registration_fee=0).save()
        Tournament(name='Tournament 3', registration_open=yesterday, registration_close=now, registration_fee=0).save()
        tournaments = Tournament.objects.all()
        self.assertEqual(tournaments[0].name, 'Tournament 2')
        self.assertEqual(tournaments[1].name, 'Tournament 1')
        self.assertEqual(tournaments[2].name, 'Tournament 3')


class EventModelTests(TestCase):

    def test_create_event(self):
        """
        Verify that saving an event with missing parameters fails but succeeds when the required parameters are present.
        Also checks that default values for fields are set properly.
        Returns:
            None
        """
        yesterday = timezone.now() - timezone.timedelta(days=1)
        tomorrow = timezone.now() + timezone.timedelta(days=1)
        Tournament(name='Tournament 1', registration_open=yesterday, registration_close=tomorrow, registration_fee=0).save()
        event = Event()
        event.name = 'Test Event'
        event.fencers_max = 15
        event.tournament = Tournament.objects.get(pk=1)
        event.save()
        event = Event.objects.get(pk=1)
        self.assertEqual(event.name, 'Test Event')
        self.assertEqual(event.weapon, 'E')
        self.assertEqual(event.fee, 0)
        self.assertEqual(event.rating_min, 'U')
        self.assertEqual(event.rating_max, 'A')
        self.assertEqual(event.fencers_max, 15)
        self.assertEqual(event.tournament.name, 'Tournament 1')
        self.assertEqual(event.fencers.all().count(), 0)
        with self.assertRaises(IntegrityError):
            Event().save()
            Event(name='').save()
            Event(name='', fencers_max=1).save()

    def test_string_representation(self):
        """
        Check that events with their weapon in the title don't have redundant string representations.
        Returns:
            None
        """
        yesterday = timezone.now() - timezone.timedelta(days=1)
        tomorrow = timezone.now() + timezone.timedelta(days=1)
        Tournament(name='Tournament 1', registration_open=yesterday, registration_close=tomorrow, registration_fee=0).save()
        tournament = Tournament.objects.get(pk=1)
        Event(name='Epee E and Under', fencers_max=15, tournament=tournament).save()
        Event(name='Test', fencers_max=15, tournament=tournament, weapon='F', rating_min='E').save()
        event1 = Event.objects.get(pk=1)
        event2 = Event.objects.get(pk=2)
        self.assertEqual(str(event1), event1.name)
        self.assertEqual(str(event2), "{} [Foil]".format(event2.name))

    def test_can_fence(self):
        """
        Test that a fencer can_fence if the event is not full and does not have a rating restriction that prevents it.
        Returns:
            None
        """
        yesterday = timezone.now() - timezone.timedelta(days=1)
        tomorrow = timezone.now() + timezone.timedelta(days=1)
        fencer = get_user_model().objects.create_user(email='test@example.com', username='test', password='change-me')
        Tournament(name='Tournament 1', registration_open=yesterday, registration_close=tomorrow, registration_fee=0).save()
        tournament = Tournament.objects.get(pk=1)
        Event(name='Epee E and Under', fencers_max=15, tournament=tournament).save()
        Event(name='Foil Test', fencers_max=15, tournament=tournament, weapon='F', rating_min='E').save()
        Event(name='Sabre Test', fencers_max=-1, tournament=tournament, weapon='S').save()
        event1 = Event.objects.get(pk=1)
        event2 = Event.objects.get(pk=2)
        event3 = Event.objects.get(pk=3)
        self.assertTrue(event1.can_fence(fencer))
        self.assertFalse(event2.can_fence(fencer))
        self.assertFalse(event3.can_fence(fencer))
