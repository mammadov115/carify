from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginViewTest(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123",
            role="buyer"
        )
        self.url = reverse("login")  

    def test_login_get_request(self):
        """GET request should return the login page with status 200"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")
        self.assertIn("form", response.context)

    def test_login_post_valid_credentials(self):
        """POST with valid credentials should log the user in and redirect to home"""
        response = self.client.post(self.url, {
            "username": "testuser",
            "password": "password123"
        })
        self.assertRedirects(response, reverse("home"))
        # Check if user is authenticated
        user = response.wsgi_request.user
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.username, "testuser")

    def test_login_post_invalid_credentials(self):
        """POST with invalid credentials should return the form with errors"""
        response = self.client.post(self.url, {
            "username": "testuser",
            "password": "wrongpassword"
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")
        form = response.context["form"]
        self.assertTrue(form.errors)
