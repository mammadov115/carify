from django.test import TestCase
from django.urls import reverse
from accounts.models import CustomUser, BuyerProfile, DealerProfile

class RegisterViewTest(TestCase):

    def setUp(self):
        self.url = reverse('register')

    def test_get_register_view(self):
        """Test GET request returns 200 and contains the registration form"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')

    def test_post_register_buyer_creates_user_and_profile(self):
        """Test POST request creates a buyer user and BuyerProfile"""
        data = {
            'username': 'buyer1',
            'email': 'buyer1@example.com',
            'password1': 'Testpass123!',
            'password2': 'Testpass123!',
            'role': 'buyer'
        }
        response = self.client.post(self.url, data)
        # Check redirect
        self.assertEqual(response.status_code, 302)

        # Check user is created
        user = CustomUser.objects.get(username='buyer1')
        self.assertEqual(user.role, 'buyer')

        # Check BuyerProfile is created
        self.assertTrue(BuyerProfile.objects.filter(user=user).exists())

    def test_post_register_dealer_creates_user_and_profile(self):
        """Test POST request creates a dealer user and DealerProfile"""
        data = {
            'username': 'dealer1',
            'email': 'dealer1@example.com',
            'password1': 'Testpass123!',
            'password2': 'Testpass123!',
            'role': 'dealer'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)

        user = CustomUser.objects.get(username='dealer1')
        self.assertEqual(user.role, 'dealer')
        self.assertTrue(DealerProfile.objects.filter(user=user).exists())
