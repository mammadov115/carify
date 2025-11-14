from django.test import TestCase
from cars.models import Car, CarImage, CarFeature
from accounts.models import DealerProfile, CustomUser


class CarImageModelTest(TestCase):
    """
    Unit tests for the CarImage model.
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

    def test_carimage_creation(self):
        """
        Test that a CarImage can be created and linked to a Car.
        """
        car_image = CarImage.objects.create(
            car=self.car,
            image="path/to/gallery_image.jpg"
        )
        self.assertEqual(car_image.car, self.car)
        self.assertEqual(str(car_image), f"Image for {self.car}")
        self.assertIsNotNone(car_image.uploaded_at)
