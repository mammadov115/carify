from django.test import TestCase
from django.core.exceptions import ValidationError
from accounts.models import CustomUser, DealerProfile


class DealerProfileModelTest(TestCase):
    """
    Unit tests for the DealerProfile model.
    """

    def setUp(self):
        # Create a dealer user
        self.dealer_user = CustomUser.objects.create_user(
            username="dealer1",
            email="dealer1@example.com",
            password="password123",
            role="dealer",
            first_name="Alice",
            last_name="Smith"
        )

        # Create a non-dealer user (buyer)
        self.buyer_user = CustomUser.objects.create_user(
            username="buyer1",
            email="buyer1@example.com",
            password="password123",
            role="buyer"
        )

    def test_dealerprofile_creation(self):
        """
        Test that a DealerProfile can be created for a user with role 'dealer'.
        """
        profile = DealerProfile.objects.create(
            user=self.dealer_user,
            company_name="Super Cars LLC",
            tax_number="123456789",
            phone_number="555123456",
            email="info@supercars.com",
            address="123 Main Street"
        )
        self.assertEqual(profile.user, self.dealer_user)
        self.assertEqual(str(profile), "Super Cars LLC")

    def test_dealerprofile_role_validation(self):
        """
        Test that creating a DealerProfile for a non-dealer user raises ValidationError.
        """
        profile = DealerProfile(
            user=self.buyer_user,
            company_name="Fake Company"
        )
        with self.assertRaises(ValidationError):
            profile.save()
