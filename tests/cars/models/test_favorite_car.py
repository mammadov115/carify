from django.test import TestCase
from django.db.utils import IntegrityError
from cars.models import Car, CarFeature, FavoriteCar
from accounts.models import DealerProfile, CustomUser


class FavoriteCarModelTest(TestCase):
    """
    Unit tests for the FavoriteCar model.
    """

    def setUp(self):
        # Dealer user and profile
        self.dealer_user = CustomUser.objects.create_user(
            username="dealer1",
            email="dealer1@example.com",
            password="password123",
            role="dealer"
        )
        self.dealer_profile = DealerProfile.objects.create(
            user=self.dealer_user,
            company_name="Super Cars LLC",
            phone_number="555123456"
        )

        # Buyer user
        self.buyer_user = CustomUser.objects.create_user(
            username="buyer1",
            email="buyer1@example.com",
            password="password123",
            role="buyer"
        )

        # CarFeature
        self.abs_feature = CarFeature.objects.create(name="ABS")

        # Car
        self.car = Car.objects.create(
            dealer=self.dealer_profile,
            brand="Toyota",
            model="Corolla",
            year=2022,
            fuel_type="petrol",
            transmission="automatic",
            engine_volume=1.8,
            price=20000,
            condition="new",
            mileage=0,
            main_image="path/to/main_image.jpg"
        )
        self.car.features.add(self.abs_feature)

    def test_favoritecar_creation(self):
        """
        Test that a FavoriteCar can be created and linked to a user and car.
        """
        favorite = FavoriteCar.objects.create(user=self.buyer_user, car=self.car)
        self.assertEqual(favorite.user, self.buyer_user)
        self.assertEqual(favorite.car, self.car)
        self.assertEqual(str(favorite), f"{self.buyer_user} → {self.car}")
        self.assertIsNotNone(favorite.added_at)

    def test_unique_constraint(self):
        """
        Test that a user cannot favorite the same car twice.
        """
        FavoriteCar.objects.create(user=self.buyer_user, car=self.car)
        with self.assertRaises(IntegrityError):
            FavoriteCar.objects.create(user=self.buyer_user, car=self.car)
