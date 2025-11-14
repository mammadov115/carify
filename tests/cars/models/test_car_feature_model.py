from django.test import TestCase
from cars.models import CarFeature


class CarFeatureModelTest(TestCase):
    """
    Unit tests for the CarFeature model.
    """

    def test_create_car_feature(self):
        """
        Test creating a CarFeature and its string representation.
        """
        feature = CarFeature.objects.create(name="ABS")
        self.assertEqual(feature.name, "ABS")
        self.assertEqual(str(feature), "ABS")

    def test_create_multiple_features(self):
        """
        Test creating multiple CarFeature instances.
        """
        feature1 = CarFeature.objects.create(name="Parking Sensor")
        feature2 = CarFeature.objects.create(name="Bluetooth")
        features = CarFeature.objects.all()
        self.assertEqual(features.count(), 2)
        self.assertIn(feature1, features)
        self.assertIn(feature2, features)
