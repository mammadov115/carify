from django.db import models
from django.utils.text import slugify


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='models')

    def __str__(self):
        return f"{self.brand.name} {self.name}"


class Year(models.Model):
    year = models.IntegerField()

    def __str__(self):
        return f"{self.year}"
     

class Car(models.Model):
    """
    Represents a car listing with detailed information,
    including technical specs, pricing, condition,
    main image, and features.
    """


    AUCTION = 'auction'
    KOREA_STOCK = 'korea_stock'
    ON_THE_WAY = 'on_the_way'

    CATEGORY_CHOICES = [
        (AUCTION, 'Hərrac maşınları'),
        (KOREA_STOCK, 'Koreya stokumuz'),
        (ON_THE_WAY, 'Yolda satılır'),
    ]

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default=KOREA_STOCK
    )

    featured = models.BooleanField(
    default=False,
    help_text="Check to feature this car on the homepage."
    )
    

    # Basic info
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE, null=True)
    year = models.ForeignKey(Year, on_delete=models.CASCADE, null=True)
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