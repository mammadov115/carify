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
        self.login_url = reverse("login")

    def test_logout_requires_authentication(self):
        """
        Anonymous user should be redirected to login page when accessing logout.
        """
        response = self.client.get(self.logout_url)
        expected_redirect = f"{self.login_url}?next={self.logout_url}"

        self.assertRedirects(response, expected_redirect)

    def test_logout_logs_out_authenticated_user(self):
        """
        Authenticated user should be logged out and redirected to home page.
        """
        # Log in user
        self.client.force_login(self.user)

        # Perform logout
        response = self.client.get(self.logout_url)

        # Should redirect to home
        self.assertRedirects(response, self.home_url)

        # User MUST be logged out
        self.assertFalse(response.wsgi_request.user.is_authenticated)
