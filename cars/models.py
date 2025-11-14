from django.db import models
from django.utils.text import slugify
from accounts.models import DealerProfile, CustomUser


class CarFeature(models.Model):
    """
    Represents a specific feature or equipment of a car,
    e.g., ABS, Parking Sensor, Bluetooth.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Car(models.Model):
    """
    Represents a car listing with detailed information,
    including dealer, technical specs, pricing, condition,
    main image, and features.
    """
    # Dealer
    dealer = models.ForeignKey(
        DealerProfile,
        on_delete=models.SET_NULL,
        null=True,
        related_name='cars'
    )

    # Basic info
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    # Technical details
    fuel_type = models.CharField(
        max_length=20,
        choices=[
            ('petrol', 'Petrol'),
            ('diesel', 'Diesel'),
            ('hybrid', 'Hybrid'),
            ('electric', 'Electric')
        ]
    )
    transmission = models.CharField(
        max_length=20,
        choices=[
            ('automatic', 'Automatic'),
            ('manual', 'Manual')
        ]
    )
    engine_volume = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        help_text="Example: 1.6, 2.0, 3.5"
    )
    features = models.ManyToManyField(
        CarFeature,
        blank=True,
        related_name='cars'
    )

    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_negotiable = models.BooleanField(default=False)

    # Condition
    condition = models.CharField(
        max_length=20,
        choices=[
            ('new', 'New'),
            ('used', 'Used')
        ]
    )
    mileage = models.PositiveIntegerField(help_text="km")

    # Media
    main_image = models.ImageField(upload_to='cars/')

    # Description
    description = models.TextField(blank=True, null=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Automatically generates slug from brand, model, and year if not provided.
        """
        if not self.slug:
            self.slug = slugify(f"{self.brand}-{self.model}-{self.year}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand} {self.model} {self.year}"


class CarImage(models.Model):
    """
    Represents additional images for a car.
    Each car can have multiple images in a gallery.
    """
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='cars/gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.car}"


class CarReview(models.Model):
    """
    Represents a user's review of a car.
    Includes rating (1-5) and comment.
    """
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='car_reviews'
    )
    rating = models.PositiveSmallIntegerField()  # 1–5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review for {self.car} by {self.user}"


class FavoriteCar(models.Model):
    """
    Represents a user's favorite car (wishlist).
    A user cannot favorite the same car multiple times.
    """
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favorite_cars'
    )
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'car')

    def __str__(self):
        return f"{self.user} → {self.car}"
