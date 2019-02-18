from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils import timezone

from .models import Tournament


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
