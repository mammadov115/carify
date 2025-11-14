from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import CustomUser

class LogoutViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            role="buyer"
        )
        self.logout_url = reverse("logout")  
        self.home_url = reverse("home")    

    def test_logout_view_redirects_and_logs_out_user(self):
        # Log the user in first
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.logout_url)
        
        # Should redirect to home
        self.assertRedirects(response, self.home_url)
        
        # Check that the user is logged out
        response = self.client.get(self.home_url)
        user = response.context.get("user")
        self.assertFalse(user.is_authenticated)
