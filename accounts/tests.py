from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status


class AccountsTest(APITestCase):

    def setUp(self):
        # We want to go ahead and originally create a user.
        self.test_user = User.objects.create_user(
            'testuser', 'test@example.com', 'testpassword')

        # URL for creating an account.
        self.create_url = reverse('account-create')
        self.login_url = reverse('account-login')
        self.refresh_url = reverse('account-refresh')
        self.verify_url = reverse('account-verify')

    def test_create_user(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """
        data = {
            'username': 'foobar',
            'email': 'foobar@example.com',
            'password': 'somepassword'
        }

        response = self.client.post(self.create_url, data, format='json')

        # We want to make sure we have two users in the database..
        self.assertEqual(User.objects.count(), 2)
        # And that we're returning a 201 created code.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Additionally, we want to return the username and email upon
        # successful creation.
        self.assertTrue('token' in response.data)

    def test_api_login(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)

    def test_api_refresh(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response_login = self.client.post(self.login_url, data, format='json')

        response = self.client.post(
            self.refresh_url, response_login.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)

    def test_api_verify(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response_login = self.client.post(self.login_url, data, format='json')

        response = self.client.post(
            self.verify_url, response_login.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
