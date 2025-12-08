from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom manager for CustomUser to handle creation of users and superusers.
    """

    def create_user(self, username, email, password=None, role='buyer', **extra_fields):
        """
        Create and save a user with the given username, email, password, and role.
        """
        if not email:
            raise ValueError("The Email field must be set")
        if not username:
            raise ValueError("The Username field must be set")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Create and save a superuser with the given username and email.
        Superusers have role 'dealer' by default.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(username, email, password, role='dealer', **extra_fields)


class CustomUser(AbstractUser):
    """
    Custom user model to distinguish between buyers and dealers.
    """
    USER_ROLES = (
        ('buyer', 'Buyer'),
        ('dealer', 'Dealer'),
    )

    role = models.CharField(
        max_length=10,
        choices=USER_ROLES,
        default='buyer',
        help_text="Define if the user is a buyer or dealer"
    )

    objects = CustomUserManager()

    def is_buyer(self):
        """Check if the user is a buyer."""
        return self.role == 'buyer'

    def is_dealer(self):
        """Check if the user is a dealer."""
        return self.role == 'dealer'

