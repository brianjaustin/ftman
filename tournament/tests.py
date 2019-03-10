from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from tournament.factories import FencerFactory, TournamentFactory, EventFactory
from .models import Tournament, Event


class FencerModelTests(TestCase):
    def test_create_regular_fencer(self):
        """
        Verify that default values are set correctly and that the correct attributes are required.
        Returns:
            None
        """
        fencer = FencerFactory()
        self.assertTrue(fencer.is_active)
        self.assertFalse(fencer.is_staff)
        self.assertFalse(fencer.is_superuser)
        self.assertEqual(fencer.foil_rating, "U")
        self.assertEqual(fencer.epee_rating, "U")
        self.assertEqual(fencer.sabre_rating, "U")
        user_model = get_user_model()
        with self.assertRaises(TypeError):
            user_model.objects.create_user()
            user_model.objects.create_user(email="")
        with self.assertRaises(ValueError):
            user_model.objects.create_user(email="", username="")

    def test_create_superuser_fencer(self):
        """
        Verify that default values are set correctly and that the correct attributes are required.
        Returns:
            None
        """
        user_model = get_user_model()
        fencer = user_model.objects.create_superuser(
            email="admin@example.com", username="admin", password="admin"
        )
        self.assertEqual(fencer.email, "admin@example.com")
        self.assertEqual(fencer.username, "admin")
        self.assertTrue(fencer.is_active)
        self.assertTrue(fencer.is_staff)
        self.assertTrue(fencer.is_superuser)
        self.assertEqual(fencer.foil_rating, "U")
        self.assertEqual(fencer.epee_rating, "U")
        self.assertEqual(fencer.sabre_rating, "U")
        with self.assertRaises(TypeError):
            user_model.objects.create_superuser()
            user_model.objects.create_superuser(email="")
            user_model.objects.create_superuser(email="", username="")
        with self.assertRaises(ValueError):
            user_model.objects.create_superuser(
                email="", username="", password=""
            )


class TournamentModelTests(TestCase):
    def test_save_tournament(self):
        """
        Check that saving a tournament with missing parameters fails and with all required parameters succeeds.
        Returns:
            None
        """
        tournament = TournamentFactory()
        tournament.save()
        with self.assertRaises(IntegrityError):
            bad_tournament = Tournament()
            bad_tournament.save()
            bad_tournament.name = "Test Tournament"
            bad_tournament.save()
            bad_tournament.registration_close = timezone.now()
            bad_tournament.save()
            bad_tournament.registration_open = timezone.now() - timezone.timedelta(
                days=1
            )

    def test_can_register(self):
        """
        Verify can_register functions as expected.
        Returns:
            None
        """
        tournament = TournamentFactory(
            registration_open=timezone.now() - timezone.timedelta(hours=2),
            registration_close=timezone.now() + timezone.timedelta(hours=1),
        )
        self.assertTrue(tournament.can_register())
        self.assertFalse(
            tournament.can_register(
                timezone.now() - timezone.timedelta(hours=3)
            )
        )
        self.assertFalse(
            tournament.can_register(
                timezone.now() + timezone.timedelta(hours=2)
            )
        )

    def test_ordering(self):
        """
        Test that tournaments are sorted by close first, then open (both ascending).
        Returns:
            None
        """
        yesterday = timezone.now() - timezone.timedelta(days=1)
        now = timezone.now()
        tomorrow = timezone.now() + timezone.timedelta(days=1)
        TournamentFactory(
            name="Tournament 1",
            registration_open=yesterday,
            registration_close=tomorrow,
        ).save()
        TournamentFactory(
            name="Tournament 2",
            registration_open=now,
            registration_close=tomorrow,
        ).save()
        TournamentFactory(
            name="Tournament 3",
            registration_open=yesterday,
            registration_close=now,
        ).save()
        tournaments = Tournament.objects.all()
        self.assertEqual(tournaments[0].name, "Tournament 2")
        self.assertEqual(tournaments[1].name, "Tournament 1")
        self.assertEqual(tournaments[2].name, "Tournament 3")


