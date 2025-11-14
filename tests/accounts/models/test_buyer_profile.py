from django.test import TestCase
from django.core.exceptions import ValidationError
from accounts.models import CustomUser, BuyerProfile
from cars.models import Car


class BuyerProfileModelTest(TestCase):
    """
    Unit tests for the BuyerProfile model.
    """

    def setUp(self):
        # Create a buyer user
        self.buyer_user = CustomUser.objects.create_user(
            username="buyer1",
            email="buyer1@example.com",
            password="password123",
            role="buyer",
            first_name="John",
            last_name="Doe"
        )

        # Create a non-buyer user (dealer)
        self.dealer_user = CustomUser.objects.create_user(
            username="dealer1",
            email="dealer1@example.com",
            password="password123",
            role="dealer"
        )

    def test_buyerprofile_creation(self):
        """
        Test that a BuyerProfile can be created for a user with role 'buyer'.
        """
        profile = BuyerProfile.objects.create(
            user=self.buyer_user,
            phone_number="123456789",
            address="Some Street 123"
        )
        self.assertEqual(profile.user, self.buyer_user)
        self.assertEqual(str(profile), "John Doe")

    def test_buyerprofile_role_validation(self):
        """
        Test that creating a BuyerProfile for a non-buyer user raises ValidationError.
        """
        profile = BuyerProfile(
            user=self.dealer_user,
            phone_number="987654321"
        )
        with self.assertRaises(ValidationError):
            profile.save()

    def test_buyerprofile_wishlist(self):
        """
        Test that wishlist can be assigned and retrieved correctly.
        """
        profile = BuyerProfile.objects.create(
            user=self.buyer_user,
            phone_number="123456789"
        )
        car = Car.objects.create(
            dealer=None,
            brand="Toyota",
            model="Corolla",
            year=2022,
            fuel_type="petrol",
            transmission="automatic",
            engine_volume=1.8,
            price=20000,
            condition="new",
            mileage=0,
            main_image="path/to/image.jpg"
        )
        profile.wishlist.add(car)
        self.assertIn(car, profile.wishlist.all())
