from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from accounts.models import DealerProfile, CustomUser
from cars.models import Car, CarFeature

class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("home")  # Make sure your url name is "home"

        # Create a dealer user and profile
        self.user = CustomUser.objects.create_user(
            username="dealer1",
            email="dealer1@example.com",
            password="testpass123",
            role="dealer"
        )
        self.dealer_profile = DealerProfile.objects.create(user=self.user)

        # Create some car features
        self.feature1 = CarFeature.objects.create(name="ABS")
        self.feature2 = CarFeature.objects.create(name="Airbags")

        # Create a dummy image for testing
        image = SimpleUploadedFile(
            name="test_car.jpg",
            content=b"",  # empty content is fine for test
            content_type="image/jpeg"
        )

        # Create two car objects
        self.car1 = Car.objects.create(
            dealer=self.dealer_profile,
            brand="Toyota",
            model="Corolla",
            year=2020,
            fuel_type="petrol",
            transmission="automatic",
            engine_volume=1.6,
            price=20000,
            is_negotiable=True,
            condition="used",
            mileage=15000,
            main_image=image,
            description="A nice used car"
        )
        self.car1.features.set([self.feature1, self.feature2])

        self.car2 = Car.objects.create(
            dealer=self.dealer_profile,
            brand="Honda",
            model="Civic",
            year=2022,
            fuel_type="hybrid",
            transmission="manual",
            engine_volume=2.0,
            price=25000,
            is_negotiable=False,
            condition="new",
            mileage=0,
            main_image=image,
            description="Brand new car"
        )
        self.car2.features.set([self.feature2])

    def test_home_view_status_code_and_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_home_view_context_contains_cars(self):
        response = self.client.get(self.url)
        self.assertIn("cars", response.context)

        # Check if cars are ordered newest first
        cars_in_context = list(response.context["cars"])
        self.assertEqual(cars_in_context, [self.car2, self.car1])

    # def test_home_view_displays_car_details(self):
    #     response = self.client.get(self.url)
    #     content = response.content.decode()

    #     # Check that car brand, model, and price appear in HTML
    #     self.assertIn(self.car1.brand, content)
    #     self.assertIn(self.car1.model, content)
    #     self.assertIn(str(int(self.car1.price)), content.)

    #     self.assertIn(self.car2.brand, content)
    #     self.assertIn(self.car2.model, content)
    #     self.assertIn(str(int(self.car2.price)), content)
