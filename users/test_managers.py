from unittest import TestCase

from django.contrib.auth.hashers import make_password

from users.managers import UserManager
from users.models import User


class UserManagerTestCase(TestCase):

    def setUp(self):
        User.objects.all().delete()
        self.user1 = User.objects.create(
            user_name="user1",
            password=make_password("password1"),
            role="Customer"
        )
        self.user2 = User.objects.create(
            user_name="user2",
            password=make_password("password2"),
            role="Admin"
        )

    def test_get_by_user_name(self):
        # Test case where user with specified user_name exists
        user_name = "user1"
        users = User.objects.get_by_user_name(user_name)
        self.assertEqual(users.count(), 1)
        self.assertEqual(users.first().user_name, user_name)

        # Test case where user with specified user_name does not exist
        user_name = "nonexistent_user"
        users = User.objects.get_by_user_name(user_name)
        self.assertEqual(users.count(), 0)

    def test_authenticate(self):
        # Test case where user_name and password match
        user = User.objects.authenticate("user1", "password1")
        self.assertIsNotNone(user)
        self.assertEqual(user.user_name, "user1")

        # Test case where user_name is correct but password is incorrect
        user = User.objects.authenticate("user1", "wrongpassword")
        self.assertIsNone(user)

        # Test case where user_name does not exist
        user = User.objects.authenticate("nonexistent_user", "password")
        self.assertIsNone(user)

        # Test case where user_name and password match for another user
        user = User.objects.authenticate("user2", "password2")
        self.assertIsNotNone(user)
        self.assertEqual(user.user_name, "user2")
