from django.test import TestCase
from cars.models import Car, CarFeature, CarReview
from accounts.models import DealerProfile, CustomUser


class CarReviewModelTest(TestCase):
    """
    Unit tests for the CarReview model.
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

    def test_carreview_creation(self):
        """
        Test that a CarReview can be created and linked to a car and user.
        """
        review = CarReview.objects.create(
            car=self.car,
            user=self.buyer_user,
            rating=5,
            comment="Excellent car!"
        )
        self.assertEqual(review.car, self.car)
        self.assertEqual(review.user, self.buyer_user)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "Excellent car!")
        self.assertEqual(str(review), f"Review for {self.car} by {self.buyer_user}")
        self.assertIsNotNone(review.created_at)
