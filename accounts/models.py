from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError


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


class BuyerProfile(models.Model):
    """
    Profile model for buyers.
    Stores additional information beyond the user account.
    """
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='buyer_profile'
    )
    phone_number = models.CharField(max_length=30)
    address = models.CharField(max_length=255, blank=True, null=True)

    # Wishlist and orders can be related later via ForeignKey or ManyToMany
    wishlist = models.ManyToManyField("cars.Car", blank=True, related_name='wishlisted_by')

    def clean(self):
        if self.user.role != 'buyer':
            raise ValidationError("User role must be 'buyer' to create a BuyerProfile.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class DealerProfile(models.Model):
    """
    Profile model for dealers.
    Stores company-specific information and statistics.
    """
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='dealer_profile'
    )
    company_name = models.CharField(max_length=100)
    tax_number = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=30)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def clean(self):
        """
        Ensure that only users with role 'dealer' can have a DealerProfile.
        """
        if self.user.role != 'dealer':
            raise ValidationError("User role must be 'dealer' to create a DealerProfile.")

    def save(self, *args, **kwargs):
        self.clean()  # validate before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return self.company_name
