from django.contrib.auth import get_user_model
from django.test import TestCase


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
            None.
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
