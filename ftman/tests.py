from django.test import TestCase
from django.urls import reverse


class ACMEViewTests(TestCase):
    def test_acme_challenge(self):
        """
        Test that the SSL challenge view exists.
        Returns:
            None
        """
        response = self.client.get(
            reverse("acme-challenge", kwargs={"_": "test"})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "None")
