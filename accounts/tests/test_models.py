from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser

class UserTests(TestCase):

    def setUp(self):
        CustomUser.objects.create_user(
            username = "Testutis",
            email="testutis@tarkute.lt",
            password='Tarkavimas10',
            is_public=True,
        )

    def test_user_name(self):
        user = CustomUser.objects.get(id=1)
        username = user.username
        email = user.email
        self.assertEqual(username, "Testutis")
        self.assertEqual(email, "testutis@tarkute.lt")