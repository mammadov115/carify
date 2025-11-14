from django.test import TestCase
from cars.models import Car, CarFeature
from accounts.models import DealerProfile, CustomUser


class CarModelTest(TestCase):
    """
    Unit tests for the Car model.
    """

    def setUp(self):
        # Create a dealer user and profile
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

        # Create a CarFeature
        self.abs_feature = CarFeature.objects.create(name="ABS")

    def test_car_creation_and_slug(self):
        """
        Test that a Car can be created and slug is auto-generated.
        """
        car = Car.objects.create(
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
            main_image="path/to/image.jpg"
        )
        car.features.add(self.abs_feature)

        self.assertEqual(car.dealer, self.dealer_profile)
        self.assertIn(self.abs_feature, car.features.all())
        self.assertEqual(car.slug, "toyota-corolla-2022")
        self.assertEqual(str(car), "Toyota Corolla 2022")

    def test_car_slug_persistence(self):
        """
        Test that if a slug is manually provided, it is not overwritten.
        """
        car = Car.objects.create(
            dealer=self.dealer_profile,
            brand="BMW",
            model="M5",
            year=2023,
            slug="custom-slug",
            fuel_type="petrol",
            transmission="manual",
            engine_volume=3.0,
            price=90000,
            condition="new",
            mileage=0,
            main_image="path/to/image.jpg"
        )
        self.assertEqual(car.slug, "custom-slug")
