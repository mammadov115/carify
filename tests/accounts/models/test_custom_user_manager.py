from django.test import TestCase
from accounts.models import CustomUser


class CustomUserManagerTest(TestCase):
    """
    Unit tests for CustomUserManager.
    """

    def test_create_user_with_valid_data(self):
        """
        Test creating a regular user with role 'buyer'.
        """
        user = CustomUser.objects.create_user(
            username="buyer1",
            email="buyer1@example.com",
            password="testpassword"
        )
        self.assertEqual(user.username, "buyer1")
        self.assertEqual(user.email, "buyer1@example.com")
        self.assertTrue(user.check_password("testpassword"))
        self.assertEqual(user.role, "buyer")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_user_without_email_or_username(self):
        """
        Test that creating a user without email or username raises ValueError.
        """
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(username="", email="test@example.com")
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(username="user1", email="")

    def test_create_superuser_defaults_to_dealer(self):
        """
        Test creating a superuser sets correct role and permissions.
        """
        superuser = CustomUser.objects.create_superuser(
            username="dealer1",
            email="dealer1@example.com",
            password="superpassword"
        )
        self.assertEqual(superuser.username, "dealer1")
        self.assertEqual(superuser.email, "dealer1@example.com")
        self.assertTrue(superuser.check_password("superpassword"))
        self.assertEqual(superuser.role, "dealer")
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)
