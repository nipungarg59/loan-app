from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from users.constants import MESSAGE_USER_CREATED_SUCCESSFULLY, JWT_COOKIE_KEY, MESSAGE_LOGIN_SUCCESSFUL, \
    MESSAGE_INVALID_CREDENTIALS
from users.models import User
from django.contrib.auth.hashers import make_password


class RegisterUserAPIViewTestCase(TestCase):

    def setUp(self):
        # Clear existing data
        User.objects.all().delete()

        self.client = APIClient()

    def test_register_user_success(self):
        url = reverse('register-user')
        data = {
            'user_name': 'user',
            'password': 'password',
            'role': 'Customer'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], MESSAGE_USER_CREATED_SUCCESSFULLY)
        self.assertEqual(User.objects.filter(user_name='user').count(), 1)

    def test_register_user_invalid_data(self):
        url = reverse('register-user')
        data = {
            'user_name': '',
            'password': 'password',
            'role': 'Customer'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class FetchUserDetailsAPIViewTestCase(TestCase):

    def setUp(self):
        # Clear existing data
        User.objects.all().delete()

        self.client = APIClient()
        self.user = User.objects.create(
            user_name='user',
            password=make_password('password'),
            role='Customer'
        )
        setattr(self.user, "is_authenticated", True)
        self.client.force_authenticate(user=self.user)

    def test_fetch_user_details_success(self):
        url = reverse('my-profile')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['user_name'], 'user')

    def test_fetch_user_details_unauthenticated(self):
        self.client.force_authenticate(user=None)
        url = reverse('my-profile')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LoginAPIViewTestCase(TestCase):

    def setUp(self):
        # Clear existing data
        User.objects.all().delete()

        self.client = APIClient()
        self.user = User.objects.create(
            user_name='user',
            password=make_password('password'),
            role='Customer'
        )

    def test_login_success(self):
        url = reverse('login')
        data = {
            'user_name': 'user',
            'password': 'password'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], MESSAGE_LOGIN_SUCCESSFUL)
        self.assertTrue(JWT_COOKIE_KEY in response.cookies)

    def test_login_invalid_credentials(self):
        url = reverse('login')
        data = {
            'user_name': 'user',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['message'], MESSAGE_INVALID_CREDENTIALS)
