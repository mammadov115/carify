from django.test import TestCase
from accounts.models import CustomUser


class CustomUserModelTest(TestCase):
    """
    Unit tests for the CustomUser model.
    """

    def test_user_roles_methods(self):
        """
        Test is_buyer() and is_dealer() methods.
        """
        buyer = CustomUser.objects.create_user(
            username="buyer1",
            email="buyer1@example.com",
            password="testpassword",
            role="buyer"
        )
        dealer = CustomUser.objects.create_user(
            username="dealer1",
            email="dealer1@example.com",
            password="testpassword",
            role="dealer"
        )

        self.assertTrue(buyer.is_buyer())
        self.assertFalse(buyer.is_dealer())

        self.assertTrue(dealer.is_dealer())
        self.assertFalse(dealer.is_buyer())

    def test_user_default_role(self):
        """
        Test that a new user defaults to 'buyer' role if not specified.
        """
        user = CustomUser.objects.create_user(
            username="defaultuser",
            email="default@example.com",
            password="password123"
        )
        self.assertEqual(user.role, "buyer")
        self.assertTrue(user.is_buyer())
        self.assertFalse(user.is_dealer())
