from django.test import TestCase
from django.urls import reverse, resolve
from accounts.views import home, viewUser, editUser, loggedIn

class UrlTests(TestCase):

    def test_home_url_resolves(self):
        url = reverse('accounts:home')
        self.assertEqual(resolve(url).func, home)

    def test_viewUser_url_resolves(self):
        url = reverse('accounts:viewUser', args=[8])
        self.assertEqual(resolve(url).func, viewUser)

    def test_editUser_url_resolves(self):
        url = reverse('accounts:editUser', args=[7])
        self.assertEqual(resolve(url).func, editUser)