class EventModelTests(TestCase):
    def test_create_event(self):
        """
        Verify that saving an event with missing parameters fails but succeeds when the required parameters are present.
        Also checks that default values for fields are set properly.
        Returns:
            None
        """
        EventFactory().save()
        event = Event.objects.get(pk=1)
        self.assertEqual(event.weapon, "E")
        self.assertEqual(event.fee, 0)
        self.assertEqual(event.rating_min, "U")
        self.assertEqual(event.rating_max, "A")
        self.assertEqual(event.fencers.all().count(), 0)
        with self.assertRaises(IntegrityError):
            Event().save()
            Event(name="").save()
            Event(name="", fencers_max=1).save()

    def test_string_representation(self):
        """
        Check that events with their weapon in the title don't have redundant string representations.
        Returns:
            None
        """
        EventFactory(name="Epee E and Under", fencers_max=15).save()
        EventFactory(name="Test", weapon="F", rating_min="E").save()
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
        fencer = FencerFactory()
        EventFactory(name="Epee E and Under").save()
        EventFactory(name="Foil Test", weapon="F", rating_min="E").save()
        EventFactory(name="Sabre Test", fencers_max=0, weapon="S").save()
        event1 = Event.objects.get(pk=1)
        event2 = Event.objects.get(pk=2)
        event3 = Event.objects.get(pk=3)
        self.assertTrue(event1.can_fence(fencer))
        self.assertFalse(event2.can_fence(fencer))
        self.assertFalse(event3.can_fence(fencer))


class TournamentListTest(TestCase):
    def test_empty_tournament_list(self):
        """
        Verify that the list of tournaments shows a message when none are found in the database.
        Returns:
            None
        """
        response = self.client.get(reverse("tournament_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No tournaments found.")
        self.assertQuerysetEqual(response.context["tournaments"], [])
        self.assertContains(response, "Login")

    def test_tournament_list_anonymous(self):
        """
        Test that the tournament page shows a tournament when present in the database.
        Returns:
            None
        """
        TournamentFactory(name="Test Tournament").save()
        response = self.client.get(reverse("tournament_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, '<a href="/tournament/1">Test Tournament</a>'
        )
        self.assertQuerysetEqual(
            response.context["tournaments"], ["<Tournament: Test Tournament>"]
        )
        self.assertContains(response, "Login")

    def test_tournament_list_authenticated(self):
        """
        Check that the correct options are available when logged in.
        Returns:
            None
        """
        user_model = get_user_model()
        user_model.objects.create_user(
            username="test", email="test@example.com", password="test"
        )
        self.client.login(username="test", password="test")
        response = self.client.get(reverse("tournament_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Profile")
        self.assertContains(response, "My Results")
        self.assertContains(response, "Logout")


class TournamentDetailTest(TestCase):
    def test_nonexistent_detail(self):
        """
        Test that accessing the detail for a non-existent tournament results in a 404 response code.
        Returns:
            None
        """
        response = self.client.get(
            reverse("tournament_detail", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 404)

    def test_no_events_detail(self):
        """
        Test that tournaments with no events display a no events message.
        Returns:
            None
        """
        TournamentFactory().save()
        response = self.client.get(
            reverse("tournament_detail", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Registration Open:")
        self.assertContains(response, "Registration Close:")
        self.assertContains(response, "Registration Fee:")
        self.assertContains(
            response, "This tournament does not have any events."
        )

    def test_anonymous_detail(self):
        """
        Check that anonymous users can see tournament detail but not a registration link.
        Returns:
            None
        """
        EventFactory(name="Test Event", fencers_max=15).save()
        response = self.client.get(
            reverse("tournament_detail", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Event")
        self.assertContains(response, "0 / 15 fencers")
        self.assertContains(response, "$0.00")
        self.assertContains(response, '<a href="/event/1/results">')
        self.assertNotContains(response, '<a href="/event/1/register">')

    def test_authenticated_detail(self):
        """
        Verify that authenticated users _can_ see a registration link for events.
        Returns:
            None
        """
        EventFactory().save()
        user_model = get_user_model()
        user_model.objects.create_user(
            username="test", email="test@example.com", password="test"
        )
        self.client.login(username="test", password="test")
        response = self.client.get(
            reverse("tournament_detail", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<a href="/event/1/register">')